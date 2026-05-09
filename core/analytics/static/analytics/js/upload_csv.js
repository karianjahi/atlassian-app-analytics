document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("upload-form");
    const submitButton = document.getElementById("upload-submit-btn");
    const processingMessage = document.getElementById("processing-message");

    if (!form) {
        return;
    }

    form.addEventListener("submit", function () {
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        processingMessage.classList.remove("hidden");
    });
});