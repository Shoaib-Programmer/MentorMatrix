import subprocess
from icecream import ic  # type: ignore
from typing import Union
from pathlib import Path
import os
import pyttsx3  # type: ignore


def generate_podcast(text: str, speaker1: str, speaker2: str) -> str:
    """Generate a podcast-style dialogue using a summarization model."""
    # Prepare the command to run the summarization model in Ollama
    command = ["ollama", "run", "llama3"]

    # Create the prompt for summarization
    prompt = f"Make a 2 speaker, fun, digestible podcast, no more than 300 words, from: {text} \n\n\n The speakers are: {speaker1} and {speaker2}"

    try:
        # Run the command and pass the prompt for summarization
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Send the prompt to the process and get the output
        output, error = process.communicate(input=prompt)

        # Check for errors
        if error:
            if process.returncode != 0:
                ic(f"Error: {error or 'Subprocess failed unexpectedly'}")
                return ""
        return output

    except Exception as e:
        ic(f"Error running subprocess: {str(e)}")
        return ""


def get_voice_by_name(engine, name: str):
    """Returns the voice ID matching the given name."""
    voices = engine.getProperty("voices")
    for voice in voices:
        if name.lower() in voice.name.lower():
            return voice.id
    return voices[0].id  # Default to the first available voice if not found


def text_to_podcast(
    text: str,
    save_file_at: Union[str, Path],
    speaker1: str = "Adam",
    speaker2: str = "Bella",
) -> None:
    """Converts the provided text to an audio podcast using two speakers."""

    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Get the voice IDs based on the speaker names
    voice1_id = get_voice_by_name(engine, speaker1)
    voice2_id = get_voice_by_name(engine, speaker2)

    # Split the text by speakers for dialog-like output
    lines = text.splitlines()

    # Initialize a list to hold the generated file names
    temp_files = []

    # Iterate through each line and assign speakers
    for i, line in enumerate(lines):
        # Choose speaker based on the line number
        speaker_id = voice1_id if i % 2 == 0 else voice2_id

        # Set the speaker's voice
        engine.setProperty("voice", speaker_id)

        # Store speech to a temporary audio file
        temp_file = f"temp_{i}.mp3"
        engine.save_to_file(line, temp_file)

        # Add the temporary file name to the list
        temp_files.append(temp_file)

    # Final step: Combine all audio files into a single podcast file
    try:
        combine_audio_files_ffmpeg(temp_files, save_file_at)
    finally:
        for file in temp_files:
            os.remove(file)

    # Clean up the temporary files after combining them
    for file in temp_files:
        os.remove(file)

    ic(f"Podcast saved at: {save_file_at}")
    engine.runAndWait()


def combine_audio_files_ffmpeg(file_list: list, output_file: str) -> None:
    """Combines the provided audio files into one and saves it to the specified output file using ffmpeg."""
    # Create the file string in ffmpeg compatible format
    file_string = "|".join(file_list)

    # Run the ffmpeg command to combine the files
    command = ["ffmpeg", "-i", f"concat:{file_string}", "-acodec", "copy", output_file]
    subprocess.run(command, check=True)
