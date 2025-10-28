const toggle = document.getElementById('menu-toggle');
const links = document.getElementById('nav-links');

// Toggle menu
toggle.addEventListener('click', (e) => {
  e.stopPropagation(); // prevent immediate closing
  links.classList.toggle('active');
});

// Close menu when clicking a link
document.querySelectorAll('#nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    links.classList.remove('active');
  });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!toggle.contains(e.target) && !links.contains(e.target)) {
    links.classList.remove('active');
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const userIcon = document.querySelector(".user-icon");
  const dropdown = document.querySelector(".user-dropdown");

  if (userIcon && dropdown) {
    userIcon.addEventListener("click", () => {
      dropdown.classList.toggle("show");
    });

    // Close dropdown if clicking outside
    document.addEventListener("click", (e) => {
      if (!userIcon.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove("show");
      }
    });
  }
});
