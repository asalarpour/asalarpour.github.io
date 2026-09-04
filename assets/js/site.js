(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const navButton = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  const media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  const readTheme = () => {
    try {
      const saved = localStorage.getItem('site-theme');
      return saved === 'light' || saved === 'dark' ? saved : null;
    } catch (_) {
      return null;
    }
  };

  const saveTheme = (theme) => {
    try {
      localStorage.setItem('site-theme', theme);
    } catch (_) {
      // The site still works when storage is unavailable.
    }
  };

  const resolvedTheme = () => readTheme() || (media && media.matches ? 'dark' : 'light');

  const applyTheme = (theme, persist = false) => {
    root.dataset.theme = theme;
    if (persist) saveTheme(theme);
    if (themeButton) {
      const isDark = theme === 'dark';
      themeButton.setAttribute('aria-label', isDark ? 'Use light theme' : 'Use dark theme');
      themeButton.setAttribute('title', isDark ? 'Use light theme' : 'Use dark theme');
      themeButton.dataset.currentTheme = theme;
    }
  };

  applyTheme(resolvedTheme());

  themeButton?.addEventListener('click', () => {
    applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true);
  });

  media?.addEventListener?.('change', (event) => {
    if (!readTheme()) applyTheme(event.matches ? 'dark' : 'light');
  });

  const closeNav = () => {
    if (!nav || !navButton) return;
    nav.dataset.open = 'false';
    navButton.setAttribute('aria-expanded', 'false');
    navButton.setAttribute('aria-label', 'Open menu');
  };

  navButton?.addEventListener('click', () => {
    if (!nav) return;
    const open = nav.dataset.open !== 'true';
    nav.dataset.open = String(open);
    navButton.setAttribute('aria-expanded', String(open));
    navButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeNav));

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });

  document.addEventListener('click', (event) => {
    if (!nav || !navButton || nav.dataset.open !== 'true') return;
    if (!nav.contains(event.target) && !navButton.contains(event.target)) closeNav();
  });

  const year = document.querySelector('[data-current-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
