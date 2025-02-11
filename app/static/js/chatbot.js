document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('input');
    const sendButton = document.getElementById('send-button');
    const intro = document.getElementById('intro');
    const messages = document.getElementById('messages');

    // Event listener for "Enter" key press in the input field
    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) { // Check if Enter is pressed, not Shift + Enter
            event.preventDefault(); // Prevent default behavior (form submit or line break)
            sendMessage(); // Trigger the send message functionality
        }
    });

    // Event listener for the send button click
    sendButton.addEventListener('click', function () {
        sendMessage(); // Trigger the send message functionality
    });

    function sendMessage() {
        // Hide intro text when the user sends a message
        if (intro) {
            intro.style.display = 'none';
            messages.style.paddingTop = '1rem'; // Adjust padding after intro hides
        }

        const userMessage = input.value.trim();
        if (userMessage) {
            // Display the user's message
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'message user';
            userMessageDiv.textContent = userMessage;
            messages.appendChild(userMessageDiv);

            input.value = ''; // Clear the input field
            messages.scrollTop = messages.scrollHeight; // Scroll to the latest message

            // Send the user's message to the backend
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage })
            })
                .then(response => response.json())
                .then(data => {
                    // Display the bot's response (use innerHTML to render HTML properly)
                    const botMessageDiv = document.createElement('div');
                    botMessageDiv.className = 'message bot';
                    botMessageDiv.innerHTML = data.response; // Use innerHTML to render HTML

                    messages.appendChild(botMessageDiv);

                    messages.scrollTop = messages.scrollHeight; // Scroll to the latest message
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }
});
