from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

def detect_scenes(video_path):

    print("Detecting scenes by images...")

    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()

    # threshold thấp hơn để detect nhiều scene hơn
    scene_manager.add_detector(ContentDetector(threshold=25))

    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    scene_list = scene_manager.get_scene_list()

    scenes = [
        (scene[0].get_seconds(), scene[1].get_seconds())
        for scene in scene_list
    ]

    print(f"Detected {len(scenes)} visual scenes")

    return scenes


def detect_scenes_by_voice(segments, pause_threshold=1.5):
    """
    Gom các câu nói (segments) lại thành scenes.
    Nếu khoảng cách giữa câu trước và câu sau > pause_threshold,
    thì cắt thành scene mới.
    """
    print("Detecting scenes by voice pauses...")

    if not segments:
        return []

    scenes = []
    current_start = segments[0]["start"]
    current_end = segments[0]["end"]

    for i in range(1, len(segments)):
        seg = segments[i]
        
        # Nếu khoảng lặng giữa 2 segment liên tiếp quá mức cho phép
        if seg["start"] - current_end > pause_threshold:
            # Lưu lại scene hiện tại
            scenes.append((current_start, current_end))
            # Bắt đầu scene mới
            current_start = seg["start"]
            current_end = seg["end"]
        else:
            # Nếu chênh lệch ngắn, nhập chung vào scene hiện tại, kéo dài current_end
            current_end = max(current_end, seg["end"])

    # Thêm scene cuối cùng vào danh sách
    scenes.append((current_start, current_end))

    print(f"Detected {len(scenes)} voice scenes")
    return scenes
