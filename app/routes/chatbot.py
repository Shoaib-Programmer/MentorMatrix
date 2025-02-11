from flask import Blueprint, render_template, request, jsonify
from notes import chat
from icecream import ic
import markdown

# Define the chatbot blueprint
chatbot_blueprint = Blueprint('chatbot', __name__)

# Initialize chat history
chat_history = None

# Route to render the chatbot page
@chatbot_blueprint.route('/chatbot')
def chatbot():
    return render_template('chatbot.html', current_route='chatbot')

# Route to handle the user's message (POST request)
@chatbot_blueprint.route('/chat', methods=['POST'])
def chat_route():
    global chat_history  # Use the global chat history variable

    # Get the user's message from the request data
    data = request.get_json()
    user_message = data.get('message')

    # Process the message and get the bot's response
    response_message, chat_history = chat(user_message, chat_history)


    # Convert the bot's Markdown response to HTML
    response_html = markdown.markdown(response_message)

    # Return the response as JSON, including the user's message and the rendered HTML
    return jsonify({
        "user_message": user_message,
        "response": response_html  # Send the HTML version of the response
    })
