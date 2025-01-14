// Function to toggle the YouTube modal
function toggleYoutubePopup(show) {
  const youtubePopup = document.getElementById("youtube-popup");
  if (!youtubePopup) {
    console.error("YouTube popup element not found!");
    return;
  }

  if (show) {
    youtubePopup.classList.remove("hidden");
  } else {
    youtubePopup.classList.add("hidden");
  }
}

// Add event listener to the YouTube button
document.addEventListener("DOMContentLoaded", () => {
  const youtubeButton = document.querySelector(".youtube_upload-option-btn");
  if (youtubeButton) {
    youtubeButton.addEventListener("click", () => toggleYoutubePopup(true));
  } else {
    console.error("YouTube button not found!");
  }

  // Close button logic
  const closeButton = document.querySelector("#youtube-popup .close-btn");
  if (closeButton) {
    closeButton.addEventListener("click", () => toggleYoutubePopup(false));
  } else {
    console.error("Close button in YouTube popup not found!");
  }

  // Submit YouTube URL for processing
  const submitButton = document.getElementById("submit-youtube-button");
  if (submitButton) {
    submitButton.addEventListener("click", async () => {
      const youtubeUrlInput = document.getElementById("youtube-url");
      const youtubeUrl = youtubeUrlInput ? youtubeUrlInput.value.trim() : "";

      if (!youtubeUrl) {
        alert("Please enter a valid YouTube URL.");
        return;
      }

      try {
        console.log("Submitting YouTube URL:", youtubeUrl);

        // Make a POST request to the server with the YouTube URL
        const response = await fetch("/upload_youtube", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ youtube_url: youtubeUrl }),
        });

        if (response.redirected) {
          // Redirect to the URL provided by the server
          window.location.href = response.url;
        } else if (response.ok) {
          alert("YouTube video submitted successfully.");
          toggleYoutubePopup(false);
        } else {
          console.error("Server error:", response.statusText);
          alert(
            "An error occurred while processing the YouTube video. Please try again."
          );
        }
      } catch (error) {
        console.error("Error submitting YouTube URL:", error);
        alert("An error occurred. Please check your connection and try again.");
      }
    });
  } else {
    console.error("Submit button in YouTube popup not found!");
  }
});
