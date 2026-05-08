document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-upload-btn");
    const uploadSection = document.getElementById("upload-section");

    if (!toggleButton || !uploadSection) {
        return;
    }

    toggleButton.addEventListener("click", function () {
        const isHidden =
            window.getComputedStyle(uploadSection).display === "none";

        if (isHidden) {
            uploadSection.style.display = "block";

            uploadSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        } else {
            uploadSection.style.display = "none";
        }
    });
});