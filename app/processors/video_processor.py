
import os

def extract_audio_from_video(video_path: str, out_path: str) -> str:
    # Requires ffmpeg installed on the system.
    cmd = f'ffmpeg -y -i "{video_path}" -vn -acodec mp3 "{out_path}"'
    os.system(cmd)
    return out_path
