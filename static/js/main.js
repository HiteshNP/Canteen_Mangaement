// FreshBite — small UI helpers

// Auto-dismiss flash messages
document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach((f) => {
    setTimeout(() => {
      f.style.transition = "opacity .4s, transform .4s";
      f.style.opacity = "0";
      f.style.transform = "translateY(-8px)";
      setTimeout(() => f.remove(), 400);
    }, 3500);
  });

  // Live menu search (client-side filter on current page)
  const search = document.getElementById("menuSearch");
  if (search) {
    search.addEventListener("input", (e) => {
      const q = e.target.value.toLowerCase();
      document.querySelectorAll(".food-card").forEach((card) => {
        const name = card.dataset.name || "";
        card.style.display = name.includes(q) ? "" : "none";
      });
    });
  }
});

// Animate dashboard bars on load
window.addEventListener("load", () => {
  document.querySelectorAll(".bar[data-h]").forEach((bar) => {
    requestAnimationFrame(() => {
      bar.style.height = bar.dataset.h + "%";
    });
  });
  document.querySelectorAll(".progress i[data-w]").forEach((p) => {
    requestAnimationFrame(() => {
      p.style.width = p.dataset.w + "%";
    });
  });
});
