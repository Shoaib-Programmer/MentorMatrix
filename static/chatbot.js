document.getElementById('input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) { // Check if Enter is pressed, not Shift + Enter
        event.preventDefault(); // Prevent default behavior (form submit or line break)
        sendMessage(); // Trigger the send message functionality
    }
});

function sendMessage() {
    const intro = document.getElementById('intro');
    const messages = document.getElementById('messages');
    const input = document.getElementById('input');

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

        // Add a horizontal rule after user's message
        // const hr = document.createElement('hr');
        // hr.className = 'my-2';
        // messages.appendChild(hr);

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
                // Display the bot's response
                const botMessageDiv = document.createElement('div');
                botMessageDiv.className = 'message bot';
                botMessageDiv.textContent = data.response;
                messages.appendChild(botMessageDiv);

                // Add a horizontal rule after bot's response
                // const hr = document.createElement('hr');
                // hr.className = 'my-2';
                // messages.appendChild(hr);

                messages.scrollTop = messages.scrollHeight; // Scroll to the latest message
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}
