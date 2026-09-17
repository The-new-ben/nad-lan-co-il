"""Flat, poster-style SVG scenes for the Meital Katzir broker canvas.
Illustrations only: generic coast, towers and villas, never a depiction of a real listing."""
import random, itertools
_ids = itertools.count(1)

def _sky(W, H, stops):
    gid = f"sky{next(_ids)}"
    st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return gid, f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">{st}</linearGradient></defs>'

DUSK = dict(t='#133240', m='#183F4D', l='#21505F', g='#2F6F86', hz='#CFE3EA', hzo=.5, sun='#EEE9DD',
            sea='#0C1F26', wv='#CFE3EA', wvo=.14, land='#0A1A20', b='#0A1A20', far='#1B4553', win='#EEE9DD', wino=.72, pool='#3E8AA3')
DAY = dict(t='#D5E7EC', m='#DEECF0', l='#E7F1F4', g='#CFE3EA', hz='#2F6F86', hzo=.35, sun='#FFFFFF',
           sea='#2F6F86', wv='#FFFFFF', wvo=.26, land='#1F4B5C', b='#1F4B5C', far='#9CC3CF', win='#E8F1F3', wino=.5, pool='#CFE3EA')

def _r(x, y, w, h, fill, op=None):
    o = f' fill-opacity="{op}"' if op is not None else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{o}/>'

def _line(x1, y1, x2, y2, stroke, op, sw=1):
    return f'<path d="M{x1:.1f} {y1:.1f}H{x2:.1f}" stroke="{stroke}" stroke-opacity="{op}" stroke-width="{sw}" fill="none"/>'

def _palm(x, base, top, color, lean=6):
    tx = x + lean
    s = [f'<path d="M{x:.1f} {base:.1f} Q{x+lean*0.2:.1f} {(base+top)/2:.1f} {tx:.1f} {top:.1f}" stroke="{color}" stroke-width="2.4" fill="none" stroke-linecap="round"/>']
    for dx, dy in ((-22, 8), (-16, -8), (0, -14), (16, -9), (22, 7), (-10, 12), (11, 13)):
        s.append(f'<path d="M{tx:.1f} {top:.1f} Q{tx+dx*0.55:.1f} {top+dy*0.35-6:.1f} {tx+dx:.1f} {top+dy:.1f}" stroke="{color}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    return ''.join(s)

def _windows(rng, x, y, w, h, P, rows_step=9, cols=4, lit=0.22):
    out = []
    cw = w / cols
    yy = y + 6
    while yy < y + h - 6:
        for c in range(cols):
            if rng.random() < lit:
                out.append(_r(x + c * cw + cw * 0.28, yy, cw * 0.44, 3.2, P['win'], P['wino']))
        yy += rows_step
    return ''.join(out)

def _slabs(x, y, w, h, P, step=11, over=3):
    out = []
    yy = y + step
    while yy < y + h - 2:
        out.append(_line(x - over, yy, x + w + over, yy, P['win'], 0.16, 1))
        yy += step
    return ''.join(out)

def _base(P, W=400, H=240, hz=176, sun_x=86, dusk=True):
    gid, defs = _sky(W, hz, [(0, P['t']), (0.55, P['m']), (0.9, P['l']), (1, P['g'])])
    s = [defs, f'<rect x="0" y="0" width="{W}" height="{hz}" fill="url(#{gid})"/>']
    if dusk:
        s.append(f'<circle cx="{sun_x}" cy="{hz}" r="44" fill="{P["sun"]}" fill-opacity=".07"/>')
        s.append(f'<path d="M{sun_x-20} {hz} A20 20 0 0 1 {sun_x+20} {hz} Z" fill="{P["sun"]}"/>')
    else:
        s.append(f'<circle cx="{sun_x}" cy="{hz*0.36:.0f}" r="13" fill="{P["sun"]}" fill-opacity=".95"/>')
    s.append(_r(0, hz, W, H - hz, P['sea']))
    s.append(f'<path d="M0 {hz}H{W}" stroke="{P["hz"]}" stroke-opacity="{P["hzo"]}" stroke-width="1"/>')
    for i, yy in enumerate((hz + 13, hz + 29, hz + 47)):
        s.append(f'<path d="M0 {yy} C {W*0.18:.0f} {yy-3}, {W*0.34:.0f} {yy+3}, {W*0.5:.0f} {yy} S {W*0.82:.0f} {yy-3}, {W} {yy}" stroke="{P["wv"]}" stroke-opacity="{P["wvo"] - i*0.03:.2f}" fill="none"/>')
    if dusk:
        for i, (dy, half) in enumerate(((7, 16), (15, 11), (24, 7), (34, 4))):
            s.append(f'<path d="M{sun_x-half} {hz+dy}H{sun_x+half}" stroke="{P["sun"]}" stroke-opacity="{0.5 - i*0.11:.2f}" stroke-width="1.6"/>')
    return s

def plate(kind, mode, seed='x'):
    """400x240 listing plate. kind: estate, twin, boutique, penthouse, lowrise, complex."""
    P = DUSK if mode == 'dusk' else DAY
    rng = random.Random(seed)
    s = _base(P, dusk=(mode == 'dusk'))
    land = f'<path d="M150 192 L400 192 L400 240 L128 240 Z" fill="{P["land"]}"/>'
    b = P['b']
    if kind == 'estate':
        s.append(land)
        s.append(_palm(192, 198, 118, b, 5))
        s.append(_r(208, 156, 166, 40, b))
        s.append(_r(228, 126, 150, 4, b))
        s.append(_r(238, 130, 132, 26, b))
        s.append(_r(222, 166, 54, 20, P['win'], P['wino']))
        s.append(_r(286, 166, 76, 20, P['win'], P['wino'] * 0.55))
        s.append(_r(252, 136, 104, 14, P['win'], P['wino'] * 0.8))
        s.append(_r(196, 204, 160, 7, P['pool'], .85))
        s.append(_palm(386, 198, 132, b, -6))
    elif kind == 'twin':
        s.append(land)
        s.append(_r(168, 98, 22, 98, P['far']))
        s.append(_r(356, 108, 28, 88, P['far']))
        s.append(_r(210, 176, 150, 20, b))
        s.append(_r(226, 42, 48, 154, b)); s.append(_r(233, 33, 34, 9, b))
        s.append(_r(292, 64, 46, 132, b)); s.append(_r(299, 57, 32, 7, b))
        s.append(_windows(rng, 226, 42, 48, 130, P, 8, 4, 0.2))
        s.append(_windows(rng, 292, 64, 46, 110, P, 8, 4, 0.18))
    elif kind in ('boutique', 'penthouse'):
        s.append(land)
        s.append(_r(176, 138, 36, 58, P['far']))
        s.append(_r(348, 124, 42, 72, P['far']))
        s.append(_r(230, 90, 100, 106, b))
        s.append(_slabs(230, 90, 100, 106, P, 12, 4))
        s.append(_windows(rng, 230, 90, 100, 100, P, 12, 5, 0.2))
        if kind == 'penthouse':
            s.append(_r(236, 62, 92, 4, b))
            s.append(_r(244, 66, 76, 24, P['win'], P['wino'] * 0.75))
            for mx in (263, 282, 301):
                s.append(_r(mx, 66, 2, 24, b))
        else:
            s.append(_r(246, 74, 68, 16, b))
            s.append(_r(240, 71, 80, 3, b))
    elif kind == 'lowrise':
        s.append(land)
        s.append(_r(194, 138, 80, 58, b)); s.append(_slabs(194, 138, 80, 58, P, 12, 3))
        s.append(_r(284, 122, 66, 74, b)); s.append(_slabs(284, 122, 66, 74, P, 12, 3))
        s.append(_r(290, 108, 54, 14, P['win'], P['wino'] * 0.6))
        s.append(_r(358, 150, 42, 46, b))
        s.append(_windows(rng, 194, 138, 80, 52, P, 12, 4, 0.22))
        s.append(_windows(rng, 284, 122, 66, 70, P, 12, 3, 0.22))
        for cx, cy, rr in ((180, 184, 12), (352, 188, 9)):
            s.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{b}"/>')
    elif kind == 'complex':
        s.append(land)
        s.append(_r(198, 112, 54, 84, b)); s.append(_slabs(198, 112, 54, 84, P, 11, 3))
        s.append(_r(262, 94, 60, 102, b)); s.append(_slabs(262, 94, 60, 102, P, 11, 3))
        s.append(_r(332, 120, 50, 76, b)); s.append(_slabs(332, 120, 50, 76, P, 11, 3))
        s.append(_windows(rng, 262, 94, 60, 96, P, 11, 4, 0.2))
        s.append(_r(208, 205, 132, 6, P['pool'], .9))
        s.append(_palm(188, 200, 142, b, 4))
        s.append(_palm(392, 200, 150, b, -4))
    return '<svg viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" style="display: block;" aria-hidden="true">' + ''.join(s) + '</svg>'

def estate_night(W=760, H=600):
    """Signature plate: a modernist villa at blue hour, pool light, palms."""
    P = DUSK
    hz = 360
    gid, defs = _sky(W, hz, [(0, '#0E232C'), (0.45, '#133240'), (0.8, '#1B4452'), (0.96, '#28596B'), (1, '#2F6F86')])
    s = [defs, f'<rect x="0" y="0" width="{W}" height="{hz}" fill="url(#{gid})"/>']
    s.append(f'<circle cx="150" cy="118" r="17" fill="#EEE9DD" fill-opacity=".92"/>')
    s.append(f'<circle cx="150" cy="118" r="46" fill="#EEE9DD" fill-opacity=".05"/>')
    s.append(_r(0, hz, W, H - hz, '#0C1F26'))
    s.append(f'<path d="M0 {hz}H{W}" stroke="#CFE3EA" stroke-opacity=".45"/>')
    s.append(f'<path d="M0 470 L{W} 430 L{W} {H} L0 {H} Z" fill="#081519"/>')
    # villa volumes
    s.append(_r(214, 318, 470, 122, '#081519'))
    s.append(_r(300, 250, 400, 8, '#081519'))
    s.append(_r(318, 258, 360, 62, '#081519'))
    s.append(_r(244, 344, 150, 76, '#EAD9B2', .9))
    s.append(_r(410, 344, 250, 76, '#EAD9B2', .42))
    s.append(_r(346, 270, 300, 36, '#EAD9B2', .66))
    s.append(_r(262, 506, 110, 3, '#EAD9B2', .3))
    s.append(_r(440, 512, 150, 2, '#EAD9B2', .16))
    for mx in (294, 344, 470, 530, 590):
        s.append(_r(mx, 344, 3, 76, '#081519'))
    for mx in (406, 466, 526, 586):
        s.append(_r(mx, 270, 3, 36, '#081519'))
    s.append(_r(214, 440, 480, 6, '#081519'))
    # pool and its light
    s.append(_r(236, 470, 420, 34, '#2F6F86', .95))
    s.append(_r(236, 470, 420, 4, '#CFE3EA', .55))
    for i, yy in enumerate((482, 490, 497)):
        s.append(f'<path d="M{262+i*14} {yy}H{628-i*18}" stroke="#E8F1F3" stroke-opacity="{0.34 - i*0.09:.2f}" stroke-width="1.5"/>')
    s.append(_palm(160, 470, 250, '#081519', 10).replace('stroke-width="2.4"', 'stroke-width="5"').replace('stroke-width="2"', 'stroke-width="3.2"'))
    s.append(_palm(712, 452, 290, '#081519', -8).replace('stroke-width="2.4"', 'stroke-width="4.4"').replace('stroke-width="2"', 'stroke-width="3"'))
    s.append(f'<path d="M0 560 C 180 552, 380 566, 760 556" stroke="#CFE3EA" stroke-opacity=".08" fill="none"/>')
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" style="display: block;" aria-hidden="true">' + ''.join(s) + '</svg>'

def skyline(x0, x1, base, rng, fill, far, win, max_h=190):
    if x1 - x0 < 20:
        return ''
    out = []
    x = x0
    while x < x1:
        w = rng.choice((16, 20, 24, 28, 34, 40))
        h = min(max_h, rng.choice((40, 60, 76, 96, 120, 150, 176, 190)))
        if rng.random() < 0.35:
            out.append(_r(x + 6, base - h * 0.7, w * 0.8, h * 0.7, far))
        out.append(_r(x, base - h, w, h, fill))
        if h > 90:
            out.append(_r(x + w * 0.2, base - h - 6, w * 0.6, 6, fill))
            for yy in range(int(base - h + 10), int(base - 8), 11):
                if rng.random() < 0.28:
                    out.append(_r(x + w * 0.3, yy, w * 0.4, 3, win, .5))
        x += w + rng.choice((2, 4, 6, 10))
    out.append(_r(x0 - 10, base - 14, x1 - x0 + 20, 14, fill))
    return ''.join(out)

def hero_scene(W=1440, H=880, hz=700, sun_x=640, sky_x0=40, sky_x1=520, mirror=False, seed='hero', sun_r=58, max_h=190):
    rng = random.Random(seed)
    gid, defs = _sky(W, hz, [(0, '#0D222B'), (0.4, '#10262F'), (0.72, '#163846'), (0.9, '#1E4A5A'), (0.985, '#2A6275'), (1, '#2F6F86')])
    s = [defs, f'<rect x="0" y="0" width="{W}" height="{hz}" fill="url(#{gid})"/>']
    g = []
    g.append(f'<circle cx="{sun_x}" cy="{hz}" r="{sun_r*2.6:.0f}" fill="#EEE9DD" fill-opacity=".05"/>')
    g.append(f'<circle cx="{sun_x}" cy="{hz}" r="{sun_r*1.6:.0f}" fill="#EEE9DD" fill-opacity=".06"/>')
    g.append(f'<path d="M{sun_x-sun_r} {hz} A{sun_r} {sun_r} 0 0 1 {sun_x+sun_r} {hz} Z" fill="#EEE9DD"/>')
    g.append(skyline(sky_x0, sky_x1, hz, rng, '#0A1A20', '#163743', '#EEE9DD', max_h))
    s.append(''.join(g) if not mirror else f'<g transform="translate({W} 0) scale(-1 1)">' + ''.join(g) + '</g>')
    s.append(_r(0, hz, W, H - hz, '#0C1F26'))
    s.append(f'<path d="M0 {hz}H{W}" stroke="#CFE3EA" stroke-opacity=".5"/>')
    sx = W - sun_x if mirror else sun_x
    k = sun_r / 58
    for i, (dy, half) in enumerate(((12*k, 52*k), (26*k, 38*k), (42*k, 26*k), (60*k, 16*k), (80*k, 8*k))):
        s.append(f'<path d="M{sx-half:.1f} {hz+dy:.1f}H{sx+half:.1f}" stroke="#EEE9DD" stroke-opacity="{0.5 - i*0.09:.2f}" stroke-width="2"/>')
    for i, yy in enumerate((hz + 30, hz + 70, hz + 120, hz + 160)):
        if yy < H:
            s.append(f'<path d="M0 {yy} C {W*0.17:.0f} {yy-6}, {W*0.33:.0f} {yy+6}, {W*0.5:.0f} {yy} S {W*0.83:.0f} {yy-6}, {W} {yy}" stroke="#CFE3EA" stroke-opacity="{0.13 - i*0.02:.2f}" fill="none"/>')
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" width="100%" height="100%" style="display: block;" aria-hidden="true">' + ''.join(s) + '</svg>'

def card_scene(W=1050, H=600, hz=372, sun_x=250, mirror=False):
    gid, defs = _sky(W, hz, [(0, '#0E232C'), (0.5, '#122C37'), (0.85, '#1A4150'), (1, '#2A6275')])
    s = [defs, f'<rect x="0" y="0" width="{W}" height="{hz}" fill="url(#{gid})"/>']
    sx = W - sun_x if mirror else sun_x
    s.append(f'<circle cx="{sx}" cy="{hz}" r="90" fill="#EEE9DD" fill-opacity=".05"/>')
    s.append(f'<path d="M{sx-36} {hz} A36 36 0 0 1 {sx+36} {hz} Z" fill="#EEE9DD"/>')
    s.append(_r(0, hz, W, H - hz, '#0C1F26'))
    s.append(f'<path d="M0 {hz}H{W}" stroke="#CFE3EA" stroke-opacity=".55"/>')
    for i, (dy, half) in enumerate(((10, 30), (22, 20), (36, 12), (52, 6))):
        s.append(f'<path d="M{sx-half} {hz+dy}H{sx+half}" stroke="#EEE9DD" stroke-opacity="{0.46 - i*0.1:.2f}" stroke-width="1.6"/>')
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" style="display: block;" aria-hidden="true">' + ''.join(s) + '</svg>'
