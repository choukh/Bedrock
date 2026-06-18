/* Bedrock site behaviour: theme toggle, KaTeX rendering, type-on-hover, search.
 *
 * The type-on-hover mechanism is modelled on the 1lab's highlight-hover (AGPL-3.0,
 * https://1lab.dev) but reimplemented for Bedrock's `types/<Module>.json` sidecars.
 * Vanilla JS, no build step. See NOTICE.
 */
(function () {
  "use strict";
  var cfg = window.bedrock || { baseUrl: "", lang: "en", module: "" };

  /* ---- theme (light / dark / system) -------------------------------------- */
  var root = document.documentElement;
  function applyTheme(t) {
    root.classList.remove("theme-light", "theme-dark");
    if (t === "light") root.classList.add("theme-light");
    else if (t === "dark") root.classList.add("theme-dark");
  }
  applyTheme(localStorage.getItem("bedrock-theme") || "system");
  document.addEventListener("DOMContentLoaded", function () {
    try { localStorage.setItem("bedrock-lang", cfg.lang); } catch (e) {}
    var btn = document.getElementById("theme-toggle");
    if (btn) btn.addEventListener("click", function () {
      var order = ["system", "light", "dark"];
      var cur = localStorage.getItem("bedrock-theme") || "system";
      var next = order[(order.indexOf(cur) + 1) % order.length];
      localStorage.setItem("bedrock-theme", next);
      applyTheme(next);
    });
    renderMath();
    initSearch();
    initHover();
    initNav();
  });

  /* ---- mobile navigation drawer ------------------------------------------- */
  function initNav() {
    var body = document.body;
    var toggle = document.getElementById("nav-toggle");
    var toc = document.getElementById("toc");
    if (!toggle || !toc) return;
    var backdrop = document.getElementById("nav-backdrop");
    var close = document.getElementById("nav-close");
    function setOpen(open) {
      body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    toggle.addEventListener("click", function () {
      setOpen(!body.classList.contains("nav-open"));
    });
    if (backdrop) backdrop.addEventListener("click", function () { setOpen(false); });
    if (close) close.addEventListener("click", function () { setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
    /* Tapping any link in the drawer navigates, so dismiss the drawer with it. */
    toc.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    /* Leaving narrow layout (e.g. rotate to landscape) must not strand an open drawer. */
    var wide = window.matchMedia("(min-width: 60rem)");
    (wide.addEventListener ? wide.addEventListener.bind(wide, "change")
                           : wide.addListener.bind(wide))(function (e) {
      if (e.matches) setOpen(false);
    });
  }

  /* ---- math (client-side KaTeX over pre-wrapped spans) -------------------- */
  function renderMath() {
    if (typeof katex === "undefined") return;
    document.querySelectorAll(".math").forEach(function (el) {
      var disp = el.classList.contains("display");
      var tex = el.textContent.trim().replace(/^\${1,2}/, "").replace(/\${1,2}$/, "");
      try { katex.render(tex, el, { displayMode: disp, throwOnError: false }); }
      catch (e) { /* leave the source text in place on error */ }
    });
  }

  /* ---- type-on-hover ------------------------------------------------------ */
  var typeCache = {};
  function fetchTypes(mod) {
    if (typeCache[mod]) return typeCache[mod];
    typeCache[mod] = fetch(cfg.baseUrl + "/" + cfg.lang + "/types/" + mod + ".json")
      .then(function (r) { return r.ok ? r.json() : {}; })
      .catch(function () { return {}; });
    return typeCache[mod];
  }
  function initHover() {
    var popup = null;
    function hide() { if (popup) { popup.remove(); popup = null; } }
    document.querySelectorAll("a[data-type]").forEach(function (a) {
      a.addEventListener("mouseenter", function () {
        var spec = a.getAttribute("data-type").split("#");
        fetchTypes(spec[0]).then(function (tys) {
          var html = tys[spec[1]];
          if (!html) return;
          hide();
          popup = document.createElement("div");
          popup.className = "hover-popup";
          popup.innerHTML = html;
          document.body.appendChild(popup);
          var r = a.getBoundingClientRect();
          popup.style.left = (window.scrollX + r.left) + "px";
          popup.style.top = (window.scrollY + r.bottom + 4) + "px";
        });
      });
      a.addEventListener("mouseleave", hide);
    });
  }

  /* ---- search (fetch search.json once, simple fuzzy) ---------------------- */
  function fuzzy(q, s) {
    q = q.toLowerCase(); s = s.toLowerCase();
    if (s.indexOf(q) >= 0) return 100 - (s.length - q.length) * 0.1;
    var i = 0, score = 0;
    for (var j = 0; j < s.length && i < q.length; j++)
      if (s[j] === q[i]) { i++; score += 1; }
    return i === q.length ? score : -1;
  }
  function initSearch() {
    var box = document.getElementById("search-box");
    var out = document.getElementById("search-results");
    if (!box || !out) return;
    var data = null, sel = -1, shown = [];
    function load() {
      if (data) return Promise.resolve(data);
      return fetch(cfg.baseUrl + "/" + cfg.lang + "/search.json")
        .then(function (r) { return r.json(); })
        .then(function (d) { data = d; return d; }).catch(function () { return []; });
    }
    function render(q) {
      if (!q) { out.hidden = true; return; }
      shown = data.map(function (e) { return { e: e, s: fuzzy(q, e.name) }; })
        .filter(function (x) { return x.s >= 0; })
        .sort(function (a, b) { return b.s - a.s; }).slice(0, 25).map(function (x) { return x.e; });
      out.innerHTML = shown.map(function (e, i) {
        return '<a class="res' + (i === sel ? ' sel' : '') + '" href="' + e.href + '">' +
          '<span class="nm">' + esc(e.name) + '</span> ' +
          '<span class="mod">' + esc(e.module) + '</span>' +
          (e.type ? '<br><span class="ty">' + esc(e.type) + '</span>' : '') + '</a>';
      }).join("");
      out.hidden = shown.length === 0;
    }
    function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
    box.addEventListener("input", function () { sel = -1; load().then(function () { render(box.value.trim()); }); });
    box.addEventListener("keydown", function (e) {
      if (out.hidden) return;
      if (e.key === "ArrowDown") { sel = Math.min(sel + 1, shown.length - 1); render(box.value.trim()); e.preventDefault(); }
      else if (e.key === "ArrowUp") { sel = Math.max(sel - 1, 0); render(box.value.trim()); e.preventDefault(); }
      else if (e.key === "Enter" && sel >= 0) { location.href = shown[sel].href; }
      else if (e.key === "Escape") { out.hidden = true; }
    });
    document.addEventListener("click", function (e) {
      if (!out.contains(e.target) && e.target !== box) out.hidden = true;
    });
  }
})();
