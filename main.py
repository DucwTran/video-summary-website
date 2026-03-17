import os
import json
os.environ["TRANSFORMERS_VERIFY_ADVISORIES"] = "0"

from pipeline.extract_audio import extract_audio
from pipeline.speech_to_text import speech_to_text
from pipeline.extract_frames import run_extract_frames
from pipeline.caption_frames import caption_frames
from pipeline.summarize import summarize
from pipeline.scene_detect import detect_scenes
from pipeline.highlight_score import rank_scenes
from pipeline.highlight_video import create_highlight
from config import *


def main():

    print("Step 1: Extract audio")
    extract_audio(VIDEO_PATH, AUDIO_PATH)

    print("Step 2: Speech to text")
    whisper_result = speech_to_text(AUDIO_PATH, TRANSCRIPT_PATH)

    print("Step 3: Extract frames")
    run_extract_frames(VIDEO_PATH, FRAME_DIR, whisper_result.get("segments"))

    print("Step 4: Caption frames")
    caption_frames(FRAME_DIR, CAPTIONS_PATH)

    print("Step 5: Summarize")
    summarize(TRANSCRIPT_PATH, CAPTIONS_PATH, SUMMARY_PATH)

    print("Step 6: Create highlight video")

    scenes = detect_scenes(VIDEO_PATH)

    segments = whisper_result.get("segments")

    with open(CAPTIONS_PATH, encoding="utf-8") as f:
        captions = json.load(f)

    ranked = rank_scenes(scenes, segments, captions)

    from moviepy import VideoFileClip
    
    with VideoFileClip(VIDEO_PATH) as clip:
        total_duration = clip.duration
        
    target_duration = total_duration * 0.35
    
    top_scenes_unordered = []
    accumulated_duration = 0
    
    for r in ranked:
        start, end = r["scene"]
        scene_dur = end - start
        
        if scene_dur < 1:
            continue
            
        top_scenes_unordered.append(r["scene"])
        accumulated_duration += scene_dur
        
        if accumulated_duration >= target_duration:
            break
            
    if not top_scenes_unordered and ranked:
        top_scenes_unordered.append(ranked[0]["scene"])
        
    top_scenes = sorted(top_scenes_unordered, key=lambda x: x[0])

    print("Top scenes:", top_scenes)
    print(f"Total highlight duration chosen: {accumulated_duration:.2f}s out of {total_duration:.2f}s (~{accumulated_duration/total_duration*100:.1f}%)")

    create_highlight(
        VIDEO_PATH,
        top_scenes,
        "highlight.mp4"
    )
    
    print("Done.")


if __name__ == "__main__":
    main()
