"""L09 on real WordPress (the bench's PHP 8.3 with its own image libraries), synthetic files only.

Uploads go straight to the server door /owner/photo (no browser shrink), so the server's own cleaning is what is
tested. The stored photo is read back through the owner-only proxy (full size) and compared:
  - metadata: no EXIF (no GPS IFD, no orientation), no XMP, no IPTC, no PNG text, no WebP EXIF/XMP chunks;
  - pixels: the stored image must equal Pillow's ImageOps.exif_transpose() of the original (what a viewer displays),
    by size and by a per-channel mean difference on a 32x32 reduction (JPEG re-encoding allowed), for all 8 EXIF
    orientations, built with an asymmetric pattern so a mirror or a turn cannot pass.
Also: too big (413), a renamed text file and a renamed executable (415), a corrupt JPEG (422), a fake HEIC (415).
"""
import io
import json

from PIL import Image, ImageChops, ImageDraw, ImageOps, ImageStat

from bench import reset, record, state, clear, bench
from session import Session, full_fields
import uuid

V = 'after'


def pattern(w=240, h=160):
    im = Image.new('RGB', (w, h), (30, 90, 140))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w // 3, h // 4], fill=(240, 200, 40))            # top-left block
    d.rectangle([w - w // 6, h - h // 3, w - 1, h - 1], fill=(200, 30, 30))   # bottom-right block
    d.rectangle([w // 2, 0, w // 2 + 8, h // 2], fill=(20, 160, 60))      # an off-centre bar
    return im


def make(fmt, orientation=1, gps=True, extra=True):
    ex = Image.Exif()
    if orientation != 1:
        ex[0x0112] = orientation
    if gps:
        g = ex.get_ifd(0x8825)
        g[1] = 'N'; g[2] = (32.0, 4.0, 30.0); g[3] = 'E'; g[4] = (34.0, 46.0, 10.0)
    ex[0x010F] = 'SyntheticCam'          # camera make
    ex[0x0131] = 'nlj-bench'             # software
    b = io.BytesIO()
    kw = {'exif': ex.tobytes()}
    if fmt == 'JPEG':
        kw['quality'] = 95
    if fmt == 'PNG' and extra:
        from PIL.PngImagePlugin import PngInfo
        pi = PngInfo()
        pi.add_text('Comment', 'synthetic location text 32.0755,34.7818')
        kw['pnginfo'] = pi
    if fmt == 'WEBP':
        kw['quality'] = 95
        kw['xmp'] = b'<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF><rdf:Description exif:GPSLatitude="32,4.5N"/></rdf:RDF></x:xmpmeta>'
    pattern().save(b, fmt, **kw)
    raw = b.getvalue()
    if fmt == 'JPEG' and extra:
        xmp = b'http://ns.adobe.com/xap/1.0/\x00<x:xmpmeta><rdf:Description exif:GPSLatitude="32,4.5N"/></x:xmpmeta>'
        seg = b'\xff\xe1' + (len(xmp) + 2).to_bytes(2, 'big') + xmp
        com = b'synthetic comment 32.0755,34.7818'
        seg += b'\xff\xfe' + (len(com) + 2).to_bytes(2, 'big') + com
        raw = raw[:2] + seg + raw[2:]
    return raw


def metadata_left(bin_, fmt):
    left = []
    im = Image.open(io.BytesIO(bin_))
    ex = im.getexif()
    if len(ex):
        left.append('exif:%s' % sorted(ex.keys()))
    if ex.get_ifd(0x8825):
        left.append('gps')
    for marker in (b'GPSLatitude', b'xmpmeta', b'SyntheticCam', b'nlj-bench', b'32.0755', b'Photoshop 3.0'):
        if marker in bin_:
            left.append(marker.decode())
    if fmt == 'PNG':
        for ch in (b'eXIf', b'tEXt', b'zTXt', b'iTXt'):
            if ch in bin_:
                left.append('png:' + ch.decode())
    if fmt == 'WEBP':
        for ch in (b'EXIF', b'XMP '):
            if ch in bin_[12:]:
                left.append('webp:' + ch.decode().strip())
    return left


def same_pixels(a, b):
    if a.size != b.size:
        return False, 'size %s vs %s' % (a.size, b.size)
    ra = a.convert('RGB').resize((32, 32), Image.BILINEAR)
    rb = b.convert('RGB').resize((32, 32), Image.BILINEAR)
    diff = ImageStat.Stat(ImageChops.difference(ra, rb)).mean
    return max(diff) < 6.0, 'mean diff per channel %s' % [round(x, 2) for x in diff]


def main():
    clear('L09', V)
    reset(V)
    s = Session(V).login('dana')
    st, d = s.post('/owner/draft', {'create_key': str(uuid.uuid4()), 'fields': full_fields(), 'step': 'photos'})
    did = d['id']
    libs = bench(V, '/libs', None, 'GET')[1]
    results = []
    for fmt in ('JPEG', 'PNG', 'WEBP'):
        for o in range(1, 9):
            if fmt != 'JPEG' and o not in (1, 6, 3):
                continue
            raw = make(fmt, o)
            ref_img = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
            name = 'o%d.%s' % (o, fmt.lower().replace('jpeg', 'jpg'))
            code, j = s.upload('/owner/photo', name, raw, {'draft': did}, 'image/' + fmt.lower())
            row = {'format': fmt, 'orientation': o, 'upload': code}
            if code == 200:
                sc, body, hd = s.fetch(j['full'])
                stored = Image.open(io.BytesIO(body))
                same, how = same_pixels(ref_img, stored)
                row.update({'stored_type': hd.get('Content-Type'), 'stored_size': stored.size, 'displayed_as_original': same, 'pixels': how, 'metadata_left': metadata_left(body, stored.format)})
                row['ok'] = same and not row['metadata_left']
            else:
                row.update({'answer': j.get('code'), 'message': j.get('message')})
                row['ok'] = j.get('code') == 'orient'   # refused, never stored sideways
            results.append(row)
    for fmt in ('JPEG', 'PNG', 'WEBP'):
        rows = [r for r in results if r['format'] == fmt]
        ok = all(r['ok'] for r in rows)
        record({'id': 'L09', 'variant': V, 'label': 'real-wp', 'title': '%s: location/camera metadata removed and the displayed orientation kept (%s)' % (fmt, ', '.join('o%d' % r['orientation'] for r in rows)),
                'status': 'pass' if ok else 'fail', 'evidence': {'rows': rows, 'php_image_libraries': libs}})

    # bad files: one explicit answer each, nothing stored
    big = b'\xff\xd8\xff\xe0' + b'\x00' * (15 * 1024 * 1024 + 10)
    cases = [
        ('over 15 MB', 'big.jpg', big, 'image/jpeg', 413),
        ('a text file renamed .jpg', 'fake.jpg', b'<?php echo "synthetic"; ?>\n' * 20, 'image/jpeg', 415),
        ('an executable renamed .jpg', 'tool.jpg', b'MZ\x90\x00' + b'\x00' * 400, 'image/jpeg', 415),
        ('a corrupt JPEG (right header, broken data)', 'broken.jpg', b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00' + b'\x13\x37' * 500, 'image/jpeg', 422),
        ('a HEIC file (this bench cannot decode HEIC)', 'photo.heic', b'\x00\x00\x00\x18ftypheic\x00\x00\x00\x00mif1heic' + b'\x00' * 200, 'image/heic', 415),
    ]
    rows = []
    before = len(json.loads(json.dumps(s.get('/owner/draft/%d' % did)[1].get('recovered', []))))
    for title, name, data, ct, want in cases:
        code, j = s.upload('/owner/photo', name, data, {'draft': did}, ct)
        rows.append({'case': title, 'status': code, 'code': j.get('code'), 'message': j.get('message'), 'expected': want, 'ok': code == want})
    after = len(s.get('/owner/draft/%d' % did)[1].get('recovered', []))
    ok = all(r['ok'] for r in rows) and after == before
    record({'id': 'L09', 'variant': V, 'label': 'real-wp', 'title': 'bad files: too big 413, renamed text/executable 415, corrupt 422, HEIC 415; nothing stored', 'status': 'pass' if ok else 'fail',
            'evidence': {'rows': rows, 'stored_before': before, 'stored_after': after}})


if __name__ == '__main__':
    main()
