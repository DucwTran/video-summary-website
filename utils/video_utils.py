import cv2
import os


def get_video_info(video_path):
    """
    Lấy thông tin cơ bản của video
    """

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = frame_count / fps if fps > 0 else 0

    cap.release()

    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration
    }


def extract_intelligent_frames(video_path, output_dir, whisper_segments=None):
    """
    Trích xuất frame thông minh:
    1. Dùng Scene Detect để tìm chuyển cảnh.
    2. Dùng Whisper timestamps để lấy frame đầu mỗi đoạn thoại.
    """
    import os
    import cv2
    from scenedetect import detect, ContentDetector

    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Scene Detection
    print("Detecting scenes...")
    scene_list = detect(video_path, ContentDetector())
    scene_timestamps = [scene[0].get_seconds() for scene in scene_list]
    
    # 2. Whisper Timestamps
    audio_timestamps = []
    if whisper_segments:
        audio_timestamps = [seg['start'] for seg in whisper_segments]
    
    # 3. Combine and Merge nearby timestamps (closer than 2 seconds)
    all_timestamps = sorted(list(set(scene_timestamps + audio_timestamps)))
    filtered_timestamps = []
    if all_timestamps:
        filtered_timestamps.append(all_timestamps[0])
        for ts in all_timestamps[1:]:
            if ts - filtered_timestamps[-1] >= 2.0:
                filtered_timestamps.append(ts)
    
    # 4. Extract Frames at specific timestamps
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    saved_count = 0
    for ts in filtered_timestamps:
        frame_idx = int(ts * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            # Lọc khung hình bị mờ (blur detection)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            if fm < 100:  # Ngưỡng mờ thông dụng
                continue

            # Lọc khung hình quá tối (darkness detection)
            if gray.mean() < 15:  # Ngưỡng tối (cảnh đen)
                continue

            path = os.path.join(output_dir, f"frame_{saved_count}.jpg")
            # Store timestamp in metadata if possible, or just keep it simple
            cv2.imwrite(path, frame)
            saved_count += 1
            
    cap.release()
    print(f"Extracted {saved_count} intelligent frames.")
    return saved_count
