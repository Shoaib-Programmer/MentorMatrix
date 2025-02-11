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
