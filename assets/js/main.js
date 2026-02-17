/**
 * Ferhat Ozgur Catak — Personal Academic Site
 * Vanilla JS: nav, theme, data loading, BibTeX copy, reveal
 */

(function () {
  'use strict';

  // ---------- Nav (mobile menu) ----------
  var toggle = document.getElementById('nav-toggle');
  var nav = document.getElementById('nav-menu');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
    });
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // ---------- Theme ----------
  var STORAGE_KEY = 'theme-preference';
  var html = document.documentElement;

  function getTheme() {
    var stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'dark' || stored === 'light') return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    html.classList.remove('theme-dark', 'theme-light');
    html.classList.add('theme-' + theme);
    localStorage.setItem(STORAGE_KEY, theme);
    var btn = document.getElementById('theme-toggle');
    if (btn) {
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      var sun = btn.querySelector('.icon-sun');
      var moon = btn.querySelector('.icon-moon');
      if (sun) sun.style.display = theme === 'dark' ? 'block' : 'none';
      if (moon) moon.style.display = theme === 'light' ? 'block' : 'none';
    }
  }

  var theme = getTheme();
  setTheme(theme);

  var themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      setTheme(theme === 'dark' ? 'light' : 'dark');
      theme = getTheme();
    });
  }

  // Listen for system preference changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
    if (!localStorage.getItem(STORAGE_KEY)) {
      theme = e.matches ? 'dark' : 'light';
      setTheme(theme);
    }
  });

  // ---------- Data loading (fetch with inline fallback) ----------
  function loadData(id, url, callback) {
    var inline = document.getElementById('inline-' + id);
    if (inline && inline.textContent) {
      try {
        callback(JSON.parse(inline.textContent));
        return;
      } catch (e) {}
    }
    fetch(url)
      .then(function (r) { return r.json(); })
      .then(callback)
      .catch(function () {
        if (inline && inline.textContent) {
          try { callback(JSON.parse(inline.textContent)); } catch (e) {}
        }
      });
  }

  window.loadData = loadData;

  // ---------- Render helpers (used by pages that need them) ----------
  window.renderProjects = function (containerId, dataKey) {
    loadData(dataKey || 'projects', 'data/projects.json', function (data) {
      var list = Array.isArray(data) ? data : (data.projects || data.items || []);
      var el = document.getElementById(containerId);
      if (!el) return;
      el.innerHTML = list.map(function (p) {
        var links = (p.links || []).map(function (l) {
          return '<a href="' + (l.url || '#') + '" class="btn btn--outline" target="_blank" rel="noopener">' + (l.label || l.name) + '</a>';
        }).join('');
        return '<div class="card' + (p.primary ? ' card--primary' : '') + '" data-tags="' + (p.tags || []).join(' ') + '">' +
          (p.image ? '<img src="' + (p.image) + '" alt="' + escapeHtml((p.title || p.name) + ' project image for Ferhat Ozgur Catak') + '" class="card__image" loading="lazy">' : '') +
          '<h3 class="card__title">' + (p.title || p.name) + '</h3>' +
          (p.meta ? '<p class="card__meta">' + p.meta + '</p>' : '') +
          (p.description ? '<p class="card__text">' + p.description + '</p>' : '') +
          (links ? '<div class="card__actions">' + links + '</div>' : '') + '</div>';
      }).join('');
    });
  };

  window.renderPublications = function (containerId, dataKey) {
    loadData(dataKey || 'publications', 'data/publications.json', function (data) {
      var list = Array.isArray(data) ? data : (data.publications || data.items || []);
      if (containerId === 'home-publications') list = list.filter(function (p) { return p.featured === true; });
      var el = document.getElementById(containerId);
      if (!el) return;
      el.innerHTML = list.map(function (p) {
        var links = (p.links || []).map(function (l) {
          return '<a href="' + (l.url || '#') + '" class="btn btn--outline" target="_blank" rel="noopener">' + (l.label || l.name) + '</a>';
        }).join('');
        if (p.bibtex) links += '<button type="button" class="btn btn--outline btn-copy-bibtex" data-bibtex="' + escapeHtml(JSON.stringify(p.bibtex)) + '" aria-label="Copy BibTeX">Copy BibTeX</button>';
        return '<div class="pub-item">' +
          '<div class="pub-item__title">' + (p.title || p.name) + '</div>' +
          '<div class="pub-item__venue">' + (p.venue || '') + ' (' + (p.year || '') + ')</div>' +
          (p.contribution ? '<div class="pub-item__contribution">' + p.contribution + '</div>' : '') +
          (links ? '<div class="pub-item__links">' + links + '</div>' : '') + '</div>';
      }).join('');
      el.querySelectorAll('.btn-copy-bibtex').forEach(function (btn) {
        btn.addEventListener('click', copyBibTeX);
      });
    });
  };

  window.renderTalks = function (containerId, dataKey) {
    loadData(dataKey || 'talks', 'data/talks.json', function (data) {
      var list = Array.isArray(data) ? data : (data.talks || data.items || []);
      var el = document.getElementById(containerId);
      if (!el) return;
      var icon = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>';
      el.innerHTML = list.map(function (t) {
        return '<div class="talk-item">' +
          '<span class="talk-item__icon">' + icon + '</span>' +
          '<div><div class="talk-item__title">' + (t.title || t.name) + '</div>' +
          '<div class="talk-item__meta">' + (t.venue || '') + (t.date ? ' · ' + t.date : '') + '</div>' +
          (t.links && t.links.length ? '<div class="card__actions mt-2">' + t.links.map(function (l) {
            return '<a href="' + (l.url || '#') + '" class="btn btn--outline" target="_blank" rel="noopener">' + (l.label || l.name) + '</a>';
          }).join('') + '</div>' : '') + '</div></div>';
      }).join('');
    });
  };

  window.renderActivity = function (containerId, dataKey) {
    loadData(dataKey || 'activity', 'data/activity.json', function (data) {
      var list = Array.isArray(data) ? data : (data.activity || data.items || []);
      var el = document.getElementById(containerId);
      if (!el) return;
      el.innerHTML = list.map(function (a) {
        return '<div class="timeline__item">' +
          '<div class="timeline__date">' + (a.date || '') + '</div>' +
          '<div class="timeline__title">' + (a.title || a.name) + '</div>' +
          (a.description ? '<div class="timeline__desc">' + a.description + '</div>' : '') + '</div>';
      }).join('');
    });
  };

  window.renderFaq = function (containerId, dataKey) {
    loadData(dataKey || 'faq', 'data/faq.json', function (data) {
      var list = Array.isArray(data) ? data : (data.faq || data.items || []);
      var el = document.getElementById(containerId);
      if (!el) return;
      el.innerHTML = list.map(function (f) {
        return '<div class="faq-item">' +
          '<div class="faq-item__q">' + (f.question || f.q) + '</div>' +
          '<div class="faq-item__a">' + (f.answer || f.a) + '</div></div>';
      }).join('');
    });
  };

  window.renderCourses = function (containerId, dataKey) {
    loadData(dataKey || 'courses', 'data/courses.json', function (data) {
      var list = Array.isArray(data) ? data : (data.courses || data.items || []);
      var el = document.getElementById(containerId);
      if (!el) return;
      el.innerHTML = list.map(function (c) {
        var bullets = (c.outcomes || []).map(function (o) { return '<li>' + o + '</li>'; }).join('');
        var code = c.code || '';
        var name = c.name || c.title || '';
        var url = (c.url || '').replace(/"/g, '&quot;');
        var codeHtml = url ? '<a href="' + url + '" target="_blank" rel="noopener">' + escapeHtml(code) + '</a>' : escapeHtml(code);
        var nameHtml = url ? '<a href="' + url + '" target="_blank" rel="noopener">' + escapeHtml(name) + '</a>' : escapeHtml(name);
        var courseLink = url ? '<div class="card__actions mt-2"><a href="' + url + '" class="btn btn--outline" target="_blank" rel="noopener">Course page (UiS)</a></div>' : '';
        return '<div class="course-card">' +
          '<div class="course-card__code">' + codeHtml + '</div>' +
          '<div class="course-card__name">' + nameHtml + '</div>' +
          (bullets ? '<ul class="course-card__outcomes">' + bullets + '</ul>' : '') +
          courseLink + '</div>';
      }).join('');
    });
  };

  function escapeHtml(s) {
    if (!s) return '';
    var div = document.createElement('div');
    div.textContent = s;
    return div.innerHTML.replace(/"/g, '&quot;');
  }

  // ---------- Copy BibTeX ----------
  function copyBibTeX(e) {
    var btn = e.target.closest('.btn-copy-bibtex');
    if (!btn) return;
    var bibtex = btn.getAttribute('data-bibtex');
    if (!bibtex) return;
    try { bibtex = JSON.parse(bibtex); } catch (err) { bibtex = decodeHtml(bibtex); }
    navigator.clipboard.writeText(bibtex).then(function () {
      var orig = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(function () { btn.textContent = orig; }, 2000);
    });
  }

  function decodeHtml(s) {
    var div = document.createElement('div');
    div.innerHTML = s;
    return div.textContent;
  }

  window.copyBibTeX = copyBibTeX;

  // ---------- Scroll reveal ----------
  function initReveal() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    var io = typeof IntersectionObserver !== 'undefined' ? new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) entry.target.classList.add('is-visible');
      });
    }, { rootMargin: '0px 0px -40px 0px', threshold: 0.1 }) : null;
    if (io) els.forEach(function (el) { io.observe(el); });
    else els.forEach(function (el) { el.classList.add('is-visible'); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReveal);
  } else {
    initReveal();
  }
})();
