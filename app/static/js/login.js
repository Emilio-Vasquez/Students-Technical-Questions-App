// This js file is just to not show the submit button, and it toggles show/hide password. And it also adds a small spinner on submit to show loading
document.addEventListener("DOMContentLoaded", function() {
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const submitBtn = document.querySelector("button[type='submit']");
    
    // Create a show/hide password toggle button
    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.textContent = "Show Password";
    toggleBtn.style.marginLeft = "0.5rem";
    password.parentNode.appendChild(toggleBtn);
    
    toggleBtn.addEventListener("click", () => {
        if (password.type === "password") {
            password.type = "text";
            toggleBtn.textContent = "Hide Password";
        } else {
            password.type = "password";
            toggleBtn.textContent = "Show Password";
        }
    });
    
    // Initially disable the submit button
    submitBtn.disabled = true;
    submitBtn.style.opacity = "0.6";
    submitBtn.style.cursor = "not-allowed";
    
    function validateInputs() {
        // Essentially, if the username is less than 4 characters and password is less than 8, the submit button is disabled!!!
        const isUsernameValid = username.value.trim().length >= 4;
        const isPasswordValid = password.value.length >= 8;
        
        if (isUsernameValid && isPasswordValid) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1";
            submitBtn.style.cursor = "pointer";
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.6";
            submitBtn.style.cursor = "not-allowed";
        }
    }
    
    username.addEventListener("input", validateInputs);
    password.addEventListener("input", validateInputs);
    
    // Add spinner to the submit button on form submit
    const form = document.querySelector("form");
    form.addEventListener("submit", function() {
        submitBtn.disabled = true;
        submitBtn.textContent = "Logging in... ⏳";
        submitBtn.style.cursor = "not-allowed";
    });

    const forgotLink = document.getElementById("forgot-password-link");
    if (forgotLink) {
        forgotLink.addEventListener("click", (e) => {
            e.preventDefault();
            alert("Password reset instructions would be sent (feature not implemented yet).");
            // You can later redirect like this:
            // window.location.href = "/forgot_password";
        });
    }
});
