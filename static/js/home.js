document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("menu-toggle");
  const navLinks = document.getElementById("nav-links");

  if (toggle && navLinks) {
    toggle.addEventListener("click", () => {
      navLinks.classList.toggle("show");
    });
  }

  // User dropdown toggle
  const userMenu = document.querySelector(".user-menu");
  const userDropdown = document.querySelector(".user-dropdown");

  if (userMenu && userDropdown) {
    userMenu.addEventListener("click", (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle("show");
    });

    document.addEventListener("click", (e) => {
      if (!userMenu.contains(e.target)) {
        userDropdown.classList.remove("show");
      }
    });
  }
});
