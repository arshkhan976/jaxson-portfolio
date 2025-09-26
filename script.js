// Smooth scroll for nav menu + active link highlighting
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', function(e) {
    e.preventDefault();
    const id = this.getAttribute('href');
    document.querySelector(id)?.scrollIntoView({behavior: 'smooth', block: 'start'});
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    this.classList.add('active');
    // Close mobile menu
    document.querySelector('.nav-links').classList.remove('mobile-open');
  });
});

// Mobile nav menu toggle
document.getElementById('mobileMenuBtn').addEventListener('click', () => {
  document.querySelector('.nav-links').classList.toggle('mobile-open');
});

// Scroll-triggered fade-in for sections
function onScrollFadeIn() {
  document.querySelectorAll('.fade-in-up:not(.visible)').forEach(el => {
    if (el.getBoundingClientRect().top < window.innerHeight - 80) {
      el.classList.add('visible');
      el.style.opacity = 1;
      el.style.transform = 'none';
    }
  });
}
window.addEventListener('scroll', onScrollFadeIn);
window.addEventListener('DOMContentLoaded', onScrollFadeIn);

// Light/Dark mode toggle
const themeBtn = document.getElementById('toggleMode');
const root = document.documentElement;
function setTheme(theme) {
  root.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}
function toggleTheme() {
  const isDark = root.getAttribute('data-theme') === 'dark';
  setTheme(isDark ? 'light' : 'dark');
}
themeBtn.addEventListener('click', toggleTheme);
(function initTheme() {
  const saved = localStorage.getItem('theme');
  setTheme(saved ? saved : 'light');
})();

// Highlight nav on scroll
const sectionIds = ['home', 'about', 'portfolio', 'contact'];
window.addEventListener('scroll', () => {
  let scrollPos = document.documentElement.scrollTop || document.body.scrollTop;
  sectionIds.forEach(id => {
    const sec = document.getElementById(id);
    if (sec.offsetTop - 100 <= scrollPos) {
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      let active = document.querySelector(`.nav-link[href="#${id}"]`);
      if (active) active.classList.add('active');
    }
  });
});