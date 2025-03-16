import os

import logging
from icecream import ic  # type: ignore

from .audio import download_audio, is_audio_usable, transcribe_audio

# from .video import download_video, transcribe_video_without_audio
from .youtube_id import get_video_id_from_url

from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
from youtube_transcript_api._errors import (  # type: ignore
    NoTranscriptFound,
    VideoUnavailable,
    TranscriptsDisabled,
)  # type: ignore


logging.basicConfig(level=logging.ERROR)


def clean_up_file(file_path: str) -> None:
    """
    Safely removes a file if it exists.
    :param file_path: Path to the file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        ic(f"Cleaned up file: {file_path}")


def fetch_transcript(video_id):
    try:
        response = YouTubeTranscriptApi.get_transcript(video_id)
        text_results = []
        for part in response:
            text_results.append(part["text"])

        transcript = " ".join(text_results)
        return transcript
    except VideoUnavailable:
        logging.error(f"Video unavailable: {video_id}")
    except NoTranscriptFound:
        logging.error(f"No transcript found for video ID {video_id}.")
        return None
    except TranscriptsDisabled:
        logging.error(f"Subtitles are disabled for video ID {video_id}.")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


def get_transcript_from_youtube(youtube_url: str, lang: str = "en") -> str:
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
    subtitle_text = fetch_transcript(video_id)
    if subtitle_text:
        ic("Using subtitles for transcription.")
        return subtitle_text  # Return directly if subtitles are found

    # Step 2: Fallback to audio transcription
    audio_file = download_audio(youtube_url)
    # try:
    #     if is_audio_usable(audio_file):
    #         ic("Audio is suitable. Starting transcription...")
    #         # Simulate transcription (instead of using a generator)
    #         transcript = "Transcribed text from audio..."  # Placeholder text
    #         ic("Audio transcription completed.")
    #     else:
    #         ic("Audio unsuitable. Falling back to video analysis.")
    #         video_file = download_video(youtube_url)
    #         try:
    #             transcript = transcribe_video_without_audio(video_file)
    #         finally:
    #             clean_up_file(video_file)
    # finally:
    #     clean_up_file(audio_file)

    try:
        ic("Audio is suitable. Starting transcription...")
        # Simulate transcription (instead of using a generator)
        transcript = transcribe_audio(audio_file)
        ic("Audio transcription completed.")

    finally:
        clean_up_file(audio_file)
    return transcript
