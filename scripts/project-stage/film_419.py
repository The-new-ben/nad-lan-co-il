# -*- coding: utf-8 -*-
"""Release 1.72.419 (design v104.42, the Kikar loop turn 28): captions on V1, the first Kikar film, too. V1's own caption files
(docs/design-lab/films/kikar/kikar-he.vtt 0d2ad228..., kikar-en.vtt 21a3acfd...; the 2.10 build) were proven against the LIVE V1
bytes by the video producer (claude-codex.md, 3.10 ~23:55: lag 0 ms in five windows on all four live files). Uploaded once as
media 8174 / 8175 (docs/qa/film-v2r1/media-vtt-v1.json, byte-checked) and served by the 1.72.418 text/vtt route under two more
keys (v1-he, v1-en). One <track kind="captions"> per V1 video in its narration's language, off by default; the cue style now
covers the whole film section. Applied to the LIVE inc/project-stage.php text (what 1.72.418 wrote), each anchor exactly once."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
V = json.load(io.open(os.path.join(REPO, "docs", "qa", "film-v2r1", "media-vtt-v1.json"), encoding="utf-8"))
IDS = {}
for lang in ("he", "en"):
    e = V[f"kikar-hamedina-film-v1-{lang}.vtt"]
    if e.get("byte_check") != "OK":
        raise SystemExit("film_419: the V1 " + lang + " caption file was not byte-checked OK")
    IDS[lang] = int(e["id"])
RELS = ["inc/project-stage.php"]
FILES = {}

HUNKS = (
    # V1's video builder: the captions track after the source
    ("\t\t\t\t. '<source src=\"' . esc_url( $u . $k . '-' . $f . '-preview.mp4' ) . '\" type=\"video/mp4\"></video>';\n",
     "\t\t\t\t. '<source src=\"' . esc_url( $u . $k . '-' . $f . '-preview.mp4' ) . '\" type=\"video/mp4\">'\n"
     "\t\t\t\t. '<track kind=\"captions\" srclang=\"' . $k . '\" label=\"' . ( 'he' === $k ? 'עברית' : 'English' ) . '\" src=\"' . esc_url( rest_url( 'nadlan/v1/film-cc/v1-' . $k ) ) . '\"></video>'; // v104.42\n"),
    # the route serves V1's files under two more keys
    ("'/film-cc/(?P<lang>he|en)'", "'/film-cc/(?P<lang>he|en|v1-he|v1-en)'"),
    ("array( 'he' => 8172, 'en' => 8173 )", "array( 'he' => 8172, 'en' => 8173, 'v1-he' => %d, 'v1-en' => %d )" % (IDS["he"], IDS["en"])),
    # one cue style for the whole film section
    (".nlws-film__v2 video::cue{", ".nlws-film video::cue{"),
)


def apply(rel, txt):
    if "film-cc/v1-" in txt:
        raise SystemExit("film_419: already applied")
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("film_419: an anchor is there " + str(txt.count(a)) + " times: " + a.strip()[:80])
        txt = txt.replace(a, b)
    return txt
