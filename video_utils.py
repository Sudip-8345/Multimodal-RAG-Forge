import os
import yt_dlp
from moviepy.editor import VideoFileClip

# Download video from YouTube
def download_video(url, output_path):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'{output_path}/input_vid.%(ext)s',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        metadata = {
            "Author": info.get('uploader'),
            "Title": info.get('title'),
            "Views": info.get('view_count')
        }
    return metadata

# Extract frames from video
def video_to_images(video_path, output_folder, fps=0.1):
    os.makedirs(output_folder, exist_ok=True)
    clip = VideoFileClip(video_path)
    clip.write_images_sequence(os.path.join(output_folder, "frame%04d.png"), fps=fps)
    clip.close()

# Extract audio from video
def video_to_audio(video_path, output_audio_path):
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(output_audio_path)
    clip.close()
