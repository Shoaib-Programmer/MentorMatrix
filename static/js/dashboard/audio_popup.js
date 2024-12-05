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
    const progressMessage = document.getElementById("progress-message");
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

        const formData = new FormData();
        formData.append("audio", uploadedAudioBlob);

        try {
            console.log("Uploading audio...");

            // Send the audio file to the server
            await fetch("/upload_audio", {
                method: "POST",
                body: formData,
            });

            // Let the server handle the redirect after successful upload
            console.log("Audio uploaded successfully. Redirecting handled by the server.");
        } catch (error) {
            console.error("Upload error:", error);
            alert("An error occurred during upload. Please try again.");
        } finally {
            // Reset the UI or give feedback if necessary
            uploadButton.disabled = true; // Disable the upload button to avoid multiple submissions
        }
    });
});
