# -*- coding: utf-8 -*-
"""HAD-390, ConsultBand (design system v104.25): the exact text changes, one source for the local probe (applied to the page's
HTML, the inline PHP output) and for the PHP files (applied by `python consult_band_396.py --apply`). Single-line anchors, each
present once in the PHP file and once in the live page (counted in the saved live source)."""

CSS_ANCHOR = "html body #nlcta.is-cone{bottom:calc(env(safe-area-inset-bottom,0px) + var(--nlcta-lift,150px))!important}"
CSS_ADD = (CSS_ANCHOR + "\n"
    "/* ConsultBand (design system v104.25, HAD-390, 2.10.2026): on a 3D-world page (.nlps-stage--world) up to 1023px, the bar and\n"
    "   the accessibility button share a band of their own at the foot of the screen: the bar held its corner by rising over the nearest\n"
    "   free slot between buttons, and text is no obstacle, so it parked on the price, the facts and the example link. The page keeps\n"
    "   the height of the band at its end; nothing rises over the reading area; from 1024px the bar floats in its corner as before. */\n"
    "@media(max-width:1023px){"
    "body:has(.nlps-stage--world){padding-bottom:calc(72px + env(safe-area-inset-bottom,0px))!important}"
    "html body:has(.nlps-stage--world) #nlcta,html body:has(.nlps-stage--world) #nlcta.is-clear,html body:has(.nlps-stage--world) #nlcta.is-cone"
    "{left:0!important;right:0!important;bottom:0!important;display:flex;justify-content:flex-end;align-items:center;box-sizing:border-box;"
    "padding:8px 14px calc(8px + env(safe-area-inset-bottom,0px));padding-inline-start:80px;background:#FAF7F1;border-top:1px solid #E2DCD0;"
    "box-shadow:0 -6px 18px rgba(27,26,23,.07)}"
    "html body:has(.nlps-stage--world) #nlcta .nlcta-wa{max-width:min(100%,360px)!important;box-shadow:none}"
    "html body:has(.nlps-stage--world) #nla11y{bottom:calc(8px + env(safe-area-inset-bottom,0px))!important;transform:none!important}}")

JS_ANCHOR = "tick=false;"
JS_ADD = ("tick=false;"
    "if(window.innerWidth<=1023&&document.querySelector('.nlps-stage--world')){box.classList.remove('is-clear','is-cone');box.style.removeProperty('--nlcta-lift');return;}"
    "/* ConsultBand v104.25: a world page up to 1023px keeps the bar in its own band, no lifts */")

A11Y_ANCHOR = "      if (pan && !pan.hidden) return;"
A11Y_ADD = (A11Y_ANCHOR + " if (innerWidth <= 1023) { if (lift) { lift = 0; box.style.transform = ''; } return; } // ConsultBand (v104.25): the band holds the button")

# (name, old, new): applied to the page HTML by band_probe.py --local
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
