function handleNotLoggedIn(event) {
  event.preventDefault();
  alert("You must be logged in to post a comment.");
}

document.addEventListener('DOMContentLoaded', () => {
  const toggleButtons = document.querySelectorAll('.toggle-replies-btn');

  toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
      const commentId = button.getAttribute('data-comment-id');
      const repliesDiv = document.getElementById(`replies-${commentId}`);

      if (repliesDiv.style.display === 'none') {
        repliesDiv.style.display = 'block';
        button.textContent = 'Hide Replies';
      } else {
        repliesDiv.style.display = 'none';
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
          button.textContent = originalText;
        } else {
          button.textContent = 'View Replies';
        }
      }
    });
  });
});
