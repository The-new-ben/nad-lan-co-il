# -*- coding: utf-8 -*-
"""Release 1.72.469 (HAD-543, Ben 19.10.2026: "a switch: empty room, room with furniture; at the highest level"):
- every Ashira apartment room (floor 25 and floor 10, four directions, the two balconies) gets the room AS DELIVERED (empty,
  the page's own words) as its picture and the furnished look as the "warm" style, all in ChatGPT quality (gpt-image);
- the viewer may open in a style a page names (tour.js, additive: no page names one but Ashira, so the others open as before);
- Ashira opens furnished, and the switch reads "ללא ריהוט" / "עם ריהוט · עץ חם" (the labels are shared by every project).
Hunks on the LIVE texts, each anchor once."""
RELS = ["inc/project-stage.php", "assets/project-stage/tour.js", "assets/project-stage/bridge.js"]
VSRC = "\t\t\t\t\t'view_src'   => 'הנוף בחלון הוא הדמיה לפי הכיוון והגובה של הקומה, להמחשה בלבד.',\n"
PHP = [
    (VSRC, VSRC + "\t\t\t\t\t'style'      => 'warm', // 1.72.469: opens furnished; one tap shows the room as delivered\n"),
    ("'<button type=\"button\" class=\"nlds-btn nlds-btn--primary nlat__go\" data-nlps-tour=\"'",
     "'<button type=\"button\" class=\"nlds-btn nlds-btn--primary nlat__go\"' . ( ! empty( $tc['style'] ) ? ' data-nlps-tour-style=\"' . esc_attr( (string) $tc['style'] ) . '\"' : '' ) . ' data-nlps-tour=\"'"),
    ("array( 'id' => 'bare', 'label' => 'כמו במסירה', 'sub' => 'ריק, אריחים בהירים',",
     "array( 'id' => 'bare', 'label' => 'ללא ריהוט', 'sub' => 'כמו במסירה, אריחים בהירים',"),
    ("array( 'warm', 'עץ חם', 'פרקט אלון, מטבח אגוז, פשתן' )", "array( 'warm', 'עם ריהוט · עץ חם', 'פרקט אלון, מטבח אגוז, פשתן' )"),
]
TOUR = [("  let style = 'bare';\n", "  let style = o.style && o.style !== 'bare' ? String(o.style) : 'bare'; // 1.72.469: a page may open in a named style\n")]
BRIDGE = [
    ("m.openTour(Object.assign(o, { opener: opener || null }))",
     "m.openTour(Object.assign(o, { opener: opener || null, style: (tourBtn && tourBtn.getAttribute('data-nlps-tour-style')) || undefined }))"),
    ("      start,\n", "      start,\n      style: (tourBtn && tourBtn.getAttribute('data-nlps-tour-style')) || undefined,\n"),
]
SUBS = {"inc/project-stage.php": PHP, "assets/project-stage/tour.js": TOUR, "assets/project-stage/bridge.js": BRIDGE}


def apply(rel, txt):
    for a, b in SUBS.get(rel, []):
        if txt.count(a) != 1:
            raise SystemExit(f"ashira_469: anchor x{txt.count(a)} in the live {rel}: {a[:60]}")
        txt = txt.replace(a, b, 1)
    return txt
