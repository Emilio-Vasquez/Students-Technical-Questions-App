document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.upvote-btn, .downvote-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
      const parent = button.closest('.vote-controls');
      const commentId = parent.getAttribute('data-comment-id');
      const vote = button.classList.contains('upvote-btn') ? 1 : -1;

      const res = await fetch('/comment/vote', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',  // ✅ This fixes the issue!
        body: JSON.stringify({ comment_id: commentId, vote })
      });

      if (res.status === 401) {
        alert("You must be logged in to vote.");
        return;
      }

      const data = await res.json();
      document.getElementById(`score-${commentId}`).textContent = data.score;
      
      // Add "voted" class to the clicked button, remove from sibling
      parent.querySelectorAll('.upvote-btn, .downvote-btn').forEach(btn => {
        btn.classList.remove('voted');
      });
      button.classList.add('voted');
    });
  });
});