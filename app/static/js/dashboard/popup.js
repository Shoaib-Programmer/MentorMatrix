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
        uploadButton.addEventListener("click", () => {
            if (uploadedAudioBlob) {
                // Process the audio upload.
                // For example, you may use fetch or XMLHttpRequest to send the blob.
                // Here we simulate a successful upload.
                alert("Audio uploaded successfully!");
                hideModal('audio');
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
                alert("Please enter a valid YouTube URL.");
                return;
            }

            try {
                const response = await fetch("/upload_youtube", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ youtube_url: youtubeUrl })
                });

                if (response.ok) {
                    alert("YouTube video submitted successfully!");
                    hideModal('youtube');
                } else {
                    alert("Error processing YouTube URL. Please try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
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
                alert("Please select a PDF file.");
                return;
            }

            try {
                const formData = new FormData();
                formData.append('pdf', pdfInput.files[0]);

                const response = await fetch("/upload_pdf", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    alert("PDF uploaded successfully!");
                    hideModal('pdf');
                } else {
                    alert("Error uploading PDF. Please try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            }
        });
    }
});