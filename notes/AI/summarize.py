# 1. Using BART
# from transformers import BartForConditionalGeneration, BartTokenizer

# # Load pre-trained BART model and tokenizer from Hugging Face
# model_name_bart = "facebook/bart-large-cnn"
# model_bart = BartForConditionalGeneration.from_pretrained(model_name_bart)
# tokenizer_bart = BartTokenizer.from_pretrained(model_name_bart)

# # Function to summarize text using BART
# def summarize_text(text: str, max_length=150, min_length=50) -> str:
#     # Tokenize the input text
#     inputs = tokenizer_bart([text], max_length=1024, return_tensors="pt", truncation=True, padding=True)

#     # Generate the summary ids
#     summary_ids = model_bart.generate(
#         inputs["input_ids"],
#         max_length=max_length,
#         min_length=min_length,
#         length_penalty=2.0,
#         num_beams=4,
#         early_stopping=True
#     )

#     # Decode the summary
#     summary = tokenizer_bart.decode(summary_ids[0], skip_special_tokens=True)
#     return summary


# 2. Using T5
# from transformers import T5ForConditionalGeneration, T5Tokenizer

# # Load pre-trained T5 model and tokenizer from Hugging Face
# model_name_t5 = "t5-base"
# model_t5 = T5ForConditionalGeneration.from_pretrained(model_name_t5)
# tokenizer_t5 = T5Tokenizer.from_pretrained(model_name_t5)

# # Function to summarize text using T5
# def summarize_text_t5(text: str, max_length=150, min_length=50) -> str:
#     # Prepend the task prefix for T5
#     input_text = "summarize: " + text
#     inputs = tokenizer_t5(input_text, return_tensors="pt", max_length=512, truncation=True)

#     # Generate the summary ids
#     summary_ids = model_t5.generate(
#         inputs["input_ids"],
#         max_length=max_length,
#         min_length=min_length,
#         length_penalty=2.0,
#         num_beams=4,
#         early_stopping=True
#     )

#     # Decode the summary
#     summary = tokenizer_t5.decode(summary_ids[0], skip_special_tokens=True)
#     return summary


import subprocess
from icecream import ic

def summarize_text(text: str) -> str:
    # Prepare the command to run the summarization model in Ollama
    command = ['ollama', 'run', 'llama3']

    # Create the prompt for summarization
    prompt = f"Make digestible notes from this: {text}"

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

