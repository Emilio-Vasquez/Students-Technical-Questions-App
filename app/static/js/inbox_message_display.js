function toggleExpand(link) {
  const wrapper = link.previousElementSibling;
  const isExpanded = wrapper.style.maxHeight === "none";

  wrapper.style.maxHeight = isExpanded ? "5.5em" : "none";
  const fade = wrapper.querySelector('.fadeout');
  if (fade) {
    fade.style.display = isExpanded ? "" : "none";
  }
  link.textContent = isExpanded ? "Show more" : "Show less";
}

// Hide expand/fade UI for short messages
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.truncated-message').forEach(wrapper => {
    const fullHeight = wrapper.scrollHeight;
    const maxHeight = parseFloat(getComputedStyle(wrapper).maxHeight);

    if (fullHeight <= maxHeight + 2) {
      const link = wrapper.nextElementSibling;
      if (link && link.tagName.toLowerCase() === 'a') {
        link.style.display = 'none';
      }
      const fade = wrapper.querySelector('.fadeout');
      if (fade) fade.style.display = 'none';
    }
  });
});
