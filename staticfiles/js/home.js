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

document.addEventListener("DOMContentLoaded", function () {
  const faqButtons = document.querySelectorAll(".faq-question");

  faqButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const faqItem = button.closest(".faq-item");

      // Toggle current item
      faqItem.classList.toggle("active");

      // Close all other open items
      document.querySelectorAll(".faq-item").forEach((item) => {
        if (item !== faqItem) {
          item.classList.remove("active");
        }
      });
    });
  });
});

// Testimonial Slider Script
document.addEventListener("DOMContentLoaded", () => {
  const track = document.querySelector(".testimonial-track");
  const items = document.querySelectorAll(".testimonial-item");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");

  let index = 0;
  const visibleItems = 3; // Adjust number of visible cards at once
  const itemWidth = items[0].offsetWidth + 30; // card width + margin

  function updateSlider() {
    track.style.transform = `translateX(-${index * itemWidth}px)`;
  }

  nextBtn.addEventListener("click", () => {
    if (index < items.length - visibleItems) {
      index++;
    } else {
      index = 0;
    }
    updateSlider();
  });

  prevBtn.addEventListener("click", () => {
    if (index > 0) {
      index--;
    } else {
      index = items.length - visibleItems;
    }
    updateSlider();
  });

  // Auto-slide every 5 seconds
  setInterval(() => {
    nextBtn.click();
  }, 5000);
});
