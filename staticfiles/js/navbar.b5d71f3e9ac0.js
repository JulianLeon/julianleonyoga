const mobileNav = document.querySelector(".hamburger");
const navbar = document.querySelector(".menubar");

const toggleNav = () => {
  navbar.classList.toggle("active");
  mobileNav.classList.toggle("hamburger-active");
};
mobileNav.addEventListener("click", () => toggleNav());

window.addEventListener("scroll", function () {
  const nav = document.getElementById("navbar");

  if (window.scrollY > 5) {
    nav.classList.add("scrolled");
  } else {
    nav.classList.remove("scrolled");
  }
});

// Menü schließen, wenn ein Link in der mobilen Navigation geklickt wird
document.querySelectorAll(".menubar a").forEach((link) => {
  link.addEventListener("click", () => {
    navbar.classList.remove("active");
    mobileNav.classList.remove("hamburger-active");
  });
});
