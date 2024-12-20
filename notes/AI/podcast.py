import subprocess
from icecream import ic
from typing import Union
from pathlib import Path
from elevenlabs import generate, save

def podcast(text: str, speaker1: str, speaker2: str) -> str:
    # Prepare the command to run the summarization model in Ollama
    command = ['ollama', 'run', 'llama3']

    # Create the prompt for summarization
    prompt = f"Make a 2 speaker, fun, digestible podcast from: {text} \n\n\n The speakers are: {speaker1} and {speaker2}"

    # Run the command and pass the prompt for summarization
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send the prompt to the process and get the output
    output, error = process.communicate(input=prompt)

    # Check for errors
    if error:
        ic(f"Error: {error}")

    # Return the output (summary)
    return output

def text_to_podcast(text: str, save_file_at: Union[str, Path], speaker1: str = "Adam", speaker2: str = "Bella") -> None:
    """Converts the provided text to a human-like audio podcast using multiple speakers."""

    # Split the text by speakers for dialog-like output
    lines = text.splitlines()
    podcast_audio = b''

    for i, line in enumerate(lines):
        speaker = speaker1 if i % 2 == 0 else speaker2
        audio = generate(text=line, voice=speaker, model="eleven_multilingual_v1")
        podcast_audio += audio

    # Save the podcast to a file
    save(podcast_audio, str(save_file_at))

    print(f"Podcast saved at: {save_file_at}")
