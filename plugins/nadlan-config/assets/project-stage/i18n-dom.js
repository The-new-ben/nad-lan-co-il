/* The stage in the page's language (HAD-361, 28.9.2026). The stage, its 360 room, its slice and its cards are drawn in the
 * browser, in Hebrew; on a project's language page this swaps every Hebrew string they show for the page's language, by
 * the same dictionary and in the same order as the server pass (inc/lang-pages.php): exact, names, patterns (captures
 * translated when known; a capture still in Hebrew leaves the whole line as it was), then known names inside a line.
 * It starts before the stage and watches what is added or changed; the article and the lead are never touched. On the
 * left-to-right languages a block the stage makes with dir="rtl" becomes dir="ltr", and lang="he" the page's language.
 * The dictionary comes with the page, as JSON in the element #nadlan-stage-i18n ({ lang, exact, names, patterns }, from
 * i18n/lang-pages.json and i18n/stage-dict.json, for this language). This file is printed inline: no closing script tag in it. */
(function () {
  'use strict';
  const el = document.getElementById('nadlan-stage-i18n');
  if (!el) return;
  let D;
  try { D = JSON.parse(el.textContent); } catch (e) { return; }
  const HE = /[֐-׿]/;
  const LTR = D.lang !== 'ar' && D.lang !== 'he';
  const exact = D.exact || {}, names = D.names || {};
  const pats = (D.patterns || []).map((p) => { try { return { re: new RegExp(p.re, 'u'), tr: p.tr }; } catch (e) { return null; } }).filter(Boolean);
  const nameKeys = Object.keys(names).sort((a, b) => b.length - a.length);
  const cache = new Map();
  window.__nlStageI18n = { lang: D.lang, misses: new Set() };

  function tr(s) {
    if (cache.has(s)) return cache.get(s);
    let out = null;
    if (Object.prototype.hasOwnProperty.call(exact, s)) out = exact[s];
    else if (Object.prototype.hasOwnProperty.call(names, s)) out = names[s];
    else {
      for (const p of pats) {
        const m = p.re.exec(s);
        if (!m) continue;
        let r = p.tr, ok = true;
        for (let i = m.length - 1; i >= 1; i--) {
          let c = m[i] == null ? '' : m[i];
          if (Object.prototype.hasOwnProperty.call(names, c)) c = names[c];
          else if (Object.prototype.hasOwnProperty.call(exact, c)) c = exact[c];
          else if (HE.test(c)) { ok = false; break; }
          r = r.split('{' + i + '}').join(c);
        }
        if (ok) { out = r; break; }
      }
      if (out == null && nameKeys.length) {
        let t = s;
        for (const k of nameKeys) if (t.indexOf(k) >= 0) t = t.split(k).join(names[k]);
        if (t !== s && !HE.test(t)) out = t;
      }
    }
    if (out == null) window.__nlStageI18n.misses.add(s);
    cache.set(s, out);
    return out;
  }
  const kept = (node) => {
    const e = node.nodeType === 1 ? node : node.parentElement;
    return !e || !!e.closest('.nadlan-project-article, .nl-lead, script, style, textarea, [data-nl-keep-lang]');
  };
  function doText(n) {
    const v = n.nodeValue;
    if (!v || !HE.test(v) || kept(n)) return;
    const key = v.replace(/\s+/g, ' ').trim();
    const t = tr(key);
    if (t == null) return;
    const lead = v.match(/^\s*/)[0], tail = v.match(/\s*$/)[0];
    const nv = lead + t + tail;
    if (nv !== v) n.nodeValue = nv;
  }
  const ATTRS = ['aria-label', 'title', 'alt', 'placeholder'];
  function doEl(e) {
    if (kept(e)) return;
    for (const a of ATTRS) {
      const v = e.getAttribute(a);
      if (!v || !HE.test(v)) continue;
      const t = tr(v.replace(/\s+/g, ' ').trim());
      if (t != null && t !== v) e.setAttribute(a, t);
    }
    if (LTR && e.getAttribute('dir') === 'rtl') e.setAttribute('dir', 'ltr');
    if (e.getAttribute('lang') === 'he') e.setAttribute('lang', D.lang);
  }
  function walk(root) {
    if (root.nodeType === 3) { doText(root); return; }
    if (root.nodeType !== 1) return;
    doEl(root);
    const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, null);
    let n;
    while ((n = w.nextNode())) { if (n.nodeType === 3) doText(n); else doEl(n); }
  }
  const mo = new MutationObserver((list) => {
    for (const m of list) {
      if (m.type === 'childList') m.addedNodes.forEach(walk);
      else if (m.type === 'characterData') doText(m.target);
      else if (m.type === 'attributes') doEl(m.target);
    }
  });
  const start = () => {
    walk(document.body);
    mo.observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS.concat(['dir', 'lang']) });
  };
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
})();
