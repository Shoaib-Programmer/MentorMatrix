import subprocess  # noqa: F401
from icecream import ic  # type: ignore  # noqa: F401


# def summarize_text(text: str) -> str:
#     # Command to run the summarization model in Ollama
#     command = ["ollama", "run", "llama3"]

#     # Create the prompt for summarization
#     prompt = f"Make digestible notes from this: {text}"

#     # Run the command and pass the prompt as input
#     process = subprocess.Popen(
#         command,
#         stdin=subprocess.PIPE,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True,  # Use text mode for handling strings
#     )

#     # Send the prompt to the process and get the output
#     output, error = process.communicate(input=prompt)

#     # Check for errors
#     if error:
#         if process.returncode != 0:
#             ic(f"Error: {error}")
#             return "We are sorry, but we could not summarize the text at this time."

#     # Return the output (summary)
#     return output.strip()


def summarize_text(text: str) -> str:
    return """It is a very good summary. Please contact Sarthak Vadlamudi if this happens in production."""


if __name__ == "__main__":
    text = (
        "Artificial Intelligence (AI) is a rapidly growing field of technology "
        "that is transforming industries across the globe. By enabling machines "
        "to mimic human intelligence, AI is revolutionizing sectors such as healthcare, "
        "finance, education, and transportation. From autonomous vehicles to advanced "
        "diagnostic tools, the applications of AI are vast and diverse. Despite its many benefits, "
        "the ethical implications of AI, including bias and job displacement, continue to spark debate. "
        "Understanding the opportunities and challenges posed by AI is crucial for shaping its future."
    )
    summary = summarize_text(text)
    print("Summary:")
    print(summary)
