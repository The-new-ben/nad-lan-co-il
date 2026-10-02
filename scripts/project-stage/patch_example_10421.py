# -*- coding: utf-8 -*-
"""v104.21 (2.10.2026, the V2 loop turn 5, V4 step 2; HAD-380): design styles inside the Kikar example apartment.
  1. the 360 of the living room passes the manifest's styles (examples.json pano.styles: warm, light, stone, rendered by the
     fleet's studio kit) to the fleet's viewer (../tour.js), which already shows a style switch and reports the style in nl:view
     (the basket keeps it); "כמו במסירה" is the room as rendered; names and notes in five languages, no developer wording;
  2. the 360 tile says how many design styles it has;
  3. openExample({ start: 'pano' }) opens the 360 at once (the basket's "להיכנס לדירה ולבחור סגנון");
  4. the size line names no source (the owner, 1.10: no source names on the page).
  python patch_example_10421.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "project-stage", "world", "example.js")
s = open(P, encoding="utf-8").read()
if "v104.21" in s:
    raise SystemExit("already patched")


def sub(old, new, name, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"[{name}] anchor found {c} times")
    s = s.replace(old, new)


SZ = {
    "he": ("    size: (rooms, sqm, src) => `בגודל שפורסם בעסקאות במגדלים: ${rooms} חדרים, ${sqm} מ״ר (${src})`,",
           "    size: (rooms, sqm) => `בגודל של דירות שנמכרו במגדלים: ${rooms} חדרים, ${sqm} מ״ר`, // v104.21: no source name",
           """    styleNames: { bare: 'כמו במסירה', warm: 'עץ חם', light: 'בהיר', stone: 'אבן' }, stylesLabel: 'עיצוב הדירה', stylesSub: 'רעיון להמחשה',
    styleNote: 'רעיון עיצוב להמחשה.', stylesN: (n) => `${n} סגנונות עיצוב`, // v104.21"""),
    "en": ("    size: (rooms, sqm, src) => `The size of the published deals in the towers: ${rooms} rooms, ${sqm} m² (${src})`,",
           "    size: (rooms, sqm) => `The size of apartments sold in the towers: ${rooms} rooms, ${sqm} m²`, // v104.21: no source name",
           """    styleNames: { bare: 'As delivered', warm: 'Warm wood', light: 'Light', stone: 'Stone' }, stylesLabel: 'Design the apartment', stylesSub: 'An idea, for illustration',
    styleNote: 'A design idea, for illustration.', stylesN: (n) => `${n} design styles`, // v104.21"""),
    "fr": ("    size: (rooms, sqm, src) => `À la taille des ventes publiées dans les tours : ${rooms} pièces, ${sqm} m² (${src})`,",
           "    size: (rooms, sqm) => `À la taille des appartements vendus dans les tours : ${rooms} pièces, ${sqm} m²`, // v104.21: no source name",
           """    styleNames: { bare: 'Tel que livré', warm: 'Bois chaleureux', light: 'Clair', stone: 'Pierre' }, stylesLabel: 'Aménager l’appartement', stylesSub: 'Une idée, à titre d’illustration',
    styleNote: 'Une idée d’aménagement, à titre d’illustration.', stylesN: (n) => `${n} styles d’aménagement`, // v104.21"""),
    "ru": ("    size: (rooms, sqm, src) => `Площадь как в опубликованных сделках в башнях: ${rooms} комнаты, ${sqm} м² (${src})`,",
           "    size: (rooms, sqm) => `Площадь как у проданных квартир в башнях: ${rooms} комнаты, ${sqm} м²`, // v104.21: no source name",
           """    styleNames: { bare: 'Как при сдаче', warm: 'Тёплое дерево', light: 'Светлый', stone: 'Камень' }, stylesLabel: 'Дизайн квартиры', stylesSub: 'Идея, для иллюстрации',
    styleNote: 'Идея дизайна, для иллюстрации.', stylesN: (n) => `${n} стиля дизайна`, // v104.21"""),
    "ar": ("    size: (rooms, sqm, src) => `بمساحة الصفقات المنشورة في الأبراج: ${rooms} غرف، ${sqm} م² (${src})`,",
           "    size: (rooms, sqm) => `بمساحة الشقق المبيعة في الأبراج: ${rooms} غرف، ${sqm} م²`, // v104.21: no source name",
           """    styleNames: { bare: 'كما عند التسليم', warm: 'خشب دافئ', light: 'فاتح', stone: 'حجر' }, stylesLabel: 'تصميم الشقة', stylesSub: 'فكرة للتوضيح',
    styleNote: 'فكرة تصميم للتوضيح.', stylesN: (n) => `${n} أنماط تصميم`, // v104.21"""),
}
for L, (a, b, c) in SZ.items():
    sub(a, b + "\n" + c, "size " + L)
sub("""        <div class="nlex__size">${esc(T.size(size.rooms || 4, size.sqm || 140, T.sizeSrc))}</div>""",
    """        <div class="nlex__size">${esc(T.size(size.rooms || 4, size.sqm || 140))}</div>""", "size use")
# the 360 tile names its styles
sub("""<span class="nlex__tl">${esc(T.tile.pano)}</span></button>`,""",
    """<span class="nlex__tl">${esc(T.tile.pano)}${Array.isArray(ex.pano.styles) && ex.pano.styles.length ? ` · ${esc(T.stylesN(ex.pano.styles.length))}` : ''}</span></button>`,""",
    "pano tile")
# open the 360 at once when asked
sub("""    build();
  }).catch(""", """    build();
    if (o.start === 'pano' && ex.pano) open360(null); // v104.21: the basket's "להיכנס לדירה ולבחור סגנון"
  }).catch(""", "start pano")
# the viewer gets the styles
sub("""        scenes: [{ id: p.base, dir: 'w', spot: 'living', title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),
          note: T.panoNote(ex.floor, p.hour), chip: T.chip }],
        chip: T.chip, caption: T.label + '.', hint: T.drag, close: T.close, lang, dir: rtl ? 'rtl' : 'ltr', errorText: T.error, opener: btn,""",
    """        scenes: [{ id: p.base, dir: 'w', spot: 'living', title: T.panoTitle(o.tower, ex.floor), src: U(p.base + '.webp'), small: U(p.base + '-2k.webp'),
          note: T.panoNote(ex.floor, p.hour), chip: T.chip,
          // v104.21: the design styles (studio kit), the same room and the same look in another picture; "bare" is the room as rendered
          styles: Array.isArray(p.styles) && p.styles.length ? [{ id: 'bare', label: T.styleNames.bare }].concat(p.styles.map((st) => ({
            id: st.id, label: T.styleNames[st.id] || st.id, thumb: U(st.base + '-thumb.webp'), src: U(st.base + '.webp'), small: U(st.base + '-2k.webp') }))) : undefined }],
        stylesLabel: T.stylesLabel, stylesSub: T.stylesSub, styleNote: T.styleNote,
        chip: T.chip, caption: T.label + '.', hint: T.drag, close: T.close, lang, dir: rtl ? 'rtl' : 'ltr', errorText: T.error, opener: btn || o.opener,""",
    "viewer styles")
open(P, "w", encoding="utf-8", newline="\n").write(s)
print("example.js patched (v104.21)")
