# -*- coding: utf-8 -*-
"""HAD-390 R4 (design v104.34, Maya's measurement 3.10.2026 08:34 UTC): FocusInFreeScreen, one hunk in inc/conversion-cta.php.
On a 3D-world page a keyboard focus that lands under the sticky header or the WhatsApp band is moved into the free screen.
Chrome does not scroll a control that is already inside the window when it takes focus, whatever the scroll-padding says
(measured: a tower button focused at y 15-59 stayed under the 57 px header and its centre hit the logo). Keyboard only
(:focus-visible), never a tap or a finger scroll, never in full screen, never the band itself. The band keeps its size.
Applied to the LIVE text by the release runner (the anchor exactly once) and by --apply to the repo copy."""
import io, os, sys

ANCHOR = ("\t\tdocument.addEventListener('focusout',function(e){if(typing(e.target)){clearTimeout(back);back=setTimeout(function(){"
          "box.classList.remove('is-typing');fit();},700);}});\n")
ADD = ("\t\t// v104.34 (HAD-390 R4, Maya 3.10 08:34): on a 3D-world page a KEYBOARD focus that lands under the sticky header or under the band\n"
       "\t\t// is moved into the free screen. Chrome leaves a control that is already inside the window where it is, scroll-padding or not; the jump is instant, as the browser's own focus scroll is.\n"
       "\t\tif(document.querySelector('.nlps-stage--world')){document.addEventListener('focusin',function(e){var t=e.target;"
       "if(!t||!t.closest||t.closest('#nlcta,.nlw--full')){return;}var kb=false;try{kb=t.matches(':focus-visible');}catch(x){kb=false;}"
       "if(!kb){return;}setTimeout(function(){var r=t.getBoundingClientRect(),hd=document.querySelector('.nlhp-top'),"
       "top=hd?Math.max(0,hd.getBoundingClientRect().bottom):0,bot=box.getBoundingClientRect().top||window.innerHeight;"
       "if(r.top<top+8){window.scrollBy({top:r.top-top-16,left:0,behavior:'instant'});}else if(r.bottom>bot-8){window.scrollBy({top:r.bottom-bot+16,left:0,behavior:'instant'});}},0);});}\n")


def apply(txt):
    if txt.count(ANCHOR) != 1:
        raise SystemExit("cc_r4: the focusout anchor is there " + str(txt.count(ANCHOR)) + " times")
    if "HAD-390 R4" in txt:
        raise SystemExit("cc_r4: the R4 focus reveal is already there")
    return txt.replace(ANCHOR, ANCHOR + ADD)


if __name__ == "__main__" and "--apply" in sys.argv:
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "inc", "conversion-cta.php")
    t = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in t
    t = apply(t.replace("\r\n", "\n"))
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("applied to the repo copy")
