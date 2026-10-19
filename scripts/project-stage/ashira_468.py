# -*- coding: utf-8 -*-
"""Release 1.72.468 (HAD-543, Ben 19.10.2026: ChatGPT quality only): Ashira's floor-25 living-room 360s (four directions and
the three styles) are replaced by photoreal panoramas upgraded from the 1.72.464 geometry (gpt-image, same room and window).
Hunks on the LIVE inc/project-stage.php: (1) the north and south labels were wrong (the port and the Yarkon lie SOUTH of
Sde Dov); (2) the view line now says what the window shows: an illustration by direction and height, not the city layer."""
RELS = ["inc/project-stage.php"]
SUBS = [
    ("array( 'n', 'צפון', 'לכיוון נמל תל אביב והירקון', '' ),", "array( 'n', 'צפון', 'לכיוון תל ברוך והרצליה', '' ),"),
    ("array( 's', 'דרום', 'לכיוון מרכז העיר', '' ),", "array( 's', 'דרום', 'לכיוון פארק הירקון, הנמל ומרכז העיר', '' ),"),
    ("'facing'     => 'מול הים, הירקון, רמת אביב ומרכז העיר',", "'facing'     => 'מול הים, תל ברוך, רמת אביב ופארק הירקון',"),
    ("'view_src'   => 'הנוף בחלון בנוי מהבניינים הקיימים לפי שכבת המבנים של העירייה ומקו החוף.',", "'view_src'   => 'הנוף בחלון הוא הדמיה לפי הכיוון והגובה של הקומה, להמחשה בלבד.',"),
]


import ashira_464 as P464


def apply(rel, txt):
    if rel != "inc/project-stage.php":
        return txt
    # 1.72.464's first run was rolled back without restoring this file (its PHP_RELS was empty), so the tour block sits twice
    n = txt.count(P464.TOUR)
    if n == 2:
        txt = txt.replace(P464.TOUR, "", 1)
    elif n != 1:
        raise SystemExit(f"ashira_468: the 1.72.464 tour block x{n} in the live {rel}")
    new = P464.TOUR
    for a, b in SUBS:  # inside Ashira's own block only (DUO and others share some of these words)
        if new.count(a) != 1:
            raise SystemExit(f"ashira_468: anchor x{new.count(a)} in the 1.72.464 tour block: {a[:50]}")
        new = new.replace(a, b, 1)
    if txt.count(P464.TOUR) != 1:
        raise SystemExit("ashira_468: the tour block is not there once after the dedupe")
    return txt.replace(P464.TOUR, new, 1)
