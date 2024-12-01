import os
from .audio import *
from .video import *


def extract_audio_from_video(video_path, audio_path="extracted_audio.wav"):
    """
    Extracts audio from a video file and saves it as a WAV file.

    Parameters:
        video_path (str): Path to the video file.
        audio_path (str): Path where the extracted audio will be saved.

    Returns:
        str: The path to the extracted audio file.
    """
    # Use ffmpeg to extract the audio from the video and save it as a WAV file
    os.system(f"ffmpeg -i \"{video_path}\" -vn -acodec pcm_s16le -ar 44100 -ac 2 \"{audio_path}\"")
    return audio_path


def transcribe_video(video_path):
    """
    Transcribes a video by analyzing its audio and visual content.
    If audio is clear and usable, it uses Whisper for transcription.
    Otherwise, it uses OCR to transcribe visuals from key frames.

    Parameters:
        video_path (str): Path to the video file.

    Returns:
        str: The transcript, either from audio or visual analysis.
    """
    # Step 1: Extract the audio from the video
    audio_file = extract_audio_from_video(video_path)

    # Step 2: Check if the audio is usable
    if is_audio_usable(audio_file):
        # If the audio is usable, transcribe using Whisper
        print("Audio is clear. Transcribing audio...")
        transcript = transcribe_audio(audio_file)
    else:
        # If the audio is not usable, proceed with visual transcription
        print("Audio is not usable. Transcribing video visually...")
        transcript = transcribe_video_without_audio(video_path)

    # Clean up the extracted audio file after use
    if os.path.exists(audio_file):
        os.remove(audio_file)

    return transcript


def main():
    # Get video path from user input
    video_path = input("Enter the path of the video file: ")

    # Ensure the video file exists
    if not os.path.exists(video_path):
        print("Error: The video file does not exist.")
        return

    # Step 1: Transcribe the video based on audio and visual content
    transcript = transcribe_video(video_path)

    # Step 2: Output the transcription result
    print("\nTranscription Result:")
    print(transcript)


if __name__ == "__main__":
    main()
