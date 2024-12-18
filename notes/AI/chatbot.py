# # 1. DialogGPT-large
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# # Load the Llama 3 model and tokenizer
# model_name = "ollama/llama3"  # Replace with the correct model name if different
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

import subprocess
from icecream import ic

def chat(user_input, chat_history=None):
    # Initialize chat history if it's None
    if chat_history is None:
        chat_history = ""

    # Append user input to chat history
    chat_history += f"You: {user_input}\n"

    # Run the ollama command and pass the chat history
    process = subprocess.Popen(
        ['ollama', 'run', 'llama3'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send the chat history to the process
    output, error = process.communicate(input=chat_history)

    ic(output.strip())

    # Return the output from the model and the updated chat history
    return output.strip(), chat_history

if __name__ == "__main__":
    print("Chat with Llama 3! Type '/bye' to exit.")
    chat_history = None  # Initialize chat history
    while True:
        user_input = input("You: ")
        if user_input.lower() == "/bye":
            print("Ending chat.")
            break
        
        # Get the response from Llama 3
        response, chat_history = chat(user_input, chat_history)
        
        # Append bot response to chat history
        chat_history += f"Llama 3: {response}\n"
        
        print(f"Llama 3: {response}")

# # Example usage
# if __name__ == "__main__":
#     chat_history = None
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             break
#         response, chat_history = chat(user_input, chat_history)
#         print(f"Bot: {response}")

# # import openai
# import os
# from dotenv import load_dotenv
# # Set up your OpenAI API key
# api_key = os.getenv("OPENAI_API_KEY")

# openai.api_key = api_key

# # Function to chat with OpenAI's ChatCompletion endpoint
# def chat(user_message, chat_history=None):
#     # Prepare the chat history
#     if chat_history is None:
#         chat_history = []
    
#     # Add the user's message to the chat history
#     chat_history.append({"role": "user", "content": user_message})

#     # Call the OpenAI API
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",  # Use "gpt-4" if needed
#         messages=chat_history
#     )

#     # Get the assistant's response
#     bot_response = response["choices"][0]["message"]["content"]

#     # Append the assistant's response to the chat history
#     chat_history.append({"role": "assistant", "content": bot_response})

#     return bot_response, chat_history

# # Example usage
# if __name__ == "__main__":
#     chat_history = None
#     while True:
#         user_message = input("You: ")
#         if user_message.lower() in {"exit", "quit"}:
#             break
#         response, chat_history = chat(user_message, chat_history)
#         print(f"Bot: {response}")

# Just for prototyping! But this is probably what you should be using during development as it saves time in starting the server
# def chat(user_message, chat_history=None):
#     return 'This is the AI\'s response. AI models are not loaded to save time in starting the server during prototyping. If this issue persists, please contact Mr. Vihaan Reddy.', chat_history
