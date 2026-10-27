import json, os, textwrap
from PIL import Image, ImageDraw, ImageFont
SH = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\kochav-ph\research-2026-10-27\shots"
OUT = r"C:\Users\777\nad-lan\nad-lan-co-il\docs\sales\kochav-ph\research-2026-10-27"
data = {}
for fn in ['bench-out.json','bench2-out.json','bench3-out.json','ours2.json']:
    for r in json.load(open(fn, encoding='utf-8')):
        data[(r['name'], r['width'])] = r
def price(name, w):
    r = data.get((name, w)); p = (r or {}).get('top', {}).get('price') if r else None
    return p
F = lambda s: ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", s)
FB = lambda s: ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", s)
INK = (14, 23, 38); MUTE = (90, 102, 120); BOX = (31, 111, 235); FOLD = (200, 30, 60)
pages = [
 ('00-nadlan-he', 'nad-lan.co.il (ours, HE, v1.72.537)', '18,000,000 NIS'),
 ('02-compass-432park', 'Compass - 432 Park Ave PH88, NYC', '$88.5M'),
 ('01-sothebys-nyc-crosby', "Sotheby's - 39 Crosby St PHN, NYC", '$25M'),
 ('07-sothebys-israel', "Sotheby's - duplex penthouse, Tel Aviv", '$29.5M / 91M NIS'),
 ('09-yad2-kochav', 'Yad2 - duplex, Levi Eshkol 2, Kochav HaTzafon', '20M NIS'),
]
notes390 = {
 '00-nadlan-he': 'photo 1/6 first, price under headline; WhatsApp pill covers facts row',
 '02-compass-432park': 'Floor Plan + Virtual Tour chips on photo; sticky Contact / Request a tour',
 '01-sothebys-nyc-crosby': 'video play on hero, 1/24, Floor Plan button; sticky Contact Agent',
 '07-sothebys-israel': 'video on hero; price in USD + NIS; sticky Contact Agent',
 '09-yad2-kochav': 'collage 1/15; monthly payment under price; WhatsApp in first screen',
}
notes1280 = {
 '00-nadlan-he': 'headline, 44px price, facts row, 2 CTAs beside a 1/6 photo card',
 '02-compass-432park': 'collage + chips; price 28px; facts; sticky agent card',
 '01-sothebys-nyc-crosby': 'video hero 1/24; price only 14px in strip; Contact Agent',
 '07-sothebys-israel': 'video hero 1/12; price 14px in strip (22px lower)',
 '09-yad2-kochav': 'collage, 32px price card, mortgage estimate',
}
def ptxt(name, w):
    p = price(name, w)
    if not p: return 'price: n/a'
    fold = 844 if w == 390 else 800
    return f"price y={p['y']}px · {int(p['fs'])}px · {'ABOVE fold' if p['y'] < fold else 'below fold'}"
# ---- phone board ----
cw, ch = 390, 844; pad = 18; capH = 118; titleH = 92
W = pad + len(pages) * (cw + pad); H = titleH + capH + ch + pad + 40
B = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(B)
d.text((pad, 18), 'First screen on a phone (390 x 844), 27 Oct 2026 - our page next to the 4 best of 13 benchmarked', fill=INK, font=FB(26))
d.text((pad, 56), 'Blue box = the asking price as measured in the page (CSS px from top). Overlays (cookie/sign-in prompts) hidden locally; raw shots kept in shots/.', fill=MUTE, font=F(17))
for i, (n, label, pr) in enumerate(pages):
    x = pad + i * (cw + pad); y0 = titleH
    d.text((x, y0), label, fill=INK, font=FB(17)); d.text((x, y0 + 26), pr, fill=INK, font=F(16))
    d.text((x, y0 + 50), ptxt(n, 390), fill=BOX, font=FB(15))
    d.multiline_text((x, y0 + 74), '\n'.join(textwrap.wrap(notes390[n], 56)[:2]), fill=MUTE, font=F(13), spacing=2)
    im = Image.open(os.path.join(SH, f'{n}-390.png')).convert('RGB').resize((cw, ch))
    dd = ImageDraw.Draw(im); p = price(n, 390)
    if p and p['y'] < 844:
        dd.rectangle([p['x'] - 4, p['y'] - 4, p['x'] + p['w'] + 4, p['y'] + p['h'] + 4], outline=BOX, width=3)
    B.paste(im, (x, y0 + capH)); d.rectangle([x - 1, y0 + capH - 1, x + cw, y0 + capH + ch], outline=(200, 205, 214))
d.text((pad, H - 32), 'Source: research-2026-10-27/BENCHMARK.md (all 13 pages, both widths). Yad2 phone shot is the raw first load (its cookie and Google prompts are part of the real first screen).', fill=MUTE, font=F(14))
B.save(os.path.join(OUT, 'board-390.png'))
# ---- desktop board (3 x 2 grid) ----
cw, ch = 760, 475; capH = 92; titleH = 92; cols = 3
W = pad + cols * (cw + pad); H = titleH + 2 * (capH + ch + pad) + 30
B = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(B)
d.text((pad, 18), 'First screen on a desktop (1280 x 800, shown at 59%), 27 Oct 2026 - our page next to the 4 best', fill=INK, font=FB(26))
d.text((pad, 56), 'Blue box = the asking price as measured. Fold = 800 px.', fill=MUTE, font=F(17))
sc = cw / 1280
for i, (n, label, pr) in enumerate(pages):
    cx = pad + (i % cols) * (cw + pad); cy = titleH + (i // cols) * (capH + ch + pad)
    d.text((cx, cy), label + '  ·  ' + pr, fill=INK, font=FB(17))
    d.text((cx, cy + 28), ptxt(n, 1280), fill=BOX, font=FB(15)); d.text((cx, cy + 52), notes1280[n], fill=MUTE, font=F(14))
    im = Image.open(os.path.join(SH, f'{n}-1280.png')).convert('RGB')
    dd = ImageDraw.Draw(im); p = price(n, 1280)
    if p and p['y'] < 800:
        dd.rectangle([p['x'] - 5, p['y'] - 5, p['x'] + p['w'] + 5, p['y'] + p['h'] + 5], outline=BOX, width=5)
    im = im.resize((cw, ch)); B.paste(im, (cx, cy + capH)); d.rectangle([cx - 1, cy + capH - 1, cx + cw, cy + capH + ch], outline=(200, 205, 214))
# legend cell
cx = pad + 2 * (cw + pad); cy = titleH + (capH + ch + pad)
lines = ['Across 13 benchmarked pages (both widths):', '',
 '- price above the fold: 10 of 12 on phone, 10 of 13 on desktop',
 '- median price position: y=534 phone, y=627 desktop',
 '- median price size: 22px phone, 28px desktop',
 '- rooms and/or size right under the price: 12 of 13',
 '- floor plan one tap from the first screen: 3 of 13',
 '  (Compass, Sotheby\'s NYC, Elliman); 0 of 6 Israeli pages',
 '- video on the first screen: 2 of 13 (both Sotheby\'s)',
 '- sticky or floating contact on phone: 9 of 12', '',
 'Ours now: price y=669 / 32px phone, y=452 / 44px desktop;',
 'no floor plan, video at y=2480 (phone), 6 photos in hero,',
 'H1 is visually hidden (1x1 px).']
for k, t in enumerate(lines):
    d.text((cx, cy + 6 + k * 27), t, fill=INK if k == 0 else (INK if not t.startswith('Ours') and k < 11 else BOX), font=FB(17) if k == 0 else F(16))
B.save(os.path.join(OUT, 'board-1280.png'))
print('boards ok')
