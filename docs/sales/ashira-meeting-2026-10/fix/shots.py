import os
from playwright.sync_api import sync_playwright
H=os.path.dirname(os.path.abspath(__file__))
spots=[("step2","השלב השני הוא"),("floors","קומה נמוכה יכולה להתאים")]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for tag,src in (("before","file"),("after","live")):
        pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2)
        if src=="file":
            html=open(os.path.join(H,"live-before.html"),encoding="utf-8").read().replace("<head>","<head><base href='https://nad-lan.co.il/projects/ashira-sde-dov/'>",1)
            pg.set_content(html,wait_until="domcontentloaded",timeout=90000)
        else:
            pg.goto("https://nad-lan.co.il/projects/ashira-sde-dov/?nlv=1",wait_until="domcontentloaded",timeout=90000)
        pg.wait_for_timeout(4000)
        for name,txt in spots:
            loc=pg.get_by_text(txt).first
            try:
                loc.scroll_into_view_if_needed(timeout=15000); pg.wait_for_timeout(600)
                box=loc.bounding_box(); y=max(0,box["y"]-120)
                pg.screenshot(path=os.path.join(H,f"shot-{tag}-{name}.png"),clip={"x":0,"y":y,"width":390,"height":700})
                print(tag,name,"ok")
            except Exception as e: print(tag,name,"fail",str(e)[:80])
        pg.close()
    b.close()
