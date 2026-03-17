import ffmpeg
import os


def extract_audio(video_path, audio_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Input video file not found: {video_path}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, ac=1, ar="16000")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode()}")
        raise
