# -*- coding: utf-8 -*-
"""Shared bits of the v3 captures: the CDP screencast recorder (as in v2's capture_live.py) and the CSS that hides the
site's floating bars in a capture (this browser only)."""
import base64, json, os

HIDE = ("#nlcta, .nlcta, #wpadminbar, [class*='cookie'], [id*='cookie'], [class*='accessib'], [id*='accessib'], "
        ".nl-a11y, #nla11y, .nla11y { display: none !important; }")


class Cast:
    """CDP screencast: every painted frame (JPEG) with its timestamp -> <folder>/c_00001.jpg ... + frames.json"""
    def __init__(self, page, folder, w, h):
        self.c = page.context.new_cdp_session(page); self.folder = folder; self.n = 0; self.log = []
        os.makedirs(folder, exist_ok=True)
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
        self.c.on("Page.screencastFrame", self.frame)
        self.w, self.h = w, h

    def frame(self, p):
        self.n += 1
        fn = os.path.join(self.folder, "c_%05d.jpg" % self.n)
        open(fn, "wb").write(base64.b64decode(p["data"]))
        self.log.append({"f": os.path.basename(fn), "t": p["metadata"]["timestamp"]})
        try:
            self.c.send("Page.screencastFrameAck", {"sessionId": p["sessionId"]})
        except Exception:
            pass

    def start(self):
        self.c.send("Page.startScreencast", {"format": "jpeg", "quality": 90, "maxWidth": self.w, "maxHeight": self.h, "everyNthFrame": 1})

    def mark(self, label):
        """a named moment in the cast (time of the last frame)"""
        self.log.append({"mark": label, "t": self.log[-1]["t"] if self.log and "t" in self.log[-1] else 0, "after": self.n})

    def stop(self):
        self.c.send("Page.stopScreencast")
        json.dump(self.log, open(os.path.join(self.folder, "frames.json"), "w"), indent=0)


# the site's sticky top bar would sit over element screenshots: hidden in the capture browser only
HIDE_STICKY_JS = """() => { for (const e of document.querySelectorAll('header, .wp-site-blocks > *, body > div')) { const p = getComputedStyle(e).position;
    const r = e.getBoundingClientRect();
    if ((p === 'sticky' || p === 'fixed') && r.top < 5 && r.height < 200 && r.width > 300) e.style.setProperty('display', 'none', 'important'); } }"""
