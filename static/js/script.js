document.addEventListener("DOMContentLoaded", function () {
  const barIcon = document.getElementById("bar-icon");
  const menu = document.getElementById("menu-hidden");

  barIcon.addEventListener("click", function () {
    menu.classList.toggle("hidden");
  });
});
