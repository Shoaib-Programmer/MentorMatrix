import os
import time
import random
from typing import Generator, Tuple, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, VideoUnavailable
from .audio import download_audio, is_audio_usable
from .video import download_video, transcribe_video_without_audio
from .youtube_id import get_video_id_from_url
from icecream import ic


def simulate_progress(
    total_steps: int = 10, step_duration: float = 1.0
) -> Generator[int, None, None]:
    """
    Simulates progress updates.
    :param total_steps: Total number of progress steps.
    :param step_duration: Duration (in seconds) for each step.
    """
    progress = 0
    increment = 100 // total_steps
    while progress < 100:
        time.sleep(step_duration + random.uniform(0.1, 0.5))
        progress += increment
        yield progress


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


def get_transcript_from_youtube(youtube_url: str, lang: str = 'en') -> Generator[Tuple[str, int], None, str]:
    """
    Transcribes a YouTube video, prioritizing subtitles if available.
    Falls back to audio transcription or visual analysis.
    :param youtube_url: YouTube video URL.
    :param lang: Preferred subtitle language.
    :yield: Partial transcript and progress updates.
    :return: Final transcript.
    """
    video_id = get_video_id_from_url(youtube_url)
    transcript = ""

    # Step 1: Attempt to fetch subtitles
    ic("Checking for subtitles...")
    subtitle_text = fetch_subtitles(video_id, lang)
    if subtitle_text:
        ic("Using subtitles for transcription.")
        yield (subtitle_text, 100)
        return subtitle_text

    # Step 2: Fallback to audio transcription
    audio_file = download_audio(youtube_url)
    try:
        if is_audio_usable(audio_file):
            ic("Audio is suitable. Starting transcription...")
            for progress in simulate_progress():
                partial_transcript = "Transcribed text chunk... "  # Simulated text
                transcript += partial_transcript
                yield (transcript, progress)
            ic("Audio transcription completed.")
        else:
            ic("Audio unsuitable. Falling back to video analysis.")
            video_file = download_video(youtube_url)
            try:
                transcript = transcribe_video_without_audio(video_file)
                yield (transcript, 100)
            finally:
                clean_up_file(video_file)
    finally:
        clean_up_file(audio_file)

    return transcript
