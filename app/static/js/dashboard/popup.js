document.addEventListener('DOMContentLoaded', function() {
    // Modal handling
    function showModal(modalType) {
        document.querySelector(`.popup-overlay[data-modal-type="${modalType}"]`)?.classList.remove('hidden');
    }

    function hideModal(modalType) {
        document.querySelector(`.popup-overlay[data-modal-type="${modalType}"]`)?.classList.add('hidden');
    }

    function hideAllModals() {
        document.querySelectorAll('.popup-overlay').forEach(modal => {
            modal.classList.add('hidden');
        });
    }

    // Initialize - ensure all modals are hidden on page load
    hideAllModals();

    // Setup open button handlers
    document.querySelectorAll('.upload-option-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const modalType = button.dataset.modalType;
            if (modalType) {
                showModal(modalType);
            }
        });
    });

    // Setup close button handlers
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.popup-overlay');
            const modalType = modal.dataset.modalType;
            if (modalType) {
                hideModal(modalType);
            }
        });
    });

    // Close on outside click
    document.querySelectorAll('.popup-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                const modalType = overlay.dataset.modalType;
                if (modalType) {
                    hideModal(modalType);
                }
            }
        });
    });

    // Progress bar handling
    function updateProgress(percent) {
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');
        
        progressContainer.classList.remove('hidden');
        progressBar.style.width = `${percent}%`;
        progressBar.textContent = `${Math.round(percent)}%`;
        
        if (percent >= 100) {
            setTimeout(() => progressContainer.classList.add('hidden'), 1000);
        }
    }

    // Show error message
    function showError(message) {
        alert(message); // Replace with a better UI notification system if needed
    }

    // Rest of your existing handlers for audio, YouTube, and PDF functionality

    //
    // AUDIO POPUP SETUP
    //
    const audioInput = document.getElementById("audio-input");
    const recordButton = document.getElementById("record-button");
    const uploadButton = document.getElementById("upload-button");
    const audioPlayer = document.getElementById("audio-player");

    let recording = false;
    let mediaRecorder;
    let chunks = [];
    let uploadedAudioBlob;

    if (audioInput) {
        // Handle file upload manually; enable the upload button when a file is chosen
        audioInput.addEventListener("change", (event) => {
            const file = event.target.files[0];
            if (file) {
                uploadedAudioBlob = file;
                uploadButton.disabled = false;
                console.log("Uploaded audio file:", file.name);
            }
        });
    }

    if (recordButton) {
        recordButton.addEventListener("click", async () => {
            if (!recording) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.start();
                    recording = true;
                    recordButton.textContent = "Stop Recording";

                    mediaRecorder.addEventListener("dataavailable", (e) => {
                        chunks.push(e.data);
                    });

                    mediaRecorder.addEventListener("stop", () => {
                        const blob = new Blob(chunks, { type: "audio/mp3" });
                        audioPlayer.src = URL.createObjectURL(blob);
                        audioPlayer.classList.remove("hidden");
                        uploadButton.disabled = false;
                        // Store the recording for uploading
                        uploadedAudioBlob = blob;
                        chunks = [];
                    });
                } catch (err) {
                    console.error("Error starting recording: ", err);
                    alert("Error starting recording.");
                }
            } else {
                mediaRecorder.stop();
                recording = false;
                recordButton.textContent = "Start Recording";
            }
        });
    }

    if (uploadButton) {
        uploadButton.addEventListener("click", async () => {
            if (!uploadedAudioBlob) {
                showError("No audio file selected");
                return;
            }

            const formData = new FormData();
            formData.append('audio', uploadedAudioBlob);

            try {
                updateProgress(0);
                const response = await fetch("/upload_audio", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: formData,
                });
                

                if (response.redirected) {
                    window.location.href = response.url;
                } else if (response.ok) {
                    const data = await response.json();
                    if (data.error) {
                        showError(data.error);
                    } else {
                        hideModal('audio');
                        updateProgress(100);
                    }
                } else {
                    showError("Failed to upload audio");
                }
            } catch (error) {
                console.error("Error:", error);
                showError("An error occurred while uploading");
            }
        });
    }

    //
    // YOUTUBE POPUP SETUP
    //
    const submitYoutubeButton = document.getElementById("submit-youtube-button");
    if (submitYoutubeButton) {
        submitYoutubeButton.addEventListener("click", async () => {
            const youtubeUrlInput = document.getElementById("youtube-url");
            const youtubeUrl = youtubeUrlInput ? youtubeUrlInput.value.trim() : "";
            
            if (!youtubeUrl) {
                showError("Please enter a valid YouTube URL");
                return;
            }

            try {
                updateProgress(20);
                const response = await fetch("/upload_youtube", {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content 
                    },
                    body: JSON.stringify({ youtube_url: youtubeUrl })
                });

                updateProgress(60);

                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    showError("Error processing YouTube URL");
                }
            } catch (error) {
                console.error("Error:", error);
                showError("Failed to process YouTube URL");
            }
        });
    }

    //
    // PDF POPUP SETUP
    //
    const submitPdfButton = document.getElementById("submit-pdf-button");
    if (submitPdfButton) {
        submitPdfButton.addEventListener("click", async () => {
            const pdfInput = document.getElementById("pdf-input");
            if (!pdfInput || !pdfInput.files.length) {
                showError("Please select a PDF file");
                return;
            }

            const formData = new FormData();
            formData.append('pdf', pdfInput.files[0]);

            try {
                updateProgress(20);
                const response = await fetch("/upload_pdf", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: formData
                });

                updateProgress(60);

                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    const data = await response.json();
                    if (data.error) {
                        showError(data.error);
                    } else {
                        hideModal('pdf');
                        updateProgress(100);
                    }
                }
            } catch (error) {
                console.error("Error:", error);
                showError("Failed to upload PDF");
            }
        });
    }

    // Handle file upload progress
    function uploadWithProgress(url, formData) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener("progress", (e) => {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    updateProgress(percentComplete);
                }
            });

            xhr.addEventListener("load", () => resolve(xhr));
            xhr.addEventListener("error", () => reject(xhr));
            
            xhr.open("POST", url);
            xhr.setRequestHeader("X-CSRFToken", document.querySelector('meta[name="csrf-token"]').content);
            xhr.send(formData);
        });
    }
});