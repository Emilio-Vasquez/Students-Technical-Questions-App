window.handleNotLoggedInSubmission = function(event) {
    event.preventDefault();

    const flashMessage = document.createElement('div');
    flashMessage.innerText = "🚫 You must be logged in to submit your solution.";
    flashMessage.style.position = 'fixed';
    flashMessage.style.top = '20px';
    flashMessage.style.left = '50%';
    flashMessage.style.transform = 'translateX(-50%)';
    flashMessage.style.backgroundColor = '#f44336';
    flashMessage.style.color = 'white';
    flashMessage.style.padding = '12px 20px';
    flashMessage.style.borderRadius = '6px';
    flashMessage.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';
    flashMessage.style.zIndex = 1000;

    document.body.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
        window.location.href = "/login";  // Or use a dynamic route if needed
    }, 1800);
};
