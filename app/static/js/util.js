// util.js

// JavaScript function to handle redirects
function redirectToPage(url) {
    window.location.href = url;
}

// JavaScript function to handle flash message disappearance after 5 seconds
window.addEventListener('DOMContentLoaded', (event) => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach((message) => {
        // After 5 seconds, the message will fade out and be removed
        setTimeout(() => {
            message.classList.add('opacity-0');
            message.style.transition = 'opacity 0.5s ease-out'; // For smooth disappearance
            setTimeout(() => {
                message.remove(); // Remove the message from the DOM
            }, 500); // Delay for opacity transition
        }, 5000); // Message disappears after 5 seconds
    });
});

import { Clerk } from '@clerk/clerk-js';

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
const clerk = new Clerk(clerkPubKey);

clerk.load().then(() => {
  // Check if the user is signed in
  if (clerk.user) {
    // If signed in, you can mount a user button (for account management)
    const userButtonContainer = document.getElementById('user-button');
    if (userButtonContainer) {
      clerk.mountUserButton(userButtonContainer);
    }
  } else {
    // If not signed in, mount a sign-in widget instead
    const signInContainer = document.getElementById('sign-in');
    if (signInContainer) {
      clerk.mountSignIn(signInContainer);
    }
  }
});

