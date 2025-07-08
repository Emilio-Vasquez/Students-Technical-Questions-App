document.addEventListener("DOMContentLoaded", function () {
    const togglePasswordBtn = document.getElementById("toggle-password-btn");
    const passwordForm = document.getElementById("password-form");
    if (togglePasswordBtn && passwordForm) {
        togglePasswordBtn.addEventListener("click", () => {
            passwordForm.classList.toggle("visible");
        });
    }

    const togglePhoneBtn = document.getElementById("toggle-phone-btn");
    const phoneForm = document.getElementById("phone-form");
    if (togglePhoneBtn && phoneForm) {
        togglePhoneBtn.addEventListener("click", () => {
            phoneForm.classList.toggle("visible");
        });
    }

    const sendCodeForm = document.getElementById("send-code-form");
    const codeEntryDiv = document.getElementById("code-entry");

    // If the code was already requested and page reloaded, show it
    if (localStorage.getItem("showCodeEntry") === "true") {
        if (codeEntryDiv) {
            codeEntryDiv.style.display = "block";
        }
        localStorage.removeItem("showCodeEntry");
    }

    // Set flag to show input on next page load
    if (sendCodeForm) {
        sendCodeForm.addEventListener("submit", function () {
            localStorage.setItem("showCodeEntry", "true");
        });
    }
});
