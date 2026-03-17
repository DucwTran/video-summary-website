from utils.video_utils import extract_intelligent_frames


def run_extract_frames(video_path, frame_dir, whisper_segments=None):

    count = extract_intelligent_frames(
        video_path,
        frame_dir,
        whisper_segments
    )

    print(f"Extracted {count} intelligent frames")

    return count
