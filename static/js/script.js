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
