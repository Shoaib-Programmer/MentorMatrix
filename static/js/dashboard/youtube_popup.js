// Function to toggle the YouTube modal
function toggleYoutubePopup(show) {
    const youtubePopup = document.getElementById("youtube-popup");
    if (show) {
        youtubePopup.classList.add("active"); // Use 'active' instead of 'hidden'
    } else {
        youtubePopup.classList.remove("active");
    }
}

// Add event listener to the YouTube button
document.querySelector(".youtube_upload-option-btn").addEventListener("click", function () {
    toggleYoutubePopup(true);
});

// Close button logic
document.querySelector("#youtube-popup .close-btn").addEventListener("click", function () {
    toggleYoutubePopup(false);
});

// Submit YouTube URL for transcription
document.getElementById("submit-youtube-button").addEventListener("click", function () {
    const youtubeUrl = document.getElementById("youtube-url").value.trim();
    if (!youtubeUrl) {
        alert("Please enter a valid YouTube URL.");
        return;
    }

    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");
    const transcriptContainer = document.getElementById("transcript-container");
    const transcriptText = document.getElementById("transcript-text");

    // Reset previous progress and transcript UI
    progressBar.value = 0;
    transcriptContainer.classList.add("hidden");
    transcriptText.textContent = "";

    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource(`/upload_audio?youtube_url=${encodeURIComponent(youtubeUrl)}`);

    eventSource.onmessage = function (event) {
        const data = JSON.parse(event.data);

        // Update progress
        if (data.progress !== undefined) {
            progressBar.value = data.progress;
        }

        // Display transcript
        if (data.transcript) {
            transcriptContainer.classList.remove("hidden");
            transcriptText.textContent = data.transcript;
            eventSource.close();
        }

        // Handle errors
        if (data.error) {
            alert(`Error: ${data.error}`);
            eventSource.close();
        }
    };

    eventSource.onerror = function () {
        alert("An error occurred during transcription.");
        eventSource.close();
    };
});
