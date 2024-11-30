# 1. Using BART
from transformers import BartForConditionalGeneration, BartTokenizer

# Load pre-trained BART model and tokenizer from Hugging Face
model_name_bart = "facebook/bart-large-cnn"
model_bart = BartForConditionalGeneration.from_pretrained(model_name_bart)
tokenizer_bart = BartTokenizer.from_pretrained(model_name_bart)

# Function to summarize text using BART
def summarize_text(text: str, max_length=150, min_length=50) -> str:
    # Tokenize the input text
    inputs = tokenizer_bart([text], max_length=1024, return_tensors="pt", truncation=True, padding=True)

    # Generate the summary ids
    summary_ids = model_bart.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decode the summary
    summary = tokenizer_bart.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# 2. Using deepseek-llm-67b-base. This is requiring way too much storage space. So better keep this code commented guys
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# # Load the model and tokenizer
# model_name = "deepseek-ai/deepseek-llm-67b-base"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")

# # Configure generation settings
# model.generation_config = GenerationConfig.from_pretrained(model_name)
# model.generation_config.pad_token_id = model.generation_config.eos_token_id

# # Function to summarize text using the deepseek model
# def summarize_text(text: str, max_length: int = 150, min_length: int = 50) -> str:
#     # Tokenize the input text
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=1024)

#     # Generate the summary
#     outputs = model.generate(
#         **inputs.to(model.device),
#         max_new_tokens=max_length,
#         min_new_tokens=min_length,
#         length_penalty=2.0,
#         num_beams=4,
#         early_stopping=True
#     )

#     # Decode the summary
#     summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return summary

# 3. Using T5
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

# Just for testing! But this is preferably what you should be using when developing the project.
# def summarize_text(text: str) -> str:
#     summary = """
#     This is the summarized text.

#     AI summarizing models are not loaded to save time in starting the server. This is only for testing during prototyping.

#     If this issue persists, contact Mr. Sarthak.
#     """
#     return summary

if __name__ == "__main__":
    text_to_summarize = 'Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem-solving".'
    # summary_bart = summarize_text_bart(text_to_summarize)
    # summary_normal = summarize_text(text_to_summarize)
    # summary_t5 = summarize_text_t5(text_to_summarize)

    # print("Summary using BART:", summary_bart)
    # print("Summary using T5:", summary_t5)
    # print("Summary text:", summary_normal)
