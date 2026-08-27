# מפת מקורות ייחוס שאינם Lovable raw

הנתיבים להלן קיימים בריפו בבסיס הארכוב ומשמשים להשוואה בלבד. הם לא הועתקו ל־`raw/` ולא מיוחסים ל־Lovable בלי ראיה.

| תחום | נתיב בריפו | שימוש נכון |
|---|---|---|
| שפת sketch קאנונית | `docs/design/2026-06-30-sketch-art-prompt-spec.md` | צבע, קו, חומריות והיררכיית imagery |
| Image factory | `handoff/cowork/2026-07-02-image-factory-mega-prompt.md` | תהליך יצירה, authenticity ladder ו־prompt governance |
| Premium assets | `assets/premium/` | SVG symbols, micro UI, fallbacks ו־concept assets; לבדוק wiring וזכויות |
| Premium manifest | `assets/premium/MANIFEST.md` | מקור ושימוש מיועד של assets |
| Concept manifest | `assets/premium/concept/MANIFEST.md` | הפרדה בין concept לחומר רשמי |
| Rainbow media | `docs/rainbow-media/` | hero/location/amenities היסטוריים; לא Lovable output |
| Rainbow project assets | `assets/projects/rainbow-tel-aviv/` | GLB, poster, payload, unit map ותוכניות אילוסטרטיביות |
| Rainbow source notes | `assets/projects/rainbow-tel-aviv/source-notes.md` | אזהרה שהתוכניות/מלאי/מחירים אינם חומר מכר רשמי |
| Rainbow docs | `docs/2026-06-11-rainbow-3d-product-direction.md` | כיוון מוצר ומסלול רוכש |
| Rainbow selector | `docs/2026-06-14-rainbow-apartment-cell-selector-spec.md` | חוזה בחירה והקלקה היסטורי |
| Local previews | `docs/previews/` | השוואת UI בלבד; לא evidence של אתר חי |
| Historic live QA | `docs/qa/screenshots/` | ראיות לדורות קוד אחרים; לא להעתיק wholesale |
| Sde Dov experience | `experience/sde-dov/` | reference לסביבת פרויקט וסיור, לא Lovable raw |
| 1,000-step WP plan | `handoff/codex/2026-06-24-lovable-implementation-plan/` | Codex implementation plan; אינו פלט Lovable |
| Mixed prompt glossary | `docs/prompts-lovable-and-cowork-glossary.md` | input/support בלבד |

## Assets שדורשים זהירות

- `assets/design/sketch-art-2026-06-30/tower-A-unconfirmed-project.jpg`
- `assets/design/sketch-art-2026-06-30/tower-B-unconfirmed-project.jpg`

שני הקבצים מסומנים unconfirmed ואין להציגם כפרויקט מזוהה.

## כלל השוואה

כשיש סתירה בין Lovable לבין קוד/DOM חי, הפרויקט החי והמקור הרשמי גוברים. כשאין חומר רשמי, משתמשים ב־concept מסומן או במצב ריק; לא משדרגים mock לעובדה.
