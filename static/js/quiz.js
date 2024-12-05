// Modal functionality
document.getElementById("closeModalBtn").addEventListener("click", function () {
  document.getElementById("myModal").style.display = "none";
});
document.querySelector(".close-btn").addEventListener("click", function () {
  document.getElementById("myModal").style.display = "none";
});

document.querySelectorAll('.hint-btn').forEach(button => {
    button.addEventListener('click', toggleHint);
});

// Open the modal
function openModal() {
  document.getElementById("myModal").style.display = "flex";
}

// Toggle hint display
function toggleHint(index, type = '') {
    const hint = document.getElementById(`${type ? type + '-' : ''}hint-${index}`);
    if (hint) {
        hint.style.display = hint.style.display === "none" ? "block" : "none";
    } else {
        console.error("Hint element not found.");
    }
}

// Functions to manage quiz sessions
function startNewSession() {
    fetch("/start_session", { method: "POST" })
      .then(response => {
        if (!response.ok) throw new Error("Failed to start a new session.");
        return response.json();
      })
      .then(data => {
        if (data.success) {
          location.reload(); // Reload the page to update the UI
        } else {
          alert("Error starting session: " + (data.message || "Unknown error."));
        }
      })
      .catch(error => {
        console.error(error);
        alert("An error occurred while starting a new session.");
      });
    openModal(); // Show the modal after starting the session
}

function resumeSession() {
  location.href = "/quiz";
}

function endSession() {
  fetch("/end_session", { method: "POST" })
      .then(response => {
          if (!response.ok) throw new Error("Failed to end session.");
          return response.json();
      })
      .then(data => {
          if (data.success) {
              location.reload();
          } else {
              alert("Error ending session: " + (data.message || "Unknown error."));
          }
      })
      .catch(error => {
          console.error(error);
          alert("An error occurred while ending the session.");
      });
}

// Handle form submission for adding new questions
document.querySelector("#myModal form").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission

  const formData = new FormData(this);
  fetch("/add_question", {
      method: "POST",
      body: formData
  })
      .then(response => {
          if (!response.ok) throw new Error("Failed to add question.");
          return response.json();
      })
      .then(data => {
          if (data.success) {
              alert("Question added successfully!");
              document.getElementById("myModal").style.display = "none";
              location.reload();
          } else {
              alert("Error adding question: " + (data.message || "Unknown error."));
          }
      })
      .catch(error => {
          console.error(error);
          alert("An error occurred while adding the question.");
      });
});

// Helper to close the modal on outside click
window.onclick = function (event) {
  const modal = document.getElementById("myModal");
  if (event.target === modal) {
      modal.style.display = "none";
  }
};
