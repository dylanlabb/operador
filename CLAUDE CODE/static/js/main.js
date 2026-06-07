// Navbar: shadow on scroll
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNav');
  if (!nav) return;
  nav.style.boxShadow = window.scrollY > 20 ? '0 2px 20px rgba(0,0,0,0.35)' : 'none';
});

// Close mobile menu on nav-link click
document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
  link.addEventListener('click', () => {
    const collapse = document.getElementById('navMenu');
    if (collapse && collapse.classList.contains('show')) {
      const bsCollapse = bootstrap.Collapse.getInstance(collapse);
      if (bsCollapse) bsCollapse.hide();
    }
  });
});

// #24: IntersectionObserver — highlight nav link for visible section (index page only)
(function () {
  const sections = document.querySelectorAll('section[id]');
  if (!sections.length) return;

  const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href*="#"]');
  if (!navLinks.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navLinks.forEach(link => {
        const href = link.getAttribute('href') || '';
        if (href.endsWith('#' + entry.target.id)) {
          navLinks.forEach(l => l.classList.remove('active'));
          link.classList.add('active');
        }
      });
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => observer.observe(s));
})();

// #25: Pre-fill contact form from URL params (?producto=... or ?asunto=...)
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const asuntoSelect = document.getElementById('asunto');
  const msgArea = document.getElementById('mensaje');

  const producto = params.get('producto');
  const asunto = params.get('asunto');

  if (asuntoSelect) {
    if (producto) {
      asuntoSelect.value = 'Cotización de envases';
      if (msgArea && !msgArea.value) {
        msgArea.value = `Hola, me interesa obtener información y precio sobre: ${producto}.`;
      }
    } else if (asunto) {
      const opt = Array.from(asuntoSelect.options).find(o => o.value === asunto);
      if (opt) asuntoSelect.value = asunto;
    }
  }
});
