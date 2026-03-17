from moviepy import VideoFileClip, concatenate_videoclips


def create_highlight(video_path, scenes, output_path):

    print("Creating highlight video...")

    video = VideoFileClip(video_path)

    clips = []

    for start, end in scenes:

        duration = end - start

        # bỏ scene quá ngắn
        if duration < 1:
            continue

        clip = video.subclipped(start, end)

        clips.append(clip)

    if len(clips) == 0:
        print("No valid scenes for highlight")
        return

    final = concatenate_videoclips(clips)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    video.close()

    print("Highlight saved to:", output_path)
