  // Modal functionality
  document.getElementById("closeModalBtn").addEventListener("click", function() {
    document.getElementById("myModal").style.display = "none";
  });
  document.querySelector(".close-btn").addEventListener("click", function() {
    document.getElementById("myModal").style.display = "none";
  });

  // Toggle hint display
  function toggleHint(index, type = '') {
    const hint = document.getElementById(`${type ? type + '-' : ''}hint-${index}`);
    hint.style.display = hint.style.display === "none" ? "block" : "none";
  }

  // Functions to manage quiz sessions
  function startNewSession() {
    fetch("/start_session", { method: "POST" })
      .then(response => response.json())
      .then(data => {
        if (data.success) location.reload();
      });
  }

  function resumeSession() {
    location.href = "/quiz";
  }

  function endSession() {
    fetch("/end_session", { method: "POST" })
      .then(response => response.json())
      .then(data => {
        if (data.success) location.reload();
      });
  }
