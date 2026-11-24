"""Aurelia showroom (HAD-810): flats.json for the cockpit, from the Blender model v2 units + the viewer cards (sample rooms/status).
python scripts/aurelia/build_flats.py

Building size (Ben, 23.11.2026): 47 floors, 320 flats. Those two numbers are the building's declared size and are the only size the
data names (block `building`). The sample flats below are the concept model's unit volumes (floors 6-46) plus floor 47, the top floor,
which repeats the 6-room sample layout of floor 46 (Ben's 47th floor; the model v2 was built with 46). Floors 1-5 of the tower stand in
the podium and carry no flat in the model: the floor stepper starts at 6, nothing is said about their use.
The script checks: the declared size is 47 / 320, every residential floor 6..47 has a sample flat, and it prints how many sample flats
the data holds (the sample is not the building's size and no visible label prints it)."""
import json, collections, sys
OBJ = 'D:/Media/Aurelia/v2/aurelia-objects-v2.json'
CARDS = 'plugins/nadlan-config/assets/aurelia-viewer/data.json'
OUT = 'plugins/nadlan-config/assets/aurelia-viewer/flats.json'
FLOORS, FLATS, FIRST_RES, FLOOR_H = 47, 320, 6, 3.3
d = json.load(open(OBJ, encoding='utf-8'))
U = [o for c in d['collections'] if c['name'] == 'UNITS' for o in c['objects']]
cards = json.load(open(CARDS, encoding='utf-8'))['cards']
byflat = {}
for g, c in cards.items():
    if c.get('flat'):
        byflat.setdefault(c['flat'], c)
X0, X1, Y0, Y1 = 2.0, 28.0, 40.0, 84.0
out = []
for u in sorted(U, key=lambda o: (o['floor'], o['unit'])):
    (x0, y0, z0), (x1, y1, z1) = u['bbox_min'], u['bbox_max']
    if x0 <= X0 + .01: b, w, dp = 270, y1 - y0, x1 - x0
    elif x1 >= X1 - .01: b, w, dp = 90, y1 - y0, x1 - x0
    elif y0 <= Y0 + .01: b, w, dp = 180, x1 - x0, y1 - y0
    else: b, w, dp = 0, x1 - x0, y1 - y0
    c = byflat.get(u['id'], {})
    rooms = c.get('rooms') or (6 if u['area_m2'] > 300 else 5 if u['area_m2'] > 125 else 4 if u['area_m2'] > 100 else 2)
    out.append({'id': '%d-%d' % (u['floor'], u['unit']), 'f': u['floor'], 'u': u['unit'], 'a': round(u['area_m2'], 1), 'r': rooms,
                'b': b, 'w': round(w, 2), 'd': round(dp, 2), 'z': round(z0, 2), 'st': c.get('status', 'free'), 'sea': b == 270,
                'flat': u['id'], 'k': [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)]})
# floor 47 (the top floor): the 6-room sample of floor 46, one floor higher; no picture of the tower shows it, the stepper reaches it
top = max(f['f'] for f in out)
for f in [x for x in out if x['f'] == top]:
    for fl in range(top + 1, FLOORS + 1):
        n = dict(f, id='%d-%d' % (fl, f['u']), f=fl, z=round(f['z'] + (fl - top) * FLOOR_H, 2), flat='AUR-SAMPLE_%d_%d' % (fl, f['u']))
        out.append(n)
out.sort(key=lambda x: (x['f'], x['u']))
fl = sorted({f['f'] for f in out})
assert fl == list(range(FIRST_RES, FLOORS + 1)), 'residential floors with a sample flat: %s' % fl
assert len({f['id'] for f in out}) == len(out)
building = {'floors': FLOORS, 'flats': FLATS, 'res': [FIRST_RES, FLOORS],
            'note': 'גודל הבניין: 47 קומות ו-320 דירות. הדירות בקובץ הן דירות לדוגמה מהמודל, לא ספירת הדירות בבניין.'}
assert building['floors'] == 47 and building['flats'] == 320
json.dump({'note': 'קונספט. שטחים ומספרים מהמודל; חדרים וזמינות: נתוני דוגמה.', 'building': building,
           'origin': {'lat': 32.1100, 'lng': 34.7845, 'note': 'מיקום רעיוני'},
           'tower': {'x0': X0, 'x1': X1, 'y0': Y0, 'y1': Y1}, 'flats': out}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('building (declared, the only size the data names): %d floors, %d flats; residential floors %d-%d' % (FLOORS, FLATS, FIRST_RES, FLOORS))
print('sample flats in the data: %d (model units %d + floor 47: %d); the sample is NOT the building size' % (len(out), len(U), len(out) - len(U)))
print('sample flats per floor type:', dict(collections.Counter(collections.Counter(f['f'] for f in out).values())))
print('rooms:', dict(collections.Counter(f['r'] for f in out)), 'sides:', dict(collections.Counter(f['b'] for f in out)))
if len(out) != FLATS:
    print('NOTE: the concept model describes %d sample flats, the building has %d: the model is a sample, its floor layouts were not '
          're-drawn to reach %d (that would be a design decision, not data).' % (len(out), FLATS, FLATS))
