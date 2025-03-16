// util.js

// JavaScript function to handle redirects
function redirectToPage(url) {
  window.location.href = url;
}

// JavaScript function to handle flash message disappearance after 5 seconds
window.addEventListener("DOMContentLoaded", (event) => {
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach((message) => {
    // After 5 seconds, the message will fade out and be removed
    setTimeout(() => {
      message.classList.add("opacity-0");
      message.style.transition = "opacity 0.5s ease-out"; // For smooth disappearance
      setTimeout(() => {
        message.remove(); // Remove the message from the DOM
      }, 500); // Delay for opacity transition
    }, 5000); // Message disappears after 5 seconds
  });
});
