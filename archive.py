import os
import time
import yt_dlp
import subprocess
import requests
#https://github.com/yt-dlp/FFmpeg-Builds?tab=readme-ov-file#ffmpeg-static-auto-builds for ffmpeg

def check_internet_connection():
    try:
        response = requests.get("https://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False    


def download_video(video_url, output_path="downloads", renamed_filename="downloaded_video"):
    # Download options for yt-dlp
    ydl_options = {
        'live_from_start': True,
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f"{output_path}/{renamed_filename}.%(ext)s",  # Use renamed_filename here
        'verbose': True,
        #"skip_download":True,
        #"listformats":True
    }

    while True:
        try:
            # Download the video using yt-dlp
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                info = ydl.extract_info(video_url, download=True)
            # Get the downloaded video file path
            video_file_path = ydl.prepare_filename(info)
            return video_file_path, renamed_filename
        except yt_dlp.utils.DownloadError:
            print("Checking internet connection.")
            if check_internet_connection():
                print("something unexpected happened")
            else:
                print("No internet. Retrying in 20 seconds.")
                time.sleep(20)  # Wait for 20 minutes before retrying


def encode_video_nvenc(input_path, output_path, output_format='mp4', crf=23, max_framerate=30, resolution='854x480',bitrate="1000k"):
    # Reencoding options for ffmpeg with NVENC, CRF, max framerate, and resolution
    ffmpeg_options = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'h264_nvenc',  # NVENC H.264 video codec
        '-b:v', bitrate,  # Set bitrate to 0 for CRF mode
        '-preset', 'fast',
        # '-crf', str(crf),  # Constant Rate Factor (adjust as needed)
        '-pix_fmt', 'yuv420p',
        '-profile:v', 'baseline',
        #'-level', '3.0',
        '-max_muxing_queue_size', '1024',  # Control peak framerate
        '-r', str(max_framerate),  # Set max output framerate
        '-s', resolution,  # Set output resolution
        '-c:a', 'aac',  # Audio codec
        '-strict', 'experimental',  # Allow using experimental codecs (needed for some audio codecs)
        '-b:a', '128k',  # Audio bitrate
        '-movflags', '+faststart',
        '-threads', '0',# if set to 0 ffmpeg will use the max amount of threads available
        output_path,  # Output file path
    ]
    # Run the ffmpeg command
    subprocess.run(ffmpeg_options)


if __name__ == "__main__":
    url = f"""url here"""

    # Download the video
    filename=r"""trying to chill"""
    video_path, video_title = download_video(url,renamed_filename=filename,output_path=f"F:\\downloads")

    #video_path = f"""F:\\downloads\\FF VII Rebirth (Gongaga) 7.mp4"""
    #video_title = f"""FF VII Rebirth (Gongaga) 7"""
    # Define the output path for the re encoded video
    # {video_title}
    output = f"downloads/{video_title}_480p.mp4"

    # Encode the video using ffmpeg with NVENC, CRF, max framerate, and resolution
    #854x480 1280x720
    encode_video_nvenc(video_path, output, crf=35, max_framerate=30, resolution='854x480',bitrate="1500k")

    print(f"finished")

    os.system("shutdown.exe /h")
