document.addEventListener("DOMContentLoaded", function () {
  const dateInput = document.querySelector('input[type="date"]');
  if (dateInput) {
    dateInput.addEventListener("change", function () {
      dateInput.setCustomValidity("");
    });
  }
});
