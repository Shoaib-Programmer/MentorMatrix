// Function to open transcript popup
function openTranscriptPopup(transcriptText) {
  const overlay = document.createElement("div");
  overlay.id = "transcript-popup-overlay";
  overlay.style.position = "fixed";
  overlay.style.top = 0;
  overlay.style.left = 0;
  overlay.style.width = "100vw";
  overlay.style.height = "100vh";
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
  overlay.style.display = "flex";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.zIndex = 1000;

  const popup = document.createElement("div");
  popup.id = "transcript-popup-container";
  popup.style.width = "80%";
  popup.style.maxHeight = "80vh";
  popup.style.overflowY = "auto";
  popup.style.padding = "20px";
  popup.style.backgroundColor = "#ffffff";
  popup.style.borderRadius = "10px";
  popup.style.color = "#333333";

  const closeButton = document.createElement("button");
  closeButton.innerText = "Close";
  closeButton.onclick = () => document.body.removeChild(overlay);

  const transcriptContent = document.createElement("div");
  transcriptContent.innerText = transcriptText; // Replace with the actual transcript content

  popup.appendChild(transcriptContent);
  popup.appendChild(closeButton);
  overlay.appendChild(popup);
  document.body.appendChild(overlay);
}
