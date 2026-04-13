/* =============================================
   PORTFOLIO — main.js
============================================= */

/* === THEME SYSTEM === */
(function() {
  const root = document.documentElement;

  function applyTheme(mode) {
    if (mode === 'dark') {
      root.setAttribute('data-theme', 'dark');
    } else if (mode === 'light') {
      root.setAttribute('data-theme', 'light');
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
  }

  function setActiveButton(mode) {
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === mode);
    });
  }

  function setTheme(mode) {
    localStorage.setItem('theme', mode);
    applyTheme(mode);
    setActiveButton(mode);
  }

  const saved = localStorage.getItem('theme') || 'dark';
  applyTheme(saved);

  document.addEventListener('DOMContentLoaded', function() {
    setActiveButton(saved);

    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => setTheme(btn.dataset.mode));
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (localStorage.getItem('theme') === 'system') {
        applyTheme('system');
      }
    });
  });
})();

/* === CUSTOM CURSOR === */
document.addEventListener('mousemove', (e) => {
  document.body.style.setProperty('--cx', e.clientX + 'px');
  document.body.style.setProperty('--cy', e.clientY + 'px');
});

/* === NAVBAR SCROLL EFFECT === */
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 40) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

/* === HAMBURGER MENU === */
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('active');
    const spans = hamburger.querySelectorAll('span');
    if (hamburger.classList.contains('active')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity   = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.opacity   = '';
      spans[2].style.transform = '';
    }
  });

  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
      hamburger.querySelectorAll('span').forEach(s => {
        s.style.transform = '';
        s.style.opacity   = '';
      });
    });
  });
}

/* === SCROLL REVEAL === */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* === SKILL BAR ANIMATION === */
const skillObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const fill = entry.target;
      const width = fill.dataset.width;
      setTimeout(() => {
        fill.style.width = width + '%';
      }, 300);
      skillObserver.unobserve(fill);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.skill-fill').forEach(el => skillObserver.observe(el));

/* === TYPEWRITER EFFECT === */
const typewriterEl = document.getElementById('typewriter');
if (typewriterEl) {
  const phrases = [
    'Full Stack Developer',
    'Python & Django Builder',
    'Electrical Engineering Student @ FUTO',
    'Frontend Developer',
  ];
  let phraseIndex = 0;
  let charIndex   = 0;
  let isDeleting  = false;
  let typingSpeed = 80;

  function type() {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      typewriterEl.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 40;
    } else {
      typewriterEl.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 80;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      isDeleting = true;
      typingSpeed = 1800;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typingSpeed = 400;
    }

    setTimeout(type, typingSpeed);
  }

  setTimeout(type, 600);
}

/* === AUTO-DISMISS MESSAGES === */
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(alert => {
    alert.style.transition = 'opacity 0.5s ease';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 500);
  });
}, 4000);