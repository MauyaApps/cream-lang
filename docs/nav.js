// ── Language ──
let currentLang = localStorage.getItem('cream-lang') || 'en';

function applyLang() {
  document.querySelectorAll('[data-en]').forEach(el => {
    el.textContent = currentLang === 'en' ? el.dataset.en : el.dataset.ru;
  });
  document.querySelectorAll('.lang-toggle').forEach(b => {
    b.textContent = currentLang === 'en' ? 'RU' : 'EN';
  });
  document.documentElement.lang = currentLang;
}

function toggleLang() {
  currentLang = currentLang === 'en' ? 'ru' : 'en';
  localStorage.setItem('cream-lang', currentLang);
  applyLang();
}

// ── Hamburger ──
function initNav() {
  const burger = document.querySelector('.nav-burger');
  const drawer = document.querySelector('.nav-drawer');
  if (!burger || !drawer) return;

  burger.addEventListener('click', () => {
    const open = drawer.classList.toggle('open');
    burger.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // close on link click
  drawer.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      drawer.classList.remove('open');
      burger.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  applyLang();
  initNav();
});
