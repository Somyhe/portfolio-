// =============================================
//  THEME
// =============================================
const setTheme = t => { document.body.setAttribute('data-theme', t); localStorage.setItem('theme', t); };
const toggleTheme = () => setTheme(document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
setTheme(localStorage.getItem('theme') || 'light');
document.getElementById('themeToggle').onclick = toggleTheme;
document.getElementById('themeToggleMob').onclick = toggleTheme;

const mql = matchMedia('(max-width:900px)');
const syncMob = e => document.getElementById('themeToggleMob').style.display = e.matches ? 'block' : 'none';
mql.addEventListener('change', syncMob); syncMob(mql);

// =============================================
//  NAVBAR
// =============================================
const nav = document.getElementById('nav');
const ham = document.getElementById('hamburger');
const links = document.getElementById('navLinks');

window.addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 50), { passive: true });
ham.onclick = () => { ham.classList.toggle('active'); links.classList.toggle('open'); };
links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { ham.classList.remove('active'); links.classList.remove('open'); }));

// Active nav highlight
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
  const sy = scrollY + 120;
  sections.forEach(s => {
    const link = links.querySelector(`a[href="#${s.id}"]`);
    if (link) link.classList.toggle('active', sy >= s.offsetTop - 100 && sy < s.offsetTop + s.offsetHeight);
  });
}, { passive: true });

// =============================================
//  MAGNETIC CURSOR  (desktop only)
// =============================================
const dot = document.getElementById('curDot');
const ring = document.getElementById('curRing');
let mx = 0, my = 0, rx = 0, ry = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  dot.style.left = mx - 3 + 'px';
  dot.style.top = my - 3 + 'px';
});

(function curLoop() {
  rx += (mx - rx) * 0.12;
  ry += (my - ry) * 0.12;
  ring.style.left = rx - 21 + 'px';
  ring.style.top = ry - 21 + 'px';
  requestAnimationFrame(curLoop);
})();

const interactors = 'a, button, .chip, .stat, .proj, .pub, .act, .tl, .exp, .gcard';
document.querySelectorAll(interactors).forEach(el => {
  el.addEventListener('mouseenter', () => ring.classList.add('hover'));
  el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
});

// =============================================
//  3D TILT ON CARDS  (glass cards get perspective)
// =============================================
document.querySelectorAll('.gcard').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const px = (e.clientX - cx) / (rect.width / 2);
    const py = (e.clientY - cy) / (rect.height / 2);
    card.style.transform = `perspective(800px) rotateY(${px * 3}deg) rotateX(${-py * 3}deg) scale3d(1.01,1.01,1.01)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(800px) rotateY(0) rotateX(0) scale3d(1,1,1)';
  });
});

// =============================================
//  PARALLAX MESH ORBS on mouse
// =============================================
const orbs = document.querySelectorAll('.mesh-orb');
document.addEventListener('mousemove', e => {
  const fx = (e.clientX / innerWidth - 0.5) * 2;
  const fy = (e.clientY / innerHeight - 0.5) * 2;
  orbs.forEach((orb, i) => {
    const speed = (i + 1) * 12;
    orb.style.transform += ''; // trigger recomposite
    orb.style.marginLeft = fx * speed + 'px';
    orb.style.marginTop = fy * speed + 'px';
  });
});

// =============================================
//  SCROLL REVEAL (IntersectionObserver)
// =============================================
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('vis'); });
}, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

document.querySelectorAll('.rv').forEach(el => revealObs.observe(el));

// =============================================
//  COUNTER ANIMATION  (stats section)
// =============================================
const counters = document.querySelectorAll('[data-count]');
const countObs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    const isFloat = target % 1 !== 0;
    const duration = 1800;
    const start = performance.now();

    (function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 4); // ease-out quart
      const current = eased * target;
      el.textContent = (isFloat ? current.toFixed(2) : Math.floor(current)) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    })(start);

    countObs.unobserve(el);
  });
}, { threshold: 0.5 });

counters.forEach(c => countObs.observe(c));

// =============================================
//  SKILLS FILTER with animation
// =============================================
document.querySelectorAll('.sf').forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.sf').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
    const f = btn.dataset.f;
    document.querySelectorAll('.chip').forEach((c, i) => {
      const show = f === 'all' || c.dataset.cat === f;
      if (!show) {
        c.style.transform = 'scale(0.8)';
        c.style.opacity = '0';
        setTimeout(() => c.classList.add('hide'), 250);
      } else {
        c.classList.remove('hide');
        c.style.opacity = '0';
        c.style.transform = 'scale(0.8)';
        setTimeout(() => {
          c.style.opacity = '1';
          c.style.transform = 'translateY(0) scale(1)';
        }, i * 30);
      }
    });
  };
});

// =============================================
//  IMAGE CAROUSEL
// =============================================
const cState = {};

function cGet(id) { return cState[id] || (cState[id] = { i: 0 }); }

function cMove(id, dir) {
  const el = document.getElementById(id);
  const track = el.querySelector('.crsl-track');
  const slides = el.querySelectorAll('.crsl-slide');
  const dots = el.querySelectorAll('.crsl-pip');
  const s = cGet(id);
  s.i = (s.i + dir + slides.length) % slides.length;
  track.style.transform = `translateX(-${s.i * 100}%)`;
  dots.forEach((d, i) => d.classList.toggle('on', i === s.i));
}

function cGo(id, idx) {
  const el = document.getElementById(id);
  const s = cGet(id);
  s.i = idx;
  el.querySelector('.crsl-track').style.transform = `translateX(-${idx * 100}%)`;
  el.querySelectorAll('.crsl-pip').forEach((d, i) => d.classList.toggle('on', i === idx));
}

// Auto-play
['crsl-aydi', 'crsl-mz'].forEach(id => setInterval(() => cMove(id, 1), 5500));

// =============================================
//  SMOOTH SCROLL
// =============================================
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.onclick = e => {
    e.preventDefault();
    const t = document.querySelector(a.getAttribute('href'));
    if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
});

// =============================================
//  TYPED EFFECT on hero heading (one-time)
// =============================================
//  BACK TO TOP
// =============================================
document.getElementById('year').textContent = new Date().getFullYear();

const backTop = document.getElementById('backTop');
window.addEventListener('scroll', () => {
  backTop.classList.toggle('show', window.scrollY > 400);
}, { passive: true });
backTop.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });

// =============================================
//  ROLE CYCLING in hero
// =============================================
const heroRoleEl = document.getElementById('heroRole');
if (heroRoleEl) {
  const roles = ['Computer Science Graduate', 'AI Researcher', 'Published Author', 'Full-Stack Developer'];
  let roleIdx = 0;
  setInterval(() => {
    heroRoleEl.style.opacity = '0';
    heroRoleEl.style.transform = 'translateY(-8px)';
    setTimeout(() => {
      roleIdx = (roleIdx + 1) % roles.length;
      heroRoleEl.textContent = roles[roleIdx];
      heroRoleEl.style.opacity = '1';
      heroRoleEl.style.transform = 'translateY(0)';
    }, 350);
  }, 2800);
}

// =============================================
//  TYPED EFFECT on hero heading (one-time)
// =============================================
const heroName = document.getElementById('heroName');
if (heroName) {
  const text = heroName.textContent;
  heroName.textContent = '';
  heroName.style.borderRight = '2px solid var(--ac1)';
  let i = 0;
  const typeInterval = setInterval(() => {
    heroName.textContent += text[i];
    i++;
    if (i >= text.length) {
      clearInterval(typeInterval);
      setTimeout(() => heroName.style.borderRight = 'none', 1200);
    }
  }, 80);
}