// 1. NAV TOGGLE
const navToggle = document.getElementById('navToggle');
const navList   = document.querySelector('.nav-list');
navToggle.addEventListener('click', () => {
  navList.classList.toggle('open');
});

// 2. HEADER BG ON SCROLL
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 50);
});

// 3. SCROLL-REVEAL (IntersectionObserver)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.scroll-reveal')
  .forEach(el => observer.observe(el));