// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(flash) {
        // Add fade-out animation after 4 seconds
        setTimeout(function() {
            flash.style.transition = 'opacity 0.5s ease-out';
            flash.style.opacity = '0';
            
            // Remove the element completely after fade animation
            setTimeout(function() {
                flash.remove();
            }, 500);
        }, 4000); // 4 seconds delay
    });
});