import os
import time
from .audio import download_audio, is_audio_usable
from .video import download_video, transcribe_video_without_audio
from .util import extract_youtube_subtitles

# TODO: this file contains print messages that need to be removed

def get_transcript_from_youtube(youtube_url, lang='en'):
    """
    This function attempts to transcribe a YouTube video by first checking for available subtitles.
    If subtitles are available, it uses them; otherwise, it downloads the audio for transcription.
    If audio is unsuitable, it falls back to visual analysis.
    Yields progress updates and eventually returns the full transcript.
    """
    try:
        # Step 1: Check for subtitles
        print("Checking for subtitles...")
        subtitles = extract_youtube_subtitles(youtube_url, lang=lang)
        if subtitles:
            print("Subtitles found! Using subtitles for transcription.")
            transcript = "\n".join([sub['text'] for sub in subtitles])
            yield (transcript, 100)  # Subtitles are instantly 100% complete
            return transcript
    except ValueError as e:
        print(f"No subtitles available or error occurred: {e}")
        print("Falling back to audio transcription...")

    # Step 2: Download the audio
    audio_file = download_audio(youtube_url)

    # Check if the audio is suitable for transcription
    if is_audio_usable(audio_file):
        # Simulate the transcription process and yield progress
        total_duration = 10  # Simulate a 10-second transcription process
        progress = 0
        transcript = ""

        # Simulating transcription process with progress updates
        while progress < 100:
            time.sleep(1)  # Simulate delay (1 second)
            progress += 10  # Increment progress
            transcript += "Transcribed text chunk... "  # Simulated transcript chunk

            # Yield the current progress (used in streaming)
            yield (transcript, progress)

        print("\nAudio Transcription Completed:\n")
        print(transcript)

    else:
        print("Audio is not suitable for transcription, proceeding with visual analysis...")
        # If audio is not usable, fall back to video analysis
        video_file = download_video(youtube_url)
        visual_transcript = transcribe_video_without_audio(video_file)

        # Simulate a similar progress update for visual analysis
        transcript = visual_transcript  # Assigning the visual transcript as fallback

        yield (transcript, 100)  # Mark as 100% complete

    # Clean up the downloaded audio file
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return transcript  # Final transcript
