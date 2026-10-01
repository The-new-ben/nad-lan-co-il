# -*- coding: utf-8 -*-
"""v104.20 (1.10.2026, the V2 loop turn 4, V4's first parity step; HAD-380): the apartment's basket from the 3D world.
The fleet's basket (assets/basket/basket.js, BasketOne v86: the apartment, the style, a team of real professionals, the full price
with purchase tax, then the representative on WhatsApp or the shared viewing room) was loaded on the Kikar page and heard its
nl:floor / nl:facing, but had no way in: it mounts its button on the fleet stage's steps and view band, which the world page has
not. Now, once an apartment is chosen, a terracotta "לסל הדירה" button sits under its deals (Hebrew, where the basket runs) and
opens the basket; nl:facing carries the apartment's own words ({label}) so the basket names it. No other page changes.
  python patch_world_10420.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "project-stage", "world")
JS, CSS = os.path.join(D, "world.js"), os.path.join(D, "world.css")
s = open(JS, encoding="utf-8").read()
css = open(CSS, encoding="utf-8").read()
if "v104.20" in s or "v104.20" in css:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


sub("""    dealsWhat: (n, r, a, f0, f1) => `${n} עסקאות · ${r} חדרים, ${a} מ״ר · קומות ${f0}–${f1}`, ppm: (x) => `כ-${x} ₪ למ״ר`,""",
    """    dealsWhat: (n, r, a, f0, f1) => `${n} עסקאות · ${r} חדרים, ${a} מ״ר · קומות ${f0}–${f1}`, ppm: (x) => `כ-${x} ₪ למ״ר`,
    basket: 'לסל הדירה: המחיר המלא, הצוות והנציג', // v104.20 (the basket runs on the Hebrew pages only)""", "basket word")
# the button under the deals; only where the basket runs
sub("""${u == null ? '' : dealsHtml(rng)}${views}${seg}` +""",
    """${u == null ? '' : dealsHtml(rng) + basketHtml()}${views}${seg}` +""", "basket place")
sub("""  function bindPlan() {
    if (!ui.panel) return;""", """  // v104.20 (V4): the apartment's basket (assets/basket/basket.js): the full price, a team and the representative
  const basketHtml = () => (T.basket && window.__nlBasket ? `<button class="nlw-btn nlw-btn--bk" type="button" data-basket><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h14l-1.4 8.2a1.5 1.5 0 0 1-1.5 1.3H5.9a1.5 1.5 0 0 1-1.5-1.3L3 6Z"/><path d="M7 6V4.8a3 3 0 0 1 6 0V6"/></svg><span>${esc(T.basket)}</span></button>` : '');
  function bindPlan() {
    if (!ui.panel) return;
    ui.panel.querySelectorAll('[data-basket]').forEach((b) => b.addEventListener('click', () => { if (window.__nlBasket) { emitFacing('user'); window.__nlBasket.open(b); } }));""", "basket bind")
# nl:facing carries the apartment's own words
sub("""    const detail = { tower: S.tower, floor: S.floor, heightM: +eyeH(S.floor).toFixed(1), bearing: Math.round(b), facing: dirWord(b), source };
    setPick();
    window.dispatchEvent(new CustomEvent('nl:facing', { detail }));""",
    """    const detail = { tower: S.tower, floor: S.floor, heightM: +eyeH(S.floor).toFixed(1), bearing: Math.round(b), facing: dirWord(b), source };
    if (S.apt != null && PLAN()) detail.label = aptName(S.tower, S.floor, S.apt); // v104.20: the basket names it
    setPick();
    window.dispatchEvent(new CustomEvent('nl:facing', { detail }));""", "facing label")
open(JS, "w", encoding="utf-8", newline="\n").write(s)
css = css.rstrip("\n") + "\n\n" + """/* v104.20 (V4): the apartment's basket, the money action (terracotta), under the deals */
.nlw-btn--bk { width: 100%; margin-top: 10px; display: flex; align-items: center; justify-content: center; gap: 8px; background: var(--nlw-terra); color: #fff; border-color: var(--nlw-terra); min-height: 46px; font-weight: 700; }
.nlw-btn--bk svg { width: 18px; height: 18px; flex: none; }
.nlw-btn--bk:hover { filter: brightness(1.06); }
"""
open(CSS, "w", encoding="utf-8", newline="\n").write(css)
print("world.js + world.css patched (v104.20)")
