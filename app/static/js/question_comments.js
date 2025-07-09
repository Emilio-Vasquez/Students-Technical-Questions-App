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
      const totalReplies = parseInt(button.getAttribute('data-total-replies'), 10);

      const isHidden = repliesDiv.style.display === 'none';

      repliesDiv.style.display = isHidden ? 'block' : 'none';

      if (isHidden) {
        button.textContent = 'Hide Replies';
      } else {
        if (totalReplies > 0) {
          const label = totalReplies === 1 ? 'Reply' : 'Replies';
          button.textContent = `View ${label} (${totalReplies})`;
        } else {
          button.textContent = 'Reply';
        }
      }
    });
  });
});