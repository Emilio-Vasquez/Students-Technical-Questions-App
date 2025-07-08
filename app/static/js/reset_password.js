document.addEventListener("DOMContentLoaded", function () {
    const flashMessage = document.querySelector(".flash.danger, .flash.success");
    if (flashMessage) {
        flashMessage.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    const form = document.querySelector("form");
    const newPasswordInput = document.getElementById("new_password");
    const confirmPasswordInput = document.getElementById("confirm_password");

    form.addEventListener("submit", function (e) {
        const newPassword = newPasswordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

        // Reset previous visual warnings
        newPasswordInput.style.border = "";
        confirmPasswordInput.style.border = "";

        // Simple frontend check
        if (newPassword.length < 8 || confirmPassword.length < 8) {
            e.preventDefault();
            alert("Password must be at least 8 characters.");
            newPasswordInput.style.border = "2px solid red";
            confirmPasswordInput.style.border = "2px solid red";
            return;
        }

        if (newPassword !== confirmPassword) {
            e.preventDefault();
            alert("Passwords do not match.");
            newPasswordInput.style.border = "2px solid red";
            confirmPasswordInput.style.border = "2px solid red";
            return;
        }

        // Disable the button to prevent double-clicking
        const submitBtn = form.querySelector("button[type='submit']");
        submitBtn.disabled = true;
        submitBtn.textContent = "Submitting...";
    });
});
