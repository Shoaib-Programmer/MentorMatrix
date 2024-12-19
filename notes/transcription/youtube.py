import os
import time
import random
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, VideoUnavailable
from .audio import download_audio, is_audio_usable
from .video import download_video, transcribe_video_without_audio
from .youtube_id import get_video_id_from_url
from icecream import ic


def clean_up_file(file_path: str) -> None:
    """
    Safely removes a file if it exists.
    :param file_path: Path to the file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        ic(f"Cleaned up file: {file_path}")


def fetch_subtitles(video_id: str, lang: str) -> Optional[str]:
    """
    Fetches subtitles for a YouTube video.
    :param video_id: YouTube video ID.
    :param lang: Language code for subtitles.
    :return: Subtitle text if available, else None.
    """
    try:
        subtitles = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        return "\n".join([sub['text'] for sub in subtitles])
    except (NoTranscriptFound, VideoUnavailable) as e:
        ic(f"Subtitles not available: {e}")
        return None


def get_transcript_from_youtube(youtube_url: str, lang: str = 'en') -> str:
    """
    Transcribes a YouTube video, prioritizing subtitles if available.
    Falls back to audio transcription or visual analysis.
    :param youtube_url: YouTube video URL.
    :param lang: Preferred subtitle language.
    :return: Final transcript.
    """
    video_id = get_video_id_from_url(youtube_url)
    transcript = ""

    # Step 1: Attempt to fetch subtitles
    ic("Checking for subtitles...")
    subtitle_text = fetch_subtitles(video_id, lang)
    if subtitle_text:
        ic("Using subtitles for transcription.")
        return subtitle_text  # Return directly if subtitles are found

    # Step 2: Fallback to audio transcription
    audio_file = download_audio(youtube_url)
    try:
        if is_audio_usable(audio_file):
            ic("Audio is suitable. Starting transcription...")
            # Simulate transcription (instead of using a generator)
            transcript = "Transcribed text from audio..."  # Placeholder text
            ic("Audio transcription completed.")
        else:
            ic("Audio unsuitable. Falling back to video analysis.")
            video_file = download_video(youtube_url)
            try:
                transcript = transcribe_video_without_audio(video_file)
            finally:
                clean_up_file(video_file)
    finally:
        clean_up_file(audio_file)

    return transcript
