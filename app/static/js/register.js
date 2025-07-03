document.addEventListener("DOMContentLoaded", function() {
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const confirm = document.getElementById("confirm_password");

    const usernameError = document.getElementById("username-error");
    const emailError = document.getElementById("email-error");
    const passwordError = document.getElementById("password-error");
    const confirmError = document.getElementById("confirm-error");

    // username must have at least 4 characters
    username.addEventListener("input", function() {
        if (username.value.trim().length < 4) {
            usernameError.textContent = "Username must be at least 4 characters.";
            usernameError.className = "error";
            return;
        }

        // Call backend API to check availability
        fetch("/check_username", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username.value.trim() })
        })
        .then(response => response.json())
        .then(data => {
            usernameError.textContent = data.message;
            usernameError.className = data.available ? "success" : "error";
        })
        .catch(() => {
            usernameError.textContent = "Error checking username.";
            usernameError.className = "error";
        });
    });

    // Updated the email validation to be more complex using an emailRegex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    email.addEventListener("input", function() {
        if (!emailRegex.test(email.value)) {
            emailError.textContent = "Enter a valid email (example@example.com).";
            emailError.className = "error";
            return;  // don't call backend if format invalid
        } else {
            emailError.textContent = "Valid email format, checking availability...";
            emailError.className = "info"; // optional: a neutral style while checking

            // Call backend API to check availability
            fetch("/check_email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email.value.trim() })
            })
            .then(response => response.json())
            .then(data => {
                emailError.textContent = data.message;
                emailError.className = data.available ? "success" : "error";
            })
            .catch(() => {
                emailError.textContent = "Error checking email availability.";
                emailError.className = "error";
            });
        }
    });

    // password rules:
    // at least 8 chars, 1 special, 1 digit, no spaces
    password.addEventListener("input", function() {
        const regex = /^(?=.*[0-9])(?=.*[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;
        if (!regex.test(password.value) || password.value.includes(" ")) {
            passwordError.textContent = "Password needs 8+ chars, 1 number, 1 special, no spaces.";
            passwordError.className = "error";
        } else {
            passwordError.textContent = "Valid password";
            passwordError.className = "success";
        }
    });

    // The password confirm must password match with the password given at the top
    confirm.addEventListener("input", function() {
        checkConfirm();
    });

    // confirm check on password field (so changing password triggers confirm re-check)
    password.addEventListener("input", function() {
        checkConfirm();
    });

    // helper function to reduce repetition
    function checkConfirm() {
        if (confirm.value !== password.value) {
            confirmError.textContent = "Passwords do not match.";
            confirmError.className = "error";
        } else {
            confirmError.textContent = "Passwords match";
            confirmError.className = "success";
        }
    }

    // This is to maintain the final check when the user finally submits:
    const form = document.querySelector("form");
    form.addEventListener("submit", function(event) {
        if (
            usernameError.classList.contains("error") ||
            emailError.classList.contains("error") ||
            passwordError.classList.contains("error") ||
            confirmError.classList.contains("error")
        ) {
            event.preventDefault();
            alert("Please fix errors before submitting.");
        }
    });
});
