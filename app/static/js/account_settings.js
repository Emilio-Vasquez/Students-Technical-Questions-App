document.addEventListener("DOMContentLoaded", function() {
    const togglePasswordBtn = document.getElementById("toggle-password-btn");
    const passwordForm = document.getElementById("password-form");
    togglePasswordBtn.addEventListener("click", () => {
        passwordForm.classList.toggle("visible");
    });

    const togglePhoneBtn = document.getElementById("toggle-phone-btn");
    const phoneForm = document.getElementById("phone-form");
    togglePhoneBtn.addEventListener("click", () => {
        phoneForm.classList.toggle("visible");
    });

    const verifyEmailBtn = document.getElementById("verify-email-btn");
    verifyEmailBtn.addEventListener("click", () => {
        alert("A verification email would be sent here (logic to implement).");
    });
});