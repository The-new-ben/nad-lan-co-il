# -*- coding: utf-8 -*-
"""HAD-403 step 2 (design v104.35, Maya's 09:00 UTC scope): no size range from illustrative units.
The price card "מחיר ממוצע למ״ר בפרויקט, דירות A-B מ״ר" took A-B from `project_3d_units`, the stage's illustrative examples.
The old guard read only the notes for "הדגמה"/"demo"; SIX 8 ("דוגמה — קומה 11", 232 / 339 m2) and Dimri Yama ("יחידת
אב-טיפוס", "להמחשה", 92-250 m2) said so in the title, the availability or the source note. Now ANY of the unit's own text fields
(not its image or tour URLs) marks it illustrative, and an illustrative unit never feeds a public number. No replacement size.
Measured on all 43 projects with units (docs/qa/had-403/units-*.json): only SIX 8 and Dimri (+4 language pages) change.
Applied to the LIVE text by the release runner (each anchor exactly once) and by --apply to the repo copy."""
import io, os, sys

OLD_NOTE = ("\t\t\t$u_note  = (string) ( $u['note'] ?? '' ) . ' ' . (string) ( $u['source_note'] ?? '' ) . ' ' . "
            "(string) ( $u['market_note'] ?? '' );\n")
NEW_NOTE = ("\t\t\t// HAD-403 (v104.35, 3.10.2026): a unit is illustrative when ANY of its own words says so (title, label, availability,\n"
            "\t\t\t// notes; not its image or tour URLs). SIX 8 and Dimri said \"דוגמה\", \"להמחשה\" or \"אב-טיפוס\" outside the notes.\n"
            "\t\t\t$u_note = '';\n"
            "\t\t\tforeach ( $u as $u_k => $u_v ) { if ( is_string( $u_v ) && ! preg_match( '/url$/', (string) $u_k ) ) { $u_note .= ' ' . $u_v; } }\n")
OLD_FLAG = "\t\t\t\t'demo'  => false !== mb_strpos( $u_note, 'הדגמה' ) || false !== stripos( $u_note, 'demo' ),\n"
NEW_FLAG = ("\t\t\t\t'demo'  => (bool) preg_match( '/הדגמה|דוגמה|דוגמא|המחשה|אב[- ]טיפוס|\bdemo|example|illustrat|prototype|sample/iu', "
            "$u_note ),\n")


def apply(txt):
    for a in (OLD_NOTE, OLD_FLAG):
        if txt.count(a) != 1:
            raise SystemExit("px_range: an anchor is there " + str(txt.count(a)) + " times: " + a.strip()[:60])
    if "HAD-403 (v104.35" in txt:
        raise SystemExit("px_range: already applied")
    return txt.replace(OLD_NOTE, NEW_NOTE).replace(OLD_FLAG, NEW_FLAG)


if __name__ == "__main__" and "--apply" in sys.argv:
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "inc", "project-experience.php")
    t = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in t
    t = apply(t.replace("\r\n", "\n"))
    io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("applied to the repo copy")
