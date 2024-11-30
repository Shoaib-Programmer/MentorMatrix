# 1. DialogGPT-large
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# Load the model and tokenizer
# model_name = "microsoft/DialoGPT-large"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# Function to chat with the model
# def chat(user_message, chat_history=None):
#     # Encode the new user input, add the eos_token and return a tensor
#     new_user_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

#     # Append the new user input to the chat history (if it exists)
#     if chat_history is None:
#         chat_history = new_user_input_ids
#     else:
#         chat_history = torch.cat([chat_history, new_user_input_ids], dim=-1)

#     # Generate a response from the model
#     response_ids = model.generate(chat_history, max_length=1000, pad_token_id=tokenizer.eos_token_id)

#     # Get the predicted response and decode it
#     bot_response = tokenizer.decode(response_ids[:, chat_history.shape[-1]:][0], skip_special_tokens=True)

#     return bot_response, chat_history


# Just for prototyping! But this is probably what you should be using during development as it saves time in starting the server
def chat(user_message, chat_history=None):
    return 'This is the AI\'s response. AI models are not loaded to save time in starting the server during prototyping. If this issue persists, please contact Mr. Vihaan Reddy.', chat_history