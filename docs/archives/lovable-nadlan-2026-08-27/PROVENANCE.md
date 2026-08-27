# Provenance — מקור, זמן ומעמד

## מקורות ראשיים

| מקור | מזהה/גרסה | נראות | שיטת לכידה | מעמד |
|---|---|---|---|---|
| Lovable Design Lab | project `627f6877-57f3-4821-9e77-2b2011c56292`; ref `5191562ae49cff8079a4a8bfb0ed1249e789532b` | private, unpublished | Lovable official connector + browser screenshots | raw Lovable export |
| NadLan Strategy Hub | project `a7493b94-2e46-4d38-9c6a-80dcf0905f45`; ref `5219d3eac8707c88fe070759dd7d5fa260d119c0` | editor private; published public | Lovable official connector + browser audit; ללא screenshot ארכיוני חדש | raw Lovable export |
| ChatGPT `NADLAN` | conversation `6a379273-5ee4-83eb-99a8-fd97141c612c` | private session | explicit attachment recovery + thread metadata | private-session export |
| Nadlan repository | `The-new-ben/nad-lan-co-il`; base `41123fad891147d9d25210b59d402a3bf6ae98fb` | private repository | isolated Git worktree | repository evidence |

Capture date: `2026-08-27`, timezone `Asia/Jerusalem`. Exact timestamps לכל קובץ נמצאים ב־`MANIFEST.json` כאשר המקור סיפק אותם.

מטא־דאטה גולמי של פעולת הייצוא, לרבות רשימת 13 הנתיבים ורשימת 80 ה־binaries שלא יוצאו, נשמר ללא עריכה תחת `raw/export-metadata/`.

## כתובות מקור

### Design Lab

- Editor: `https://lovable.dev/projects/627f6877-57f3-4821-9e77-2b2011c56292`
- Preview base: `https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app`
- אין public production URL; הפרויקט לא פורסם.

### Strategy Hub

- Editor: `https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45`
- Public: `https://nadlan-vision-quest.lovable.app/`
- Showroom: `https://nadlan-vision-quest.lovable.app/showroom/rainbow-tlv`

## תוויות provenance

| תווית | פירוש |
|---|---|
| `raw_lovable_export` | קובץ שהתקבל מה־connector ונשמר ללא עריכה |
| `browser_observation` | צילום או metadata שנלכדו מהעמוד הנראה בדפדפן |
| `captured_lovable_output` | פלט Lovable שנשמר בעבר בריפו |
| `recovered_user_attachment` | פלט ששוחזר מקובץ שהמשתמש צירף לשיחה |
| `chatgpt_private_session_export` | חומר משיחת ChatGPT פרטית; אינו raw Lovable source |
| `repo_variant` | עיבוד/סינתזה שנוצרו בריפו על בסיס פלטים קודמים |
| `repo_reference_only` | נכס או מסמך שמשמש הקשר בלבד ואינו פלט Lovable |
| `derived_archive_analysis` | מסמך הניתוח שנכתב במיוחד לארכיון זה |

## מיפוי Reports

| Artifact | מצב אמיתי | מקור |
|---|---|---|
| Report 0 | captured Lovable output | `prompts-and-reports/lovable-history/2026-06-21-report-0-strategy-intake.md` |
| Report 1 | captured Lovable output | `prompts-and-reports/lovable-history/2026-06-21-report-1-public-trust-technical-seo.md` |
| Report 2 | recovered user attachment; clean CSV הוא authority לתקופה ההיסטורית | `prompts-and-reports/lovable-history/2026-06-21-report-2-keyword-master-universe.md` |
| Reports 4–7 | משולבים בתוך bundle ששוחזר מהשיחה; לא קיימים בריפו בשמות נפרדים | `prompts-and-reports/chatgpt-handoff/NadLan-COMPLETE-BUNDLE.md` |
| A0–A9 | Project Knowledge/prompt sequence מתועד ב־bundle וב־handoff; אין export נפרד ומלא לכל A-number | limitation מפורש |

## שמות שהתבקשו אך אינם קיימים בריפו

החיפוש ב־working tree וב־`git log --all` לא מצא את הקבצים המדויקים הבאים:

- `strategy/lovable-reports/04-site-architecture-cannibalization.md`
- `strategy/lovable-reports/05-ux-ui-design-system.md`
- `strategy/lovable-reports/06-3d-project-showroom.md`
- `strategy/lovable-reports/07-revenue-model-gtm.md`
- `strategy/gap-analysis-and-build-plan.md`
- `strategy/war-room-master-report.html`
- `strategy/NadLan-COMPLETE-BUNDLE.md`

לא הומצאו קבצים חלופיים בשמות האלה. ה־bundle האמיתי ששוחזר נשמר בשמו, והווריאנטים הקרובים מסומנים `repo_variant` תחת `prompts-and-reports/repo-variants/`.

## קורפוס Lovable ההיסטורי בריפו

`prompts-and-reports/lovable-history/` הוא העתק של `strategy/lovable/` בבסיס Git. ה־README המקורי מזהה את Strategy Hub הישן. יש להבדיל בין:

- Reports 0–1: captured output.
- Report 2: recovered attachment.
- workbook, HTML ו־previews: derived repo artifacts.
- fallback/stalled/next-prompt: operational history שאינה authority.

הקבצים `nadlan-lovable-strategy-dossier.html` ו־`nadlan-report-2-keyword-master-rtl.html` הם כפילות byte-for-byte; שניהם נשמרו כדי לא לאבד path provenance.

## raw preservation

קבצים תחת `raw/` וקבצי session export לא נערכו כדי “לתקן” עובדות. ניתוח, ציונים ואזהרות נמצאים רק במסמכי הארכיון העליונים. `MANIFEST.json` משווה hashes ומסמן את שיטת הלכידה. קובץ טקסט יחיד של Strategy Hub הוחרג בשל מדיניות סודות שמרנית; 80 binaries שלא הוחזרו על ידי ה־connector מתועדים ב־[EXPORT-LIMITATIONS.md](EXPORT-LIMITATIONS.md).

## זכויות ושימוש

קיום קובץ בארכיון אינו הוכחת רישיון שימוש פומבי. assets חיצוניים, Unsplash, renders, logos, photos ו־project material מסומנים `rights_unknown` אלא אם מקור אחר בריפו מוכיח אחרת.
