document.addEventListener("DOMContentLoaded", function() {
    const youtubeOption = document.querySelector(".youtube_upload-option-btn");
    if (youtubeOption) {
        youtubeOption.addEventListener("click", openYoutubePopup);
    } else {
        console.warn('YouTube upload button not found.');
    }
});

function openYoutubePopup(event) {
    event.preventDefault();

    // Prevent opening the popup if it's already open
    if (document.getElementById("youtube-popup-overlay")) {
        return;
    }

    // Create overlay
    const overlay = document.createElement("div");
    overlay.id = "youtube-popup-overlay";

    // Create popup container
    const popup = document.createElement("div");
    popup.id = "youtube-popup-container";

    // Create form elements
    const title = document.createElement("h3");
    title.innerText = "Add YouTube Video";

    const urlLabel = document.createElement("label");
    urlLabel.for = "youtube-url";
    urlLabel.innerText = "YouTube URL:";

    const urlInput = document.createElement("input");
    urlInput.type = "url";
    urlInput.id = "youtube-url";
    urlInput.placeholder = "Enter YouTube URL";
    urlInput.required = true;

    const submitButton = document.createElement("button");
    submitButton.id = "submit-button";
    submitButton.innerText = "Submit";  // Change button text to "Submit"

    // Progress bar for transcription
    const progressContainer = document.createElement("div");
    progressContainer.id = "progress-container";
    const progressBar = document.createElement("progress");
    progressBar.id = "progress-bar";
    progressBar.max = 100;
    progressBar.value = 0;
    progressContainer.appendChild(progressBar);

    const transcriptContainer = document.createElement("div");
    transcriptContainer.id = "transcript-container";
    transcriptContainer.style.display = "none";  // Hide the transcript initially

    // Function to handle submitting the YouTube URL for transcription
    submitButton.addEventListener("click", function () {
        const youtubeUrl = urlInput.value.trim();

        if (youtubeUrl) {
            // Send GET request to start transcription and stream progress updates
            const eventSource = new EventSource(`/transcribe_youtube?youtube_url=${encodeURIComponent(youtubeUrl)}`);

            eventSource.onmessage = function (event) {
                const data = JSON.parse(event.data);

                // If data contains progress, update the progress bar
                if (data.progress !== undefined) {
                    progressBar.value = data.progress;
                }
                // If data contains transcript, display the full transcript
                else if (data.transcript) {
                    transcriptContainer.innerHTML = `<pre>${data.transcript}</pre>`;
                    transcriptContainer.style.display = "block";
                    eventSource.close();  // Close the EventSource when transcription is done
                }
                // Handle errors if any
                else if (data.error) {
                    console.error("Error in transcription:", data.error);
                    alert("An error occurred while transcribing.");
                    eventSource.close();
                }
            };

            eventSource.onerror = function (error) {
                console.error("Error in EventSource:", error);
                alert("An error occurred while starting transcription.");
            };
        } else {
            alert("Please enter a valid YouTube URL.");
        }
    });

    // Append elements to popup container
    popup.appendChild(title);
    popup.appendChild(urlLabel);
    popup.appendChild(urlInput);
    popup.appendChild(submitButton);
    popup.appendChild(progressContainer);
    popup.appendChild(transcriptContainer);

    // Append popup container to overlay
    overlay.appendChild(popup);

    // Append overlay to body
    document.body.appendChild(overlay);

    // Close the popup when clicking anywhere outside the popup
    overlay.addEventListener("click", function(event) {
        // Check if the click is outside the popup (avoid closing if clicking inside the popup)
        if (event.target === overlay) {
            document.body.removeChild(overlay);
        }
    });
}
