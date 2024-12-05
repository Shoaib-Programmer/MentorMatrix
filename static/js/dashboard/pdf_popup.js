document.addEventListener("DOMContentLoaded", function () {
    const pdfOption = document.querySelector(".pdf_upload-option-btn");
    if (pdfOption) {
        pdfOption.addEventListener("click", openPdfPopup);
    } else {
        console.warn("PDF upload button not found.");
    }
});

function openPdfPopup(event) {
    event.preventDefault();

    // Prevent opening the popup if it's already open
    if (document.getElementById("pdf-popup-overlay")) {
        return;
    }

    // Create overlay
    const overlay = document.createElement("div");
    overlay.id = "pdf-popup-overlay";

    // Close popup when clicking outside of it
    overlay.addEventListener("click", function (event) {
        if (event.target === overlay) {
            document.body.removeChild(overlay);
        }
    });

    // Create popup container
    const popup = document.createElement("div");
    popup.id = "pdf-popup-container";

    // Create form elements
    const title = document.createElement("h3");
    title.innerText = "Upload a PDF File";

    const pdfInput = document.createElement("input");
    pdfInput.type = "file";
    pdfInput.accept = "application/pdf";

    const uploadButton = document.createElement("button");
    uploadButton.id = "pdf-upload-button";
    uploadButton.innerText = "Upload PDF";
    uploadButton.disabled = true; // Disabled by default until a file is selected

    let selectedPdfFile = null;

    // Handle file selection
    pdfInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file && file.type === "application/pdf") {
            selectedPdfFile = file;
            uploadButton.disabled = false; // Enable upload button
            console.log("Selected PDF file:", file.name);
        } else {
            alert("Please select a valid PDF file.");
        }
    });

    // Handle PDF upload
    uploadButton.addEventListener("click", async function () {
        if (!selectedPdfFile) {
            alert("No PDF file selected!");
            return;
        }

        const formData = new FormData();
        formData.append("pdf", selectedPdfFile);

        try {
            console.log("Uploading PDF...");

            await fetch("/upload_pdf", {
                method: "POST",
                body: formData,
            });

            // Redirecting logic handled by the server; no further action needed.
            console.log("Upload request sent. Redirecting handled by the server.");
        } catch (error) {
            console.error("Upload error:", error);
            alert("An error occurred during upload. Please try again.");
        } finally {
            if (document.body.contains(overlay)) {
                document.body.removeChild(overlay);
            }
        }
    });


    // Append elements to popup container
    popup.appendChild(title);
    popup.appendChild(pdfInput);
    popup.appendChild(uploadButton);

    // Append popup container to overlay
    overlay.appendChild(popup);

    // Append overlay to body
    document.body.appendChild(overlay);
}
