# -*- coding: utf-8 -*-
"""HAD-390, ConsultBand (design system v104.25, revision 2 after Maya's QA of 2.10): the exact text changes, one source for the
local route-swap test (applied to the page's HTML, the inline PHP output) and for the PHP files (`--apply`; the runner applies
the same hunks to the LIVE text). Single-line anchors, each present once in its PHP file and once in the live page.

One owner for the floating layout: the CSS. On a 3D-world page (.nlps-stage--world), at every width, the "ייעוץ חינם" bar and the
accessibility button share an opaque band at the foot of the screen, and the CSS sets --nlcta-band:1 on the body. Both scripts that
used to move them (the bar's lift in conversion-cta.php, AccessibleCorner in project-stage.php) read that one variable and stand
still, so two systems with fixed collision lists no longer decide on their own. The sticky 3D on a wide stage loses the band's
height, so nothing at its foot sits under the band for good. Elsewhere nothing changes (the variable is empty)."""

CSS_ANCHOR = "html body #nlcta.is-cone{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}"
CSS_ADD = (CSS_ANCHOR + "\n"
    "/* ConsultBand (design system v104.25, HAD-390, 2.10.2026): on a 3D-world page (.nlps-stage--world), at every width, the bar and\n"
    "   the accessibility button share a band of their own at the foot of the screen. The bar used to hold its corner by rising to the\n"
    "   nearest free slot between buttons, and text was no obstacle, so it parked on the price, the facts and the apartment button.\n"
    "   The CSS owns the layout: --nlcta-band:1 tells both scripts to stand still. The page keeps the height of the band at its end,\n"
    "   and the sticky 3D of a wide stage ends above the band. Keyboard focus and in-page links scroll with the band in mind\n"
    "   (scroll-padding-bottom; Maya, 2.10: a native Tab put the apartment button half under the band) and with the sticky header in\n"
    "   mind (scroll-padding-top 77px = the tallest measured header, 69px, plus air; R3: Shift+Tab had put it under the header). */\n"
    "body:has(.nlps-stage--world){--nlcta-band:1;padding-bottom:calc(72px + env(safe-area-inset-bottom,0px))!important}"
    "html:has(.nlps-stage--world){scroll-padding-bottom:calc(84px + env(safe-area-inset-bottom,0px));scroll-padding-top:77px}"
    "html:has(body.admin-bar .nlps-stage--world){scroll-padding-top:123px}"
    "html body:has(.nlps-stage--world) #nlcta,html body:has(.nlps-stage--world) #nlcta.is-clear,html body:has(.nlps-stage--world) #nlcta.is-cone"
    "{left:0!important;right:0!important;bottom:0!important;display:flex;justify-content:flex-end;align-items:center;box-sizing:border-box;"
    "padding:8px 14px calc(8px + env(safe-area-inset-bottom,0px));padding-inline-start:80px;background:#FAF7F1;border-top:1px solid #E2DCD0;"
    "box-shadow:0 -6px 18px rgba(27,26,23,.07)}"
    "html body:has(.nlps-stage--world) #nlcta .nlcta-wa{max-width:min(100%,360px)!important;box-shadow:none}"
    "html body:has(.nlps-stage--world) #nla11y{bottom:calc(8px + env(safe-area-inset-bottom,0px))!important;transform:none!important}"
    "@media(min-width:521px){html body:has(.nlps-stage--world) #nlcta{padding-inline-end:20px;padding-inline-start:88px}}"
    "html body:has(.nlps-stage--world) .nlw.nlw--docked.nlw--side{height:clamp(440px,calc(100svh - 168px - env(safe-area-inset-bottom,0px)),760px)}")

BAND_JS = "getComputedStyle(document.body).getPropertyValue('--nlcta-band').trim()==='1'"
JS_ANCHOR = "tick=false;"
JS_ADD = ("tick=false;"
    "if(" + BAND_JS + "){box.classList.remove('is-clear','is-cone');box.style.removeProperty('--nlcta-lift');return;}"
    "/* ConsultBand v104.25: the band (CSS) owns the bar's place on this page, no lifts */")

A11Y_ANCHOR = "      if (pan && !pan.hidden) return;"
A11Y_ADD = (A11Y_ANCHOR + " if (" + BAND_JS.replace("==='1'", " === '1'") + ") { if (lift) { lift = 0; box.style.transform = ''; } return; }"
    " // ConsultBand (v104.25): the band at the foot holds the button")

# (name, old, new): applied to the page HTML by the route-swap probes (scripts/qa/had-390)
HTML_HUNKS = [("css", CSS_ANCHOR, CSS_ADD), ("js", JS_ANCHOR, JS_ADD), ("a11y", A11Y_ANCHOR, A11Y_ADD)]
# (relative plugin path, old, new): applied to the PHP files
PHP_HUNKS = [("inc/conversion-cta.php", CSS_ANCHOR, CSS_ADD), ("inc/conversion-cta.php", JS_ANCHOR, JS_ADD),
             ("inc/project-stage.php", A11Y_ANCHOR, A11Y_ADD)]


if __name__ == "__main__":
    # python consult_band_396.py --apply: the branch files (local); the runner applies the same hunks to the LIVE text
    import io, os, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    PLUG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config")
    if "--apply" not in sys.argv:
        raise SystemExit("usage: python consult_band_396.py --apply")
    texts = {}
    for rel, old, new in PHP_HUNKS:
        p = os.path.join(PLUG, *rel.split("/"))
        t = texts.get(p) or io.open(p, encoding="utf-8", newline="").read()
        if new in t:
            print("already applied:", rel, old[:40]); texts[p] = t; continue
        if t.count(old) != 1:
            raise SystemExit("FATAL: %s: the anchor %r is there %d times" % (rel, old[:50], t.count(old)))
        texts[p] = t.replace(old, new)
    for p, t in texts.items():
        io.open(p, "w", encoding="utf-8", newline="").write(t)
        print("written:", os.path.relpath(p, PLUG))
