# -*- coding: utf-8 -*-
"""Writes deploy429.py from the released and verified deploy428.py: release 1.72.429 = ProjectFilm v80 (film_429.py), the DUO,
Rainbow and Dimri Yama films live in five languages. Inherited checks that the change removes are updated (the 409 lesson):
- t346: rainbow-en must not carry the film -> it now must (the English film);
- t331: rainbow he needed the v79 files (rainbow-tel-aviv-film-wide/tall.mp4) -> the v1 files; duo forbade the film -> requires it.
New checks: the film button, the film file and the label in the page's language on all 15 pages (3 projects x he/en/fr/ru/ar);
the Hebrew label never on a language page; the v79 file never again on Rainbow."""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import film_429  # noqa: E402
s = io.open(os.path.join(HERE, "deploy428.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_428 as PX  # noqa: E402 (1.72.428: world boot A/B switch, HAD-421)\n", "    import film_429 as PX  # noqa: E402 (1.72.429: ProjectFilm v80, three project films in five languages)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.428 world-boot switch hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.429 project-films hunk)")')
rep('print("RELEASE 1.72.428 LIVE: HAD-421 step 9 (A/B), ?nlwboot=early mounts the world once the page is parsed; default unchanged")',
    'print("RELEASE 1.72.429 LIVE: ProjectFilm v80, the DUO, Rainbow and Dimri Yama films in five languages")')
# the 409 lesson: inherited checks the change removes
rep("['nlfilm', 'class=\"nlbsq\"', 'nadlan-basket-cfg', 'class=\"nlpd\"']),", "['class=\"nlbsq\"', 'nadlan-basket-cfg', 'class=\"nlpd\"']),")
rep("'rainbow-tel-aviv-film-wide.mp4', 'rainbow-tel-aviv-film-tall.mp4', 'סרטון הפרויקט',",
    "'rainbow-tel-aviv-film-v1-he-16x9-1.mp4', 'rainbow-tel-aviv-film-v1-he-9x16-1.mp4', 'סרטון הפרויקט',")
rep("    ('/projects/duo-tel-aviv/?t331=1', ['id=\"nlsch\"'], ['id=\"nlfilm\"', 'VideoObject']),",
    "    ('/projects/duo-tel-aviv/?t331=1', ['id=\"nlsch\"', 'id=\"nlfilm\"', 'VideoObject'], []),")
M = json.load(io.open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "film-v1-projects", "media.json"), encoding="utf-8"))
LABEL = {"he": "סרטון הפרויקט", "en": "Project film", "fr": "Film du projet", "ru": "Фильм о проекте", "ar": "فيلم المشروع"}
rows = []
for slug in ("duo-tel-aviv", "rainbow-tel-aviv", "dimri-yama-sde-dov"):
    for lang in ("he", "en", "fr", "ru", "ar"):
        fl = "he" if lang == "he" else "en"
        f16 = M[f"{slug}-film-v1-{fl}-16x9.mp4"]["url"].rsplit("/", 1)[-1]
        f9 = M[f"{slug}-film-v1-{fl}-9x16.mp4"]["url"].rsplit("/", 1)[-1]
        path = f"/projects/{slug}/" if lang == "he" else f"/projects/{slug}-{lang}/"
        never = ["rainbow-tel-aviv-film-wide.mp4"] + ([] if lang == "he" else ["סרטון הפרויקט"])
        rows.append((path, ['data-nlps-ev="hero-film"', 'id="nlfilm"', f16, f9, LABEL[lang], '"@type":"VideoObject"'], [], never))
OLD = """# 1.72.428 (HAD-421 step 9, A/B): the world-boot switch is on the Kikar pages and the default boot line is unchanged
"""
NEW = ("# 1.72.429 (ProjectFilm v80): the film on all 15 pages of DUO, Rainbow and Dimri Yama, in the page's language\n"
       "CHECKS += " + repr(rows) + "\n" + OLD)
rep(OLD, NEW)
for x, y in (("1.72.428", "1.72.429"), (".bak428", ".bak429"), ("PS428", "PS429"), ("ps428", "ps429"), ("deploy428", "deploy429"),
             ("result-428", "result-429"), ("speed-428", "speed-429"), ("posts-before-428", "posts-before-429"), ("make_deploy428", "make_deploy429")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-427.json")', '_prev = os.path.join(QA, "deploy-result-428.json")'),
             ('"FATAL: release 1.72.427 is still in flight', '"FATAL: release 1.72.428 is still in flight'),
             ('WANT_LIVE = "1.72.427"  # the checks name ?ver=1.72.429: this runner is for the release right after 1.72.427',
              'WANT_LIVE = "1.72.428"  # the checks name ?ver=1.72.429: this runner is for the release right after 1.72.428'),
             ("        for n in range(427, 329, -1):", "        for n in range(428, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy429.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy429.py with", len(rows), "film checks")
