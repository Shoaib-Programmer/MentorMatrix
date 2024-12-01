import yt_dlp
import whisper
import tempfile
import time
import os
import json


# Hardcoded cookies in JSON format
HARDCODED_COOKIES_JSON = [
    {
        "domain": ".youtube.com",
        "expirationDate": 1765629118.925841,
        "hostOnly": False,
        "httpOnly": True,
        "name": "HSID",
        "path": "/",
        "secure": False,
        "value": "A8z8P51feEiOXlpHD"
    },
    {
        "domain": ".youtube.com",
        "expirationDate": 1765629118.92595,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SSID",
        "path": "/",
        "secure": True,
        "value": "AKuCPY1h4DQvajHsS"
    },
    # Add the rest of the cookies here...
]

def create_temp_cookies_file(cookies_json):
    """
    Create a temporary cookies file in Netscape format from the provided JSON cookies.
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    for cookie in cookies_json:
        domain = cookie["domain"]
        flag = "TRUE" if not cookie["hostOnly"] else "FALSE"
        path = cookie["path"]
        secure = "TRUE" if cookie["secure"] else "FALSE"
        expiration = str(int(cookie["expirationDate"])) if "expirationDate" in cookie else "0"
        name = cookie["name"]
        value = cookie["value"]
        temp_file.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n")
    temp_file.close()
    return temp_file.name


def extract_youtube_subtitles(youtube_url, lang='en'):
    """
    Extract subtitles from a YouTube video using yt_dlp, with added techniques to bypass CAPTCHA.

    Parameters:
        youtube_url (str): The URL of the YouTube video.
        lang (str): Language code for subtitles (default: 'en').

    Returns:
        list: A list of subtitle entries containing start time, duration, and text.
    """
    # Headers to mimic a browser
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    ydl_opts = {
        'skip_download': True,  # Do not download the video
        'quiet': True,          # Suppress console output
        'writesubtitles': True, # Download subtitles
        'writeautomaticsub': True,  # Fallback to auto-generated subtitles if needed
        'subtitlesformat': 'json',  # Download subtitles in JSON format
        'outtmpl': '%(id)s.%(ext)s',  # Save subtitle file temporarily
        'http_headers': {
            'User-Agent': user_agent,  # Mimic browser User-Agent
        },
        'cookiefile': 'cookies.txt',  # Use cookies to avoid CAPTCHA
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract video info
            info_dict = ydl.extract_info(youtube_url, download=False)
            video_id = info_dict['id']

            # Check available subtitles
            if 'subtitles' not in info_dict and 'automatic_captions' not in info_dict:
                raise ValueError("No subtitles available for this video.")

            # Prefer user-uploaded subtitles
            subtitles = info_dict.get('subtitles', {}) or info_dict.get('automatic_captions', {})
            if lang not in subtitles:
                raise ValueError(f"Subtitles for language '{lang}' are not available.")

            # Download subtitles
            ydl_opts['subtitleslangs'] = [lang]
            ydl.download([youtube_url])

            # Parse JSON subtitle file
            subtitle_file = f"{video_id}.{lang}.json"
            try:
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Extract relevant subtitle entries
                subtitles = [
                    {
                        'start': float(entry['start']),
                        'duration': float(entry.get('dur', 0)),
                        'text': entry['text']
                    }
                    for entry in data['events'] if 'text' in entry
                ]
                return subtitles
            finally:
                # Clean up temporary subtitle file
                if os.path.exists(subtitle_file):
                    os.remove(subtitle_file)

        except yt_dlp.utils.DownloadError as e:
            raise RuntimeError("Failed to bypass CAPTCHA or download subtitles.") from e




def download_media(youtube_url, media_type='audio'):
    """
    Download YouTube media (audio or video) based on the specified type using hardcoded cookies.

    :param youtube_url: The YouTube video URL.
    :param media_type: Type of media to download ('audio' or 'video'). Default is 'audio'.
    :return: File path of the downloaded media.
    """
    # Use the hardcoded cookies
    cookies_file = create_temp_cookies_file(HARDCODED_COOKIES_JSON)

    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'cookies': cookies_file,  # Use the temporary cookies file
        }
    elif media_type == 'video':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloaded_video.%(ext)s',
            'cookies': cookies_file,  # Use the temporary cookies file
        }
    else:
        raise ValueError("Invalid media_type. Must be 'audio' or 'video'.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Using hardcoded cookies")  # Debug log
            info_dict = ydl.extract_info(youtube_url, download=True)  # Download the media
            if media_type == 'audio':
                return 'downloaded_audio.wav'
            elif media_type == 'video':
                return 'downloaded_video.mp4'
    except Exception as e:
        print(f"Error downloading {media_type}: {e}")
        return None

def transcribe_audio(audio_file):
    """
    Transcribe audio using Whisper model.

    :param audio_file: Path to the audio file.
    :return: Transcription text.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['text']

def download_audio(youtube_url):
    download_media(youtube_url)

def download_video(youtube_url):
    download_media(youtube_url, media_type='video')

# Example usage:
# download_audio("https://www.youtube.com/watch?v=example")
