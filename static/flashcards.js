// Function to flip flashcards
function flipCard(index) {
    const flashcard = document.getElementById(`flashcard-${index}`);
    const front = flashcard.querySelector('.flashcard-front');
    const back = flashcard.querySelector('.flashcard-back');
  
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
  
    if (openModalBtn) {
      openModalBtn.addEventListener("click", () => {
        modal.style.display = "flex";
      });
    }
  
    if (closeModalBtn) {
      closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
      });
    }
  
    if (closeModalXBtn) {
      closeModalXBtn.addEventListener("click", () => {
        modal.style.display = "none";
      });
    }
  
    // Close modal when clicking outside of it
    window.addEventListener("click", (event) => {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });
  });

// Modal functionality
document.getElementById("openModalBtn").addEventListener("click", function() {
  document.getElementById("myModal").style.display = "flex";
});

document.getElementById("closeModalBtn").addEventListener("click", function() {
  document.getElementById("myModal").style.display = "none";
});

document.querySelector(".close-btn").addEventListener("click", function() {
  document.getElementById("myModal").style.display = "none";
});
  