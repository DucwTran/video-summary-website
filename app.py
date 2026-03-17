import os
import shutil
import uuid
import json
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Import pipeline functions
from pipeline.extract_audio import extract_audio
from pipeline.speech_to_text import speech_to_text
from pipeline.extract_frames import run_extract_frames
from pipeline.caption_frames import caption_frames
from pipeline.summarize import summarize

from config import *

app = FastAPI(title="AI Video Summarizer")

# Setup directories
UPLOAD_DIR = Path("data/uploads")
OUTPUT_DIR = Path("data/output")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Templates and Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="data/output"), name="output")
templates = Jinja2Templates(directory="templates")

# In-memory status tracking (for a real app, use a database or Redis)
processing_jobs = {}

def run_pipeline(job_id: str, video_path: str):
    try:
        job_dir = OUTPUT_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        audio_path = str(job_dir / "audio.wav")
        transcript_path = str(job_dir / "transcript.txt")
        captions_path = str(job_dir / "captions.json")
        summary_path = str(job_dir / "summary.txt")
        frame_dir = str(job_dir / "frames")
        
        processing_jobs[job_id]["status"] = "Extracting audio..."
        extract_audio(video_path, audio_path)
        
        processing_jobs[job_id]["status"] = "Speech to text..."
        whisper_result = speech_to_text(audio_path, transcript_path)
        
        processing_jobs[job_id]["status"] = "Extracting frames..."
        run_extract_frames(video_path, frame_dir, whisper_result.get("segments"))
        
        processing_jobs[job_id]["status"] = "Captioning frames..."
        caption_frames(frame_dir, captions_path)
        
        processing_jobs[job_id]["status"] = "Generating summary..."
        summarize(transcript_path, captions_path, summary_path)
        
        # --- NEW HIGHLIGHT PIPELINE ---
        processing_jobs[job_id]["status"] = "Detecting voice scenes..."
        from pipeline.scene_detect import detect_scenes_by_voice, detect_scenes
        from pipeline.highlight_score import rank_scenes
        from pipeline.highlight_video import create_highlight
        
        segments = whisper_result.get("segments", [])
        highlight_url = None
        
        try:
            print(f"[{job_id}] Detecting scenes from {len(segments)} segments...")
            if segments:
                voice_scenes = detect_scenes_by_voice(segments, pause_threshold=1.5)
            else:
                # Fallback: API không trả segments, dùng detect_scenes hình ảnh gốc
                print(f"[{job_id}] No audio segments found! Fallback to image scene detection.")
                voice_scenes = detect_scenes(video_path)
                
            print(f"[{job_id}] Found {len(voice_scenes)} scenes.")
            
            processing_jobs[job_id]["status"] = "Scoring scenes..."
            with open(captions_path, "r", encoding="utf-8") as f:
                captions_data = json.load(f)
                
            ranked_scenes = rank_scenes(voice_scenes, segments, captions_data)
            print(f"[{job_id}] Ranked {len(ranked_scenes)} scenes.")
            
            from moviepy import VideoFileClip
            
            # Get original video duration
            with VideoFileClip(video_path) as clip:
                total_duration = clip.duration
                
            target_duration = total_duration * 0.35 # Target around 35% of original length
            
            top_scenes_unordered = []
            accumulated_duration = 0
            
            # Khởi tạo chọn các scene cho đến khi đạt giới hạn 30-40%
            for r in ranked_scenes:
                start, end = r["scene"]
                scene_duration = end - start
                
                # Bỏ qua scene quá ngắn hoặc lỗi
                if scene_duration < 1:
                    continue
                    
                top_scenes_unordered.append(r["scene"])
                accumulated_duration += scene_duration
                
                if accumulated_duration >= target_duration:
                    break
                    
            # Nếu người dùng có video quá ngắn, đảm bảo chọn ít nhất 1 hoặc 2 scenes
            if not top_scenes_unordered and ranked_scenes:
                top_scenes_unordered.append(ranked_scenes[0]["scene"])
                
            top_scenes = sorted(top_scenes_unordered, key=lambda x: x[0])
            print(f"[{job_id}] Selected {len(top_scenes)} scenes (Total duration: {accumulated_duration:.2f}s, Target: {target_duration:.2f}s) for video: {top_scenes}")
            
            processing_jobs[job_id]["status"] = "Creating highlight video..."
            highlight_path = str(job_dir / "highlight.mp4")
            create_highlight(video_path, top_scenes, highlight_path)
            
            if os.path.exists(highlight_path):
                print(f"[{job_id}] Highlight video successfully saved to {highlight_path}")
                highlight_url = f"/output/{job_id}/highlight.mp4"
                processing_jobs[job_id]["highlight_url"] = highlight_url
            else:
                print(f"[{job_id}] Highlight video file was not created!")

        except Exception as e:
            print(f"[{job_id}] Error in highlight pipeline: {str(e)}")
            import traceback
            traceback.print_exc()
        # ------------------------------
        
        # Read final summary
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_content = f.read()
            
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_content = f.read()
            
        processing_jobs[job_id]["status"] = "Completed"
        processing_jobs[job_id]["result"] = {
            "summary": summary_content,
            "transcript": transcript_content,
            "highlight_url": highlight_url
        }
        
    except Exception as e:
        processing_jobs[job_id]["status"] = f"Error: {str(e)}"
        print(f"Error processing {job_id}: {e}")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    processing_jobs[job_id] = {"status": "Starting...", "filename": file.filename}
    background_tasks.add_task(run_pipeline, job_id, str(file_path))
    
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = processing_jobs.get(job_id)
    if not job:
        return JSONResponse(status_code=404, content={"message": "Job not found"})
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
