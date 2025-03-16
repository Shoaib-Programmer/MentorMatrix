export function initializeProgressBar() {
  const progressContainer = document.getElementById("progress-container");
  const progressBar = document.getElementById("progress-bar");
  let progressInterval;

  function startProgress() {
    progressContainer.style.display = "flex";
    progressBar.style.width = "0%";
    progressBar.textContent = "0%";
    let progress = 0;
    const maxProgress = 90;

    progressInterval = setInterval(() => {
      if (progress < maxProgress) {
        progress += 1;
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;

        if (progress >= maxProgress - 20) {
          clearInterval(progressInterval);
          setTimeout(() => {
            progressInterval = setInterval(() => {
              if (progress < maxProgress) {
                progress += 0.5;
                progressBar.style.width = `${progress}%`;
                progressBar.textContent = `${progress}%`;
              }
            }, 1000);
          }, 500);
        }
      }
    }, 100);
  }

  function completeProgress() {
    clearInterval(progressInterval);
    progressBar.style.width = "100%";
    progressBar.textContent = "100%";
  }

  return { startProgress, completeProgress };
}
