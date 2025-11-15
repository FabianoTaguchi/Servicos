document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach((el) => {
    setTimeout(() => {
      el.remove();
    }, 3000);
  });
});