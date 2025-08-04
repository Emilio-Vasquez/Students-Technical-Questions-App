function showFlash(message, type = "success") {
  const container = document.getElementById("flash-container");
  const flash = document.createElement("div");
  flash.textContent = message;
  flash.style.padding = "0.75rem";
  flash.style.marginBottom = "1rem";
  flash.style.borderRadius = "4px";

  if (type === "success") {
    flash.style.backgroundColor = "#d4edda";
    flash.style.color = "#155724";
    flash.style.border = "1px solid #c3e6cb";
  } else if (type === "error" || type === "danger") {
    flash.style.backgroundColor = "#f8d7da";
    flash.style.color = "#721c24";
    flash.style.border = "1px solid #f5c6cb";
  } else if (type === "warning") {
    flash.style.backgroundColor = "#fff3cd";
    flash.style.color = "#856404";
    flash.style.border = "1px solid #ffeeba";
  }

  container.appendChild(flash);

  setTimeout(() => {
    flash.remove();
  }, 3000);
}

document.getElementById('select-all').addEventListener('click', function(e) {
  const checkboxes = document.querySelectorAll('input[name="user_ids"]');
  for (const cb of checkboxes) cb.checked = e.target.checked;
});

function submitVerifyForm(userId, username, action) {
  const form = document.getElementById(`verify-form-${userId}`);
  const actionInput = form.querySelector('input[name="action"]');
  if (actionInput) {
    actionInput.value = action;
    form.submit();
  }
}

function submitPromoteForm(userId, username, action) {
  const form = document.getElementById(`promote-form-${userId}`);
  const actionInput = form.querySelector('input[name="action"]');
  if (actionInput) {
    actionInput.value = action;
    form.submit();
  }
}
