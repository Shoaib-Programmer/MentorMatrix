// Toggle Modal Visibility
function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.toggle("hidden");
    }
}

function toggleAudioPopup(show) {
    const modal = document.getElementById("audio-popup");
    if (!modal) {
        console.error("Audio popup modal not found!");
        return;
    }

    if (show) {
        modal.classList.remove("hidden"); // Show the popup
    } else {
        modal.classList.add("hidden"); // Hide the popup
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const audioInput = document.getElementById("audio-input");
    const recordButton = document.getElementById("record-button");
    const uploadButton = document.getElementById("upload-button");
    const mainContent = document.getElementById("main-content");
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const audioPlayer = document.getElementById("audio-player");

    let recording = false;
    let mediaRecorder;
    let chunks = [];
    let uploadedAudioBlob;

    // Handle File Upload
    audioInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadedAudioBlob = file;
            uploadButton.disabled = false;
            console.log("Uploaded audio file:", file.name);
        }
    });

    // Handle Recording
    recordButton.addEventListener("click", async () => {
        if (!recording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = (event) => {
                    chunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(chunks, {
                        type: "audio/wav",
                    });
                    uploadedAudioBlob = audioBlob;
                    const audioUrl = URL.createObjectURL(audioBlob);

                    audioPlayer.src = audioUrl;
                    audioPlayer.classList.remove("hidden");
                    uploadButton.disabled = false;
                };

                mediaRecorder.start();
                recording = true;
                recordButton.innerText = "Stop Recording";
            } catch (error) {
                console.error("Recording failed:", error);
                alert("Could not access microphone. Please check permissions.");
            }
        } else {
            mediaRecorder.stop();
            recording = false;
            recordButton.innerText = "Start Recording";
        }
    });

    // Handle Audio Upload
    uploadButton.addEventListener("click", async () => {
        if (!uploadedAudioBlob) {
            alert("No audio file selected or recorded!");
            return;
        }

        progressContainer.style.display = "flex";
        progressBar.style.width = "0%";
        progressBar.textContent = "0%";
        mainContent.style.display = "none";

        const formData = new FormData();
        formData.append("audio", uploadedAudioBlob);

        let progress = 0;
        const maxProgress = 90;
        const progressInterval = setInterval(() => {
            if (progress < maxProgress) {
                progress += 1;
                progressBar.style.width = `${progress}%`;
                progressBar.textContent = `${progress}%`;

                // Slow down the animation as it approaches maxProgress
                if (progress >= maxProgress - 20) {
                    clearInterval(progressInterval);
                    setTimeout(() => {
                        const newInterval = setInterval(() => {
                            if (progress < maxProgress) {
                                progress += 0.5;  // Slower increment
                                progressBar.style.width = `${progress}%`;
                                progressBar.textContent = `${progress}%`;
                            }
                        }, 1000);  // Slower update interval
                    }, 500);  // Delay before slowing down
                }
            }
        }, 100);  // Initial fast update interval

        try {
            console.log("Uploading audio...");

            // Send the audio file to the server
            const response = await fetch("/upload_audio", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Upload failed");
            }

            console.log("Audio uploaded successfully.");
            clearInterval(progressInterval);
            progressBar.style.width = "100%";
            progressBar.textContent = "100%";

            finishUpload();

        } catch (error) {
            console.error("Upload error:", error);
            clearInterval(progressInterval);
            alert("An error occurred during upload. Please try again.");
            finishUpload();
        }
    });

    function finishUpload() {
        setTimeout(() => {
            alert("Notes complete!");
            window.location.href = "/notes";
        }, 500);
    }
});
