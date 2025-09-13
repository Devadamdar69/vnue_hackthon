from moviepy import (
    VideoFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    concatenate_videoclips
)

# Load the video
clip = VideoFileClip("no_chance_behara_do_it.mp4")  # Use relative or full path

# Cut the first 5 seconds
short_clip = clip.subclipped(0, 5)

# Save the trimmed clip
short_clip.write_videofile(
    "output_video.mp4",
    codec="libx264",
    audio_codec="aac",
    fps=24  # Optional: force frame rate if needed
)
