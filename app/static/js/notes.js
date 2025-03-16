document.getElementById("openModalBtn")?.addEventListener("click", function () {
  const modal = document.getElementById("myModal");
  modal.style.display = "flex"; // Display the modal
  setTimeout(() => {
    modal.classList.add("show"); // Apply the 'show' class for animation
  }, 10); // Small delay to ensure the modal is visible first
});

document
  .getElementById("closeModalBtn")
  ?.addEventListener("click", function () {
    const modal = document.getElementById("myModal");
    modal.classList.remove("show"); // Remove the 'show' class for the fade-out effect
    setTimeout(() => {
      modal.style.display = "none"; // Hide the modal after animation
    }, 300); // Delay to match the duration of the fade-out transition
  });

document.querySelector(".close-btn")?.addEventListener("click", function () {
  const modal = document.getElementById("myModal");
  modal.classList.remove("show");
  setTimeout(() => {
    modal.style.display = "none";
  }, 300);
});
