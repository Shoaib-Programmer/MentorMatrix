// Function to flip flashcards
function flipCard(index) {
  const flashcard = document.getElementById(`flashcard-${index}`);
  const front = flashcard.querySelector('.flashcard-front');
  const back = flashcard.querySelector('.flashcard-back');

  // Toggle visibility
  if (front.style.display === "block") {
    front.style.display = "none";
    back.style.display = "block";
  } else {
    front.style.display = "block";
    back.style.display = "none";
  }
}

// Modal functionality
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("myModal");
  const openModalBtn = document.getElementById("openModalBtn");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const closeModalXBtn = document.querySelector(".close-btn");

  // Open modal
  openModalBtn?.addEventListener("click", () => {
    modal.style.display = "flex";
  });

  // Close modal on 'Cancel' button or 'X' button
  closeModalBtn?.addEventListener("click", closeModal);
  closeModalXBtn?.addEventListener("click", closeModal);

  // Close modal when clicking outside of it
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal();
    }
  });

  // Function to close modal
  function closeModal() {
    modal.style.display = "none";
  }

  // Handle deck selection change (Form submit)
  const deckSelect = document.getElementById("deck-select");
  if (deckSelect) {
    deckSelect.addEventListener("change", () => {
      // Submit the form automatically when deck is changed
      deckSelect.closest("form").submit();
    });
  }
});

// Keyboard accessibility for modal (ESC to close)
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    const modal = document.getElementById("myModal");
    if (modal && modal.style.display === "flex") {
      modal.style.display = "none";
    }
  }
});
