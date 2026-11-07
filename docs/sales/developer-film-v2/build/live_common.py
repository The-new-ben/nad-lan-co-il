"""Shared bits for the read-only live captures (headless installed Chrome, analytics blocked in THIS browser only)."""
BLOCK = ("google-analytics.com", "googletagmanager.com", "hotjar.com", "hotjar.io", "clarity.ms", "facebook.net",
         "facebook.com/tr", "doubleclick.net", "tiktok", "linkedin")
CSS_STAGE = """
section#nlps { position: fixed !important; inset: 0 !important; width: 100vw !important; height: 100vh !important;
  max-width: none !important; max-height: none !important; margin: 0 !important; border-radius: 0 !important;
  border: 0 !important; outline: 0 !important; box-shadow: none !important; z-index: 2147483000 !important; }
section#nlps > * { border: 0 !important; border-radius: 0 !important; }
#nlcta, .nlcta, #wpadminbar, [class*="cookie"], [id*="cookie"], [class*="accessib"], [id*="accessib"] { display: none !important; }
html, body { overflow: hidden !important; }
section#nlps .rbs-qpin--project, section#nlps .rbs-leader { visibility: hidden !important; }
"""
EVENTS_JS = """() => { window.__ev = []; for (const n of ['nl:floor','nl:facing','nl:view','nl:floor-action','nl:floor-cta'])
  window.addEventListener(n, e => window.__ev.push({n, d: e.detail || null, t: performance.now()})); }"""


def launch(p, w, h, dpr=1, mobile=False):
    b = p.chromium.launch(channel="chrome", headless=True, args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, locale="he-IL", is_mobile=mobile, has_touch=mobile)
    ctx.route("**/*", lambda r: r.abort() if any(x in r.request.url for x in BLOCK) else r.continue_())
    return b, ctx
