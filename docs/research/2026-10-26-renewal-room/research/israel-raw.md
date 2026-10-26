# Israeli urban-renewal tools: raw evidence (26.10.2026)

Scope: real Israeli software, apps and portals that organizers (חברות מארגנות / ליווי דיירים), residents' committees (נציגות דיירים), developers and their lawyers use to track owner consent/signatures in פינוי בינוי and תמ"א 38. Read-only research. No form was submitted, no account created, no trial started, no demo booked, no one contacted.

All pages read on 26.10.2026.

## Evidence classes used below

- **[S]** seen on the public page (URL given in the product section), 26.10.2026.
- **[B]** seen in the public JavaScript bundle that renders the marketing site (the site is a client-side app, so the text is not in the raw HTML). Where the bundle file name showed the string belongs to the marketing page (for example `Landing.tsx`), it is the visible landing-page text. Strings that look like in-app screens are labelled "in-app string" and are weaker evidence.
- **[L]** the vendor's own `llms.txt` / `llms-full.txt` file (machine-readable product description published by the vendor).
- **[SERP]** Google result snippet (title or description) captured through DataForSEO, Israel/Hebrew, 26.10.2026. Used only where the page itself blocked automated reading.
- **[3P]** a third-party page (news or competitor comparison) describing the product.
- **n/s** = not stated on anything read. **inferred** = my inference, labelled.

Quotes are short Hebrew phrases copied from the source (each under 15 words).

---

## 1. OneStep

- **URLs read:** https://onestep.co.il/software/hitchadshut-ironit · https://onestep.co.il/for/meargenim · https://onestep.co.il/pricing · https://onestep.co.il/compare · https://onestep.co.il/tenant-portal · https://onestep.co.il/capabilities · https://onestep.co.il/privacy (rendered without policy text) · SERP snippet for https://b.me.app/onestep
- **Date read:** 26.10.2026
- **Who it is for:** urban-renewal developers, construction companies, organizers, law firms, local authorities [S hitchadshut-ironit]. Dedicated pages for organizers (/for/meargenim), developers (/for/yazamim), lawyers (/for/orchei-din) [S link list].
- **What it really offers (as the pages show):**
  - "מפת החתמה לפי בניין וקומה" and "סטטוס חתימה לכל דירה" [S meargenim].
  - Consent "מחושבים לפי בעלות"; threshold set per track; "תחזית להגעה לסף" [S hitchadshut-ironit, meargenim].
  - Owner types: heirs, owners abroad, companies, guardians, protected tenants [S hitchadshut-ironit]; "בעלות משותפת, אחוזי בעלות ובעלים ראשי לכל דירה" [S capabilities].
  - Project set-up from Tabu extract: "סריקת נסחי טאבו ב-AI" [S capabilities].
  - Signature rounds per stage, up to 1,000 signers per round with audit trail (vendor claim) [S compare]; "חותם דיגיטלי עם hash לאימות שלמות המסמך" [S capabilities].
  - "יומן ביקורת מלא" [S capabilities]; every action logged with time and actor [S hitchadshut-ironit].
  - "דוחות פרויקט ב-PDF ובאקסל בעברית מימין לשמאל" [S capabilities]; consent reports in the format the authority requires, no API to the authority [S hitchadshut-ironit].
  - "SMS ממותג", "וואטסאפ רשמי דרך Meta", email, from one communication centre [S capabilities]; signature link "בהודעת טקסט או בוואטסאפ", automatic reminders to non-signers [S meargenim].
  - Tenant portal: "אזור אישי לכל דייר", OTP + ID number + phone login, "מה חדש" feed, residents upload files to project folder, sign on phone [S tenant-portal].
  - Voting "סגירה אוטומטית במועד שנקבע"; "פרוטוקול חתום דיגיטלית"; "דפי נוכחות דיגיטליים לאסיפות דיירים" [S capabilities].
  - CRM for leads, tasks "עם אחראי ותאריך יעד", AI agent STEP, AI voice dialer, GIS complex check, developer tender module [S capabilities, pricing].
  - "הרשאות ברמת פרויקט וברמת לשונית"; "בידוד מלא בין חברות"; two-step login [S capabilities].
  - Claims "מעל 50 פרויקטים פעילים" (vendor claim, no customers named) [S hitchadshut-ironit].
- **Price (published):** TRY ₪85/month (1 project, no WhatsApp/SMS, 50 signatures, 3 GB); START ₪183/month on the plan card, ₪218 in the comparison table (5 projects, 100 WhatsApp + 150 SMS, 100 signatures, 10 GB); PRO ₪490 card / ₪590 table (20 projects, 200 WhatsApp + 200 SMS, 350 signatures, 60 GB); custom plan on request. All before VAT, 14-day trial. AI dialer is a paid add-on [S pricing]. Price for residents: n/s (inferred: residents do not pay; nothing on the page charges them).
- **Languages shown:** tenant portal Hebrew, English, Arabic, Russian with automatic direction [S tenant-portal]; organizer page says "בעברית, ערבית ורוסית" [S meargenim]; content translation to Russian, English, French, Arabic, Amharic [S capabilities].
- **Mobile app:** tenant portal is mobile web ("מכל דפדפן ומכל מכשיר"), no App Store / Google Play link shown [S]. Capabilities page says "אפליקציה להתקנה בנייד" with no store link (inferred: installable web app).

| # | Capability | Score | Note (evidence) |
|---|---|---|---|
| 1 | Consent/signature status per apartment | Yes | "סטטוס חתימה לכל דירה", list of non-signers [S meargenim] |
| 2 | Multi-building complex | Yes | Signing map by building and floor [S meargenim] |
| 3 | Portfolio across projects | Yes | Many complexes, one control screen, GIS portfolio map [S] |
| 4 | Owners per apartment, co-owners, heirs | Yes | Co-ownership shares, main owner; heirs, abroad, guardians listed [S] |
| 5 | Document checklist / file storage | Partial | Stores files (3/10/60 GB); per-apartment checklist n/s [S pricing, tenant-portal] |
| 6 | Stage ladder, legal clocks | Partial | Four signing stages, milestones, task due dates; legal clocks n/s [S] |
| 7 | Majority calculator by law | Yes | Per-track threshold, by ownership share, forecast to threshold [S] |
| 8 | Per-apartment change log | Yes | "יומן ביקורת מלא"; history kept on each tenant card [S] |
| 9 | Role-based privacy | Partial | Personal area per tenant, tiered roles; neighbour isolation not explicitly stated [S] |
| 10 | Committee report printable/PDF | Yes | Consent report in authority format; PDF/Excel RTL [S] |
| 11 | Updates feed + WhatsApp/SMS/email | Yes | "מה חדש" feed; Meta WhatsApp, branded SMS, email; quotas per plan [S] |
| 12 | Languages | Yes | He/En/Ar/Ru portal; translation to more [S] |
| 13 | Phone use | Partial | Mobile-first web portal; "installable" app, no store link [S] |
| 14 | Price residents / organizer | Yes (organizer) | ₪85–₪590/month before VAT; residents n/s [S pricing] |
| 15 | E-signature built in | Yes | Signature rounds with hash; monthly signature quotas [S] |
| 16 | Assemblies/voting/minutes | Yes | Voting, digitally signed protocol, digital attendance pages [S] |
| 17 | Staff tasks / CRM | Yes | Lead CRM, tasks with owner/date, AI dialer [S] |
| 18 | Privacy / hosting / Israeli law | Partial | Encryption, 2FA, company isolation; hosting and Privacy Law n/s [S] |

---

## 2. BinuGo (בינוגו)

- **URLs read:** https://binugo.com/ (client-rendered; text read from bundle `/assets/index-BkyCZD3j.js`) · https://binugo.com/llms.txt · https://binugo.com/llms-full.txt (updated 2026-08-23 per the file) · https://binugo.com/sitemap.xml · https://binugo.com/pricing, /terms, /professionals, /guides/choose-system (all client-rendered; read from bundle)
- **Date read:** 26.10.2026
- **Who it is for:** apartment owners and residents' committees (free), plus professionals: residents' lawyers, developers, project managers, appraisers, supervisors, architects (paid) [L].
- **What it really offers:**
  - Residents get everything on WhatsApp, no app: updates, timeline, documents, votes, and a personal AI agent that answers from project data [L, B].
  - "מעקב חתימות לפי תת-חלקה (דירה), לא לפי אנשים" [B]; "הדירה נספרת רק כשכולם חתמו" [B]; stance per owner: "תומך, מתלבט או מתנגד" [B].
  - "אחוז הסכמה משוקלל גם לפי חלקה ברכוש המשותף" [B].
  - Digital signature of the committee authorization letter and other PDFs: personal WhatsApp link, one-time code, audit trail (time, IP, device, SHA-256 of the document), signature appendix attached to the PDF; based on the Electronic Signature Law 2001 [L]. When the majority is reached it produces a signed PDF [B].
  - Gantt timeline with stages and sub-stages, templates per project type, "אנחנו כאן" marker [L, B].
  - Broadcast updates to the whole building "עם מעקב מי קרא" [B]; residents' questions gathered, answers go back to WhatsApp [L]; votes with live results [L].
  - "בקשת מסמכים אישיים מדיירים (נסח טאבו, צילום ת"ז)" returned over WhatsApp [L].
  - Import residents from Excel or build the whole project from a Tabu PDF with AI, "כולל כמה בעלים לדירה" [B].
  - Company entity, team, multi-project dashboard, shared templates; MCP/API for outside AI agents [L].
  - Online assemblies: connects to Google Calendar, a bot joins Zoom/Meet/Teams, transcribes Hebrew, drafts a summary for WhatsApp broadcast [B].
  - "הודעות SMS — בקרוב" (SMS not yet available) [B].
- **Price (published):** Free: one project, up to 20 residents, 3 team members, 50 WhatsApp messages/month. Pro ₪200/month (₪180 on annual): 10 paid project slots, unlimited residents per paid project, 6 team, 500 WhatsApp/month. Business ₪400/month (₪360 annual): 20 slots, 12 team, opening message in the office's name. Partner: by contract for developers and large organizations [L, B]. "חינם לדיירים ולנציגות" [L].
- **Languages shown:** "Hebrew UI" [L]. No other interface language found (n/s).
- **Mobile app:** none by design; WhatsApp plus secure browser links [L].
- **Privacy:** terms say the system works under "חוק הגנת הפרטיות, התשמ"א-1981, לרבות תיקון מס' 13" [B]; sub-processors named: Supabase, OpenAI, Resend, Recall.ai [B]; "הרשאות לפי תפקיד, נתונים בישראל/EU, ואפשרות לייצא הכל" (from its own buying guide) [B]; documents delivered "בקישורים חתומים מוגבלי-זמן" [B].

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Yes | Per sub-parcel, all owners must sign, stance per owner [L, B] |
| 2 | Multi-building complex | n/s | Guide mentions multi-building projects; product view not described [B] |
| 3 | Portfolio | Yes | Multi-project dashboard, company entity, 10/20 project slots [L] |
| 4 | Owners, co-owners, heirs | Partial | Several owners per apartment from Tabu; heirs n/s [B] |
| 5 | Documents / storage | Yes | Requests Tabu and ID copy per resident; project document store [L] |
| 6 | Stage ladder, legal clocks | Partial | Gantt with sub-stages and templates; legal clocks n/s [L] |
| 7 | Majority calculator | Yes | By apartments, weighted by common-property share, vs threshold [B] |
| 8 | Change log | Partial | Full audit trail for signatures; general per-apartment log n/s [L] |
| 9 | Role-based privacy | Partial | Role permissions, signed time-limited links; neighbour view n/s [B] |
| 10 | Committee report / PDF | Partial | Signed PDF when majority reached; committee status report n/s [B] |
| 11 | Updates feed + push | Yes | WhatsApp broadcast with read tracking, AI bot; SMS "בקרוב" [B] |
| 12 | Languages | No | Hebrew only stated [L] |
| 13 | Phone use | Yes | WhatsApp-first, browser links, no app needed [L] |
| 14 | Price | Yes | Free for committee/residents; ₪180–₪400/month professionals [L] |
| 15 | E-signature | Yes | OTP, audit trail, signature appendix, Electronic Signature Law [L] |
| 16 | Assemblies/voting/minutes | Yes | Votes with live results; meeting recording, Hebrew transcript, summary [B] |
| 17 | Tasks / CRM | Partial | Team workspace, Q&A inbox, API/MCP; task manager or CRM n/s [L] |
| 18 | Privacy / hosting / law | Yes | Privacy Law + Amendment 13 cited; Israel/EU data; sub-processors named [B] |

---

## 3. Redirectx

- **URLs read:** https://redirectx.co.il/he · https://redirectx.co.il/he/pricing · https://redirectx.co.il/he/features · https://redirectx.co.il/he/security · https://redirectx.co.il/he/portal · SERP snippets (he/en home, portal, features)
- **Date read:** 26.10.2026
- **Who it is for:** nine roles: organizer, developer, committee, resident, lawyer, appraiser, supervisor, professional, municipality, each with its own home screen [S /he].
- **What it really offers:**
  - Personal portal per resident: signatures, votes, project status; "שקיפות מלאה על היחידה שלך" [S portal].
  - Signature funnel "נשלח → נצפה → בתהליך → נחתם"; each signature hashed; page calls it "קבילה משפטית" [S /he, features].
  - "סטטוס ההסכמה ואחוזי הבעלות המשותפת" [S features]; a calculator at /he/calculator [S /he].
  - Seven stages from locating a building to occupancy, permit tracking [S /he].
  - Document library "לפי תפקיד ושלב", AES-256, virus scan on upload [S /he, features].
  - Developer tender comparison on six criteria with AI scoring and committee vote [S /he]; "תיבת החלטות שקופה" for votes [S features].
  - Reports exported to PDF and Excel ("דוחות מצרפיים") [S features].
  - "הודעות SMS / וואטסאפ / מייל" with ready templates [S features]; AI assistant ("Atlas") answers status questions on WhatsApp [S /he].
  - "כל פעולה במערכת מתועדת ובלתי ניתנת לשינוי", kept 12 months [S features, security].
  - Lead pipeline and GIS map for finding buildings; per-unit project billing and professional invoices [S /he].
  - Expert/company directory at /he/experts (seen in SERP: developer profile pages with public project counts) [SERP].
- **Price:** "הדיירים והנציגות לעולם לא משלמים" [S pricing]. Plans with limits but no prices on the page: סולו basic (up to 5 projects, 10 GB, 100 SMS / 50 WhatsApp), צוות start (15 projects, 30 GB, 500/500), חברה pro (30 projects, 60 GB, 1,000/1,000), ארגון enterprise (unlimited, API, white-label). Digital signatures unlimited on all plans; residents and team unlimited [S pricing]. 14-day trial without card [S /he]. Organizer price: not published.
- **Languages shown:** Hebrew, English, Russian (HE / EN / RU selector in portal) [S portal].
- **Mobile app:** portal "מהמחשב ומהנייד"; app screens shown but no store links [S].
- **Privacy:** "שרתי המערכת בישראל, בהתאם לחוק הגנת הפרטיות" [S security]; AES-256, encrypted transport and backups, 2FA by mobile number; Amendment 13 compliance documentation managed in Compass by Lancelot Technologies [S security]. ISO/SOC n/s.

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Partial | Signature funnel per signer; per-apartment rollup not explicit [S] |
| 2 | Multi-building complex | n/s | Not described [S features] |
| 3 | Portfolio | Yes | Plans by project count up to unlimited; "project portfolio" plan [S pricing] |
| 4 | Owners, co-owners, heirs | Partial | Co-ownership percentages; heirs n/s [S features] |
| 5 | Documents / storage | Partial | Encrypted library by role and stage, 10–60 GB; per-apartment checklist n/s [S] |
| 6 | Stage ladder, legal clocks | Partial | Seven stages, permit tracking; legal clocks n/s [S] |
| 7 | Majority calculator | Partial | Consent and ownership %, calculator page; legal thresholds n/s [S] |
| 8 | Change log | Yes | Immutable action log, 12 months retention [S security] |
| 9 | Role-based privacy | Partial | "כל אחד רואה רק את מה שמותר לו"; own-unit wording [S] |
| 10 | Committee report / PDF | Partial | Aggregate reports to PDF/Excel; committee format n/s [S] |
| 11 | Updates feed + push | Yes | Committee messages in portal; SMS/WhatsApp/email templates; WhatsApp AI [S] |
| 12 | Languages | Partial | He/En/Ru; Arabic n/s [S portal] |
| 13 | Phone use | Partial | Mobile web portal; no store link [S] |
| 14 | Price | Partial | Free for residents/committee; professional prices not published [S] |
| 15 | E-signature | Yes | Unlimited signatures, hash per signature [S] |
| 16 | Assemblies/voting/minutes | Partial | Transparent decision box with counted votes; minutes n/s [S] |
| 17 | Tasks / CRM | Partial | Lead pipeline, GIS, billing; staff tasks n/s [S] |
| 18 | Privacy / hosting / law | Yes | Israel servers per Privacy Law, AES-256, 2FA, Amendment 13 docs [S security] |

---

## 4. BuildLy

- **URLs read:** https://buildly.co.il/ · https://buildly.co.il/pricing · https://buildly.co.il/guides/eich-bochrim-maarechet (comparison vs OneStep and BinuGo, "עודכן ב-25 באוקטובר 2026")
- **Date read:** 26.10.2026
- **Who it is for:** "מערכת ליזמים של התחדשות עירונית" [S guide]; organizers and developers running signature drives (inferred from features).
- **What it really offers:**
  - Owners table per apartment with status "חתמה" / "ממתינים" [S home].
  - Each building tracked separately ("בניין א׳") [S home]; its guide warns "החוק דורש 60% בכל בניין, לא רק שני שלישים מהמקבץ" [S guide] (legal claim by the vendor, not verified here).
  - Majority "לפי דירות, מול שני שלישים; דירה נספרת רק כשכל בעליה חתמו" [S guide]; map shows apartments still needed for two thirds [S home].
  - "כמה בעלים לדירה" (example: 41 owners across 26 apartments) [S home]; Tabu extract read automatically "עם בדיקה שאף דירה לא חסרה" [S guide].
  - Owner signs on phone via personal link: "קישור שננעל על הטלפון ובדיקת תעודת זהות"; "בתוך החוזה, במקום שסומן" [S guide].
  - Contracts organized by building, apartment and stage as private files [S home].
  - Six stages with targets for permit, construction start, handover; tasks with owner and date synced to Google Calendar [S home].
  - "יומן פעילות" [S home].
  - Investor tracking: investors get a personal page showing only their own investment [S home].
  - Feasibility check exported as PDF with logo [S home].
  - Reminders: "מייל אחרי 3 ימים ושוב אחרי 7, ממסלול צוות" [S guide].
- **Price (published):** פרויקט אחד ₪190/month (40 signatures), צוות ₪790/month (5 projects, 100 signatures), חברה ₪1,190/month (20 projects, 300 signatures), ארגון custom. Before VAT; annual 10% off; extra signature ₪3 or 50 for ₪150; 14 days free. "דיירים ומשקיעים לא משלמים לעולם" [S pricing].
- **Languages shown:** Hebrew only ("בעברית") [S home].
- **Mobile app:** phone browser, no store links [S home].
- **Privacy:** encrypted traffic; data stored in a data centre in Frankfurt [S home]. Israeli Privacy Law n/s.

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Yes | Owners table per apartment with signed/waiting [S] |
| 2 | Multi-building complex | Yes | Each building separately; per-building rule raised [S] |
| 3 | Portfolio | Yes | 1/5/20 projects; company sees only its projects [S] |
| 4 | Owners, co-owners, heirs | Partial | Several owners per apartment from Tabu; heirs n/s [S] |
| 5 | Documents / storage | Partial | Contracts stored by building/apartment/stage; ID copy n/s [S] |
| 6 | Stage ladder, legal clocks | Partial | Six stages with target dates; legal clocks n/s [S] |
| 7 | Majority calculator | Yes | By apartments vs two thirds, all owners must sign [S guide] |
| 8 | Change log | Partial | "יומן פעילות"; scope n/s [S] |
| 9 | Role-based privacy | Partial | Manager sets project visibility; owner/investor personal links [S] |
| 10 | Committee report / PDF | Partial | Feasibility PDF with logo; consent report n/s [S] |
| 11 | Updates feed + push | Partial | Email reminders 3/7 days; link by email or WhatsApp; no feed [S] |
| 12 | Languages | No | Hebrew only [S] |
| 13 | Phone use | Partial | Phone browser; no app [S] |
| 14 | Price | Yes | ₪190 / ₪790 / ₪1,190 per month; residents never pay [S] |
| 15 | E-signature | Yes | Sign inside the contract; phone-locked link + ID check [S] |
| 16 | Assemblies/voting/minutes | No | Not mentioned [S] |
| 17 | Tasks / CRM | Partial | Tasks with Google Calendar; investor tracking; CRM n/s [S] |
| 18 | Privacy / hosting / law | Partial | Encrypted, Frankfurt data centre; Israeli law n/s [S] |

---

## 5. Asset Rise

- **URLs read:** https://asset-rise.byclick.co.il/ (client-rendered; text read from bundle `/assets/index-OqDo5FUe.js`, marketing file `Landing.tsx`, login file `Login.tsx`) · https://asset-rise.byclick.co.il/sitemap.xml · SERP snippets for / and /login
- **Date read:** 26.10.2026
- **Who it is for:** owners, residents' committee, developers, lawyers, architects, suppliers [B Landing]; address "רחוב יסמין 14, חולון" [B]. Company legal name n/s.
- **What it really offers:**
  - Free feasibility check by address: score 0–100, recommended track, estimated timeline, five next steps [B]; data "מבוסס על נתוני GovMap · MAVAT · data.gov.il" [B].
  - "כל מסמך חתום דיגיטלית"; "חתימת PADES, ולידציה ברגע, היסטוריה לא ניתנת לשינוי" [B Landing].
  - "כל הצבעה מוקלטת ומאומתת"; "רוב מחייב לפי 51% מהדיירים, עם תיעוד מי הצביע ומתי" [B Landing].
  - "כל החלטה מקושרת למסמך" (who decided, when, on what basis) [B Landing].
  - Conversations split by stage: setup, tenders, signatures, construction, handover [B Landing].
  - "הרשאות לפי תפקיד": "דייר רואה את שיחות הנציגות שלו; ספק רואה רק את שלו" [B Landing]; "המייל שלך לא נחשף לדיירים אחרים" [B Login].
  - AI assistant: "תשובה לכל שאלה. בעברית, בערבית, ברוסית, באנגלית"; contract clause explanation, contract draft diff [B Landing].
  - "גשר משפחתי": elderly owner delegates read/participate rights to a relative, without signing rights; "הדייר חותם בעצמו עם זיהוי חוקי"; relative's actions logged [B Landing].
  - Surveys with "פילוח לפי קומה"; documents by stage (plans, agreements, protocols); "ייצוא PDF / Word", reports "מוכנים להגשה לוועדה המקומית" [B Landing].
  - Developer tenders and supplier management [B].
  - Install prompt "התקינו את Asset Rise לקבלת התראות" and notifications "גם כשהאפליקציה סגורה" [B, in-app string] (inferred: installable web app with push).
- **Price:** feasibility check free [B]. Platform price not published (no ₪ figure anywhere in the bundle).
- **Languages shown:** Hebrew UI; AI answers in He/Ar/Ru/En [B Landing]. Interface languages beyond Hebrew n/s.
- **Mobile app:** no store links; installable web app with push (inferred from in-app strings).
- **Privacy:** "תקן הצפנה ברמת בנקאות", Google sign-in, role permissions [B Login]; personal names/IDs removed before AI analysis [B]; 2FA strings in app [B, in-app string]. Hosting and Israeli Privacy Law n/s.

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Partial | Signature collection and history; per-apartment rollup n/s [B] |
| 2 | Multi-building complex | Partial | Feasibility computed for whole complex; management view n/s [B] |
| 3 | Portfolio | Partial | One account for all your projects; organizer portfolio n/s [B] |
| 4 | Owners, co-owners, heirs | Partial | Family delegate for elderly owners; co-owners/heirs n/s [B] |
| 5 | Documents / storage | Partial | Documents by stage with version history; per-apartment checklist n/s [B] |
| 6 | Stage ladder, legal clocks | Partial | Four documented stages, committee to keys; clocks n/s [B] |
| 7 | Majority calculator | Partial | Votes bind at 51%; consent majority only in feasibility report [B] |
| 8 | Change log | Partial | Immutable signature history; decision log; family-action log [B] |
| 9 | Role-based privacy | Yes | Resident sees own threads; supplier only own; email hidden [B] |
| 10 | Committee report / PDF | Yes | PDF/Word export, ready for local committee [B] |
| 11 | Updates feed + push | Partial | Stage-tagged messages, push when app closed; SMS/WhatsApp n/s [B] |
| 12 | Languages | Partial | AI answers He/Ar/Ru/En; UI languages n/s [B] |
| 13 | Phone use | Partial | Installable web app with push (inferred); no store links [B] |
| 14 | Price | No | Platform price not published; feasibility free [B] |
| 15 | E-signature | Yes | PAdES signatures with instant validation [B] |
| 16 | Assemblies/voting/minutes | Yes | Verified votes, surveys, committee election, protocols [B] |
| 17 | Tasks / CRM | Partial | Legal tasks, tenders, suppliers; CRM n/s [B] |
| 18 | Privacy / hosting / law | Partial | Bank-level encryption claim, PII stripping; law/hosting n/s [B] |

---

## 6. Pinui.Info (brand "Yazam")

- **URLs read:** https://pinui.info/ (client-rendered; meta description + bundle `/assets/index-u4Td86-C.js` and chunks `YPricing`, `YFaq`, `Legal`, `YTenantPortal`, `YDashboard`, `YProjectEditor`) · SERP snippet
- **Date read:** 26.10.2026
- **Who it is for:** developers ("יזם / פרויקטור"), project managers, residents' committees; residents get a portal [B].
- **What it really offers:**
  - Meta description: "מעקב חתימות, פורטל דיירים ושלבי רישוי" [S meta].
  - Dashboard: who signed, who is in process, who opposes; "מפת חתימות לפי קומה וקריטיות" [B].
  - "המערכת מחשבת אוטומטית את אחוז החתימות לפי בניין" [B]; buildings, floors, apartments, CSV import [B].
  - Project setup: address, city and "אחוז הסכמה נדרש"; "הגדר שלבי רישוי ומסמכים נדרשים" [B].
  - "העלה ועקוב אחרי מסמכים לכל דייר ודירה" [B]; Tabu PDF import of owners (in-app string) [B].
  - Tenant portal: own signature status ("סטטוס חתימה שלך"), overall signing progress, project stages, project lawyer contact, messages to the team (question/complaint/suggestion), contact history [B YTenantPortal]; "המידע בפורטל זה אישי וסודי" [B].
  - WhatsApp OTP login; WhatsApp button next to every tenant; "WhatsApp ואימייל מובנים" for updates and reminders [B].
  - Tasks and reminders, per-tenant contact history (calls, meetings), "יומן פעילות" [B].
  - Reports: "דוח חתימות", "דוח מקיף הכולל דיירים, שלבים ועדכונים" [B, in-app strings].
  - Its FAQ tells residents "נדרשת הסכמה של לפחות 80% מבעלי הדירות בכל בניין" [B YFaq] (inferred: legally questionable for פינוי בינוי, where the general rule is two thirds; flagged as a quality gap on their side, not verified here).
- **Price (published in bundle):** בסיסי ₪149/month (1 project, 40 tenants, 1 user), מקצועי ₪349 (5 projects, 200 tenants, WhatsApp updates, tasks), חברה ₪699 (20 projects, 1,000 tenants, consolidated dashboard), ארגוני ₪999 (unlimited). Annual = base x12; "תשלום חודשי עולה 20% יותר"; 14-day free trial; payment via Grow [B YPricing]. Residents and committee free: "העלות היא על היזם בלבד" [B].
- **Languages shown:** Hebrew only (no other language strings found) [B].
- **Mobile app:** "הפורטל עובד ישירות מהדפדפן בנייד — בלי הורדות" [B]; registers a service worker (`registerSW.js`) (inferred: installable web app).
- **Privacy:** privacy policy "בהתאם לחוק הגנת הפרטיות" (updated March 2026) [B Legal]; "הרשאות לפי תפקיד, גיבויים יומיים ואימות דו-שלבי" [B]. Hosting n/s.

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Yes | Signed / in process / opposed; floor map [B] |
| 2 | Multi-building complex | Yes | Buildings, floors; % per building [B] |
| 3 | Portfolio | Yes | Up to 20 / unlimited projects; consolidated dashboard [B] |
| 4 | Owners, co-owners, heirs | Partial | Several owners per apartment; heirs only as task example [B] |
| 5 | Documents / storage | Yes | Required documents per stage; upload per tenant and apartment [B] |
| 6 | Stage ladder, legal clocks | Partial | Licensing stages; legal clocks n/s [B] |
| 7 | Majority calculator | Partial | Configurable required %; FAQ states 80% per building [B] |
| 8 | Change log | Partial | Activity log, contact history per tenant [B] |
| 9 | Role-based privacy | Yes | Tenant sees own status + aggregate; roles developer/committee [B] |
| 10 | Committee report / PDF | Partial | Signature and full reports; format n/s [B] |
| 11 | Updates feed + push | Partial | Portal updates; WhatsApp and email; SMS n/s [B] |
| 12 | Languages | No | Hebrew only [B] |
| 13 | Phone use | Partial | Mobile web portal, no download [B] |
| 14 | Price | Yes | ₪149–₪999/month; residents and committee free [B] |
| 15 | E-signature | n/s | Tracks a signed consent form; built-in e-signing not found [B] |
| 16 | Assemblies/voting/minutes | Partial | Attach protocol PDF; a vote step for appraiser [B] |
| 17 | Tasks / CRM | Yes | Tasks, reminders, call/meeting history [B] |
| 18 | Privacy / hosting / law | Partial | Policy cites Privacy Law; 2FA, daily backups; hosting n/s [B] |

---

## 7. GetStatus (גט סטטוס)

- **URLs read:** https://search.getstatus.online/he · https://search.getstatus.online/he/organizers (a directory) · https://search.getstatus.online/he/magazine/project-organizers (vendor article, updated March 2026) · https://search.getstatus.online/he/pricing (no prices rendered) · project app at app.getstatus.online (not opened; behind login)
- **Date read:** 26.10.2026
- **Who it is for:** apartment owners and committees (status, transparency, offers) and professionals (developers, law firms, organizers) [S home].
- **What it really offers:**
  - Owners check project status; "פיד התחדשות"; "חותם השקיפות" for companies; "מכרזים שקופים"; rankings of developers and law firms [S home].
  - For organizers (vendor article): density/feasibility check, "המרת נסח טאבו בשנייה" to a sheet of names, parcels and IDs, "מיפוי מדויק של מי רלוונטי להחתמה", record the committee election, "שלח עדכונים שוטפים לדיירים", and "המערכת מתריעה על אי-עמידה בלו"ז שנקבע" (Organizers Law timelines) [S magazine].
- **Price:** not shown (pricing page did not render prices) [S].
- **Languages shown:** Hebrew only seen.
- **Mobile app:** owners' "app" is a web app; no store links [S home].

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Partial | Mapping who must sign; status per apartment n/s [S magazine] |
| 2 | Multi-building complex | n/s | — |
| 3 | Portfolio | n/s | Organizer "קידום מתחמים" wording only [SERP] |
| 4 | Owners, co-owners, heirs | Partial | Tabu to sheet with names, parcels, IDs [S magazine] |
| 5 | Documents / storage | n/s | — |
| 6 | Stage ladder, legal clocks | Partial | Alerts on missed Organizers-Law timeline (article claim) [S magazine] |
| 7 | Majority calculator | n/s | — |
| 8 | Change log | n/s | — |
| 9 | Role-based privacy | n/s | Owners log in to "הדירות שלי" [S] |
| 10 | Committee report / PDF | Partial | Feasibility reports only [S magazine] |
| 11 | Updates feed + push | Partial | Renewal feed; updates to residents; channel n/s [S] |
| 12 | Languages | No | Hebrew only seen |
| 13 | Phone use | Partial | Web app, no store link [S] |
| 14 | Price | n/s | Not rendered |
| 15 | E-signature | n/s | — |
| 16 | Assemblies/voting/minutes | Partial | Transparent tenders, committee election record [S] |
| 17 | Tasks / CRM | Partial | Marketplace of offers; resident inquiries [S] |
| 18 | Privacy / hosting / law | n/s | Legal page not read |

---

## 8. RolyHome (רוליהום)

- **URLs read:** https://rolyhome.com/he/ · https://rolyhome.com/he/product-overview/ · https://rolyhome.com/he/signature-solutions/ (says the content is password protected: **not public**)
- **Date read:** 26.10.2026
- **Who it is for:** "פתרון תוכנה ... המותאם לחברות נדל”ן", focus on urban renewal [S home].
- **What it really offers:** five modules you pay for separately: "החתמות, מכירות, משימות, דוחות ותקשורת" [S overview]; "לנהל חתימות דיירים" [S overview]; tasks with owners; custom reports incl. profitability; dedicated company phone number and email system; "אחסון הקבצים הבלתי מוגבל"; personal pages for residents and buyers with milestones and contracts; "ניהול הרשאות חזק" [S overview].
- **Price:** not published; pay per module chosen [S overview].
- **Languages shown:** Hebrew and English [S overview].
- **Mobile app:** n/s. A YouTube video "תוכנת רוליהום" appeared in SERP (not watched).

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Partial | "לנהל חתימות דיירים"; detail page password-protected [S] |
| 2 | Multi-building complex | n/s | — |
| 3 | Portfolio | n/s | — |
| 4 | Owners, co-owners, heirs | n/s | — |
| 5 | Documents / storage | Partial | Unlimited file storage; per-apartment checklist n/s [S] |
| 6 | Stage ladder, legal clocks | Partial | Milestones on resident pages [S] |
| 7 | Majority calculator | n/s | — |
| 8 | Change log | n/s | "עקוב אחר הפעולות" on tasks only [S] |
| 9 | Role-based privacy | Partial | Strong permissions; personal pages [S] |
| 10 | Committee report / PDF | Partial | Custom reports; PDF n/s [S] |
| 11 | Updates feed + push | Partial | Company phone line and email; WhatsApp/SMS n/s [S] |
| 12 | Languages | Partial | Hebrew, English [S] |
| 13 | Phone use | n/s | — |
| 14 | Price | n/s | Pay per module, no figures [S] |
| 15 | E-signature | n/s | Signing module described only behind password |
| 16 | Assemblies/voting/minutes | n/s | — |
| 17 | Tasks / CRM | Yes | Tasks with owners, sales module [S] |
| 18 | Privacy / hosting / law | n/s | Terms page linked, not read |

---

## 9. VPlans (developer ERP with urban-renewal module and resident portal)

- **URLs read:** https://www.vplans.com/he · https://www.vplans.com/he/products/urban-renewal · https://www.vplans.com/he/products/client-portal · https://www.vplans.com/he/about/pricing-plan · https://www.vplans.com/he/products/mailing-system · https://www.vplans.com/he/about/iso27001 (only a PDF link) · https://portal.vplans.com/he/ildc (resident portal of הכשרת הישוב התחדשות עירונית: **behind login / not public**; SERP snippet only) · Google Play listing of "שיכון ובינוי נדל"ן" (com.vplans.ShikunBinui) via SERP snippet
- **Date read:** 26.10.2026
- **Who it is for:** developer and contractor companies; residents/buyers and "בעלי הקרקע" through the portal [S].
- **What it really offers:**
  - Urban-renewal module: "ניהול סטאטוס חתימות ומידע על בעלי קרקע" [S urban-renewal]; demo rows show owner, "חלקה 12 · דירה 4", status נחתם / ממתין לחתימה / חסר מידע, and "ממתין למסמך זהות" [S urban-renewal].
  - Portfolio dashboard; project cards show "אחוז חתימות" and "יחידות לפינוי" (demo data) [S home].
  - Resident portal: news and updates, project progress (permit, construction start, Form 4), personal and general documents, account status, service tickets, tenant-change process "כולל חתימה דיגיטלית וצירוף מסמכים"; "כניסה עם מספר טלפון בלבד" via SMS code; "עובד באנדרואיד וב-iOS" in the browser [S client-portal]. The ILDC portal snippet offers "התקנת אפליקציית הדיירים" to the home screen [SERP].
  - Mailing to email, WhatsApp, SMS with segmentation by project, role or status [S mailing-system].
  - Documents, Gantt, meeting summaries, CRM sales, QA, budget, HR [S home].
  - Claims "מעל 6000 פרויקטים פעילים" [S home].
- **Price (published):** basic package ₪500/month per project (annual) or ₪700/month per project (monthly); unlimited users and storage; all modules; AI billed by usage [S pricing-plan]. Residents: n/s (inferred: paid by the developer).
- **Languages shown:** site in Hebrew, English, Arabic, Spanish, French [S links]. Portal languages n/s.
- **Mobile app:** VPlans on App Store (id1494338133) and Google Play (com.vplans) [S links] (inferred: staff app); developer-branded resident apps exist on Google Play, for example שיכון ובינוי נדל"ן: updates, site photos, milestone notifications [SERP].
- **Privacy:** ISO27001 page, DPA and privacy policy linked [S]; backups and security "על בסיס תשתיות ענן מתקדמות" [S home]. Hosting location and Israeli law n/s on pages read.

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Yes | Owner, parcel, apartment, signed/waiting/missing [S] |
| 2 | Multi-building complex | n/s | — |
| 3 | Portfolio | Yes | Company dashboard, signature % per project [S] |
| 4 | Owners, co-owners, heirs | Partial | Land owners per parcel; co-owners/heirs n/s [S] |
| 5 | Documents / storage | Yes | Unlimited storage; ID document pending status; portal uploads [S] |
| 6 | Stage ladder, legal clocks | Partial | Portal progress stages, Gantt; legal clocks n/s [S] |
| 7 | Majority calculator | n/s | Signature % only [S] |
| 8 | Change log | n/s | — |
| 9 | Role-based privacy | Partial | Personal portal per apartment, SMS login [S] |
| 10 | Committee report / PDF | Partial | Dashboards and reports; committee format n/s [S] |
| 11 | Updates feed + push | Yes | Portal news; email/WhatsApp/SMS mailing [S] |
| 12 | Languages | Partial | Site He/En/Ar/Es/Fr; portal n/s [S] |
| 13 | Phone use | Yes | Native VPlans apps; portal on any phone browser [S] |
| 14 | Price | Yes | ₪500–₪700 per project per month [S] |
| 15 | E-signature | Yes | Digital signing in portal (tenant changes) [S] |
| 16 | Assemblies/voting/minutes | Partial | Meeting summaries for staff; voting n/s [S] |
| 17 | Tasks / CRM | Yes | CRM sales, tasks, Gantt [S] |
| 18 | Privacy / hosting / law | Partial | ISO27001, DPA; hosting/law n/s [S] |

---

## 10. BMBY urban-renewal CRM

- **URLs read:** https://bmby.co.il/התחדשות-עירונית/ · https://bmby.co.il/פורטל-דיירים/ · SERP snippet
- **Date read:** 26.10.2026
- **Who it is for:** developers and real-estate companies, law firms and project managers, tenant-management groups, institutions and local authorities [S].
- **What it really offers:** "מערכת חתימות דיגיטליות" to sign tenants "בצורה דיגיטלית, מהירה ומאובטחת" [S]; tenant records with ownership data, contracts and "סטטוס הסכמות" [S]; real-time dashboard; "שליחת עדכונים לדיירים" by SMS, email and alerts; bulk email/SMS/WhatsApp [S]; tasks and CRM; integrations with SAP, Priority, חשבשבת [S]. Resident portal: contracts, invoices, receipts, real-time updates, inquiries with status, alerts; web based [S portal].
- **Price:** not published (contact) [S].
- **Languages shown:** n/s. **Mobile app:** n/s.
- **Privacy:** links to "bmby-safe" security page and privacy policy (not read) [S].

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Partial | Consent status in tenant record [S] |
| 2 | Multi-building complex | n/s | — |
| 3 | Portfolio | Partial | Dashboard across project stages [S] |
| 4 | Owners, co-owners, heirs | Partial | Ownership data field [S] |
| 5 | Documents / storage | Partial | Contracts in tenant record; checklist n/s [S] |
| 6 | Stage ladder, legal clocks | Partial | Initiation → signing → sales [S] |
| 7 | Majority calculator | n/s | — |
| 8 | Change log | n/s | — |
| 9 | Role-based privacy | Partial | Resident portal exists; scope n/s [S] |
| 10 | Committee report / PDF | Partial | Management reports; PDF n/s [S] |
| 11 | Updates feed + push | Yes | SMS, email, WhatsApp bulk; alerts [S] |
| 12 | Languages | n/s | — |
| 13 | Phone use | n/s | — |
| 14 | Price | n/s | — |
| 15 | E-signature | Yes | Digital signature of tenants [S] |
| 16 | Assemblies/voting/minutes | n/s | — |
| 17 | Tasks / CRM | Yes | Tasks, projects, contacts CRM [S] |
| 18 | Privacy / hosting / law | Partial | Security page linked only [S] |

---

## 11. Nadlan2U urban-renewal software

- **URL read:** https://www.nadlan2u.co.il/תוכנת נדלן להתחדשות עירונית.html
- **Date read:** 26.10.2026
- **Who it is for:** real-estate companies, developers, marketers [S].
- **What it really offers:** generic real-estate sales CRM adapted for urban renewal: "בקרת אחוזי החתמה", existing residents, buyer portal, sales contracts and payment schedules, dozens of reports, permissions, SMS/email/WhatsApp logging, browser on any device; operating since 2010 [S].
- **Price:** not published [S]. **Languages:** n/s. **App:** web only.

| # | Capability | Score | Note |
|---|---|---|---|
| 1 | Consent per apartment | Partial | Signing-rate control [S] |
| 2–8 | Multi-building … change log | n/s / Partial | Only "תיעוד מלא של כל פעולה" on tasks (Partial for #8) [S] |
| 9 | Role-based privacy | Partial | Permission system (staff) [S] |
| 10 | Committee report | Partial | Dozens of reports [S] |
| 11 | Push | Yes | SMS, email, WhatsApp [S] |
| 12 | Languages | n/s | — |
| 13 | Phone use | Partial | Browser on phone [S] |
| 14 | Price | n/s | — |
| 15 | E-signature | n/s | — |
| 16 | Assemblies/voting | n/s | — |
| 17 | Tasks / CRM | Yes | CRM and tasks [S] |
| 18 | Privacy | Partial | Encrypted communication, "הנתונים שלכם בלבד" [S] |

---

## 12. ComSign "נדל"ן Online" (e-signature for lawyers)

- **URLs read:** https://www.nadlancenter.co.il/article/7161 (published 06.02.23, updated 28.06.23; images credited to ComSign PR) [3P]; ComSign pages https://www.comsign.co.il/real-estate-tablets/ and the TAMA 38 article returned "Request unsuccessful. Incapsula incident" (**blocked for automated reading**), so their content is from Google snippets [SERP].
- **Date read:** 26.10.2026
- **Who it is for:** lawyers handling urban renewal, contractor sales and resale deals [3P].
- **What it really offers:** signing on tablets with "חתימה גרפית ביומטרית"; signed documents locked to changes; cloud or on-site archive; OTP access; claimed approval by the Bar ethics committee and recognition by the Justice Ministry; claimed use in "dozens of urban renewal projects" [3P]. Newer "נדל"ן אונליין 2.0": "חתימה מרחוק בנייד, מחשב או טאבלט", cloud system, fit to Tabu and tax rules [SERP].
- **Price:** n/s. **Languages:** n/s. **App:** n/s.
- **Matrix:** #15 E-signature **Yes** (biometric tablet and remote signing [3P, SERP]); #18 **Partial** (approvals claimed, OTP access [3P]); all other rows **n/s** (it is a signing tool, not a project-management tool).

---

## 13. EasyDo (digital forms and signatures for construction companies)

- **URL read:** https://easydo.co.il/solutions/פתרונות-דיגיטליים-לחברות-בנייה/
- **Date read:** 26.10.2026
- **Who it is for:** construction and development companies [S].
- **What it really offers:** "החתמת עשרות ומאות דיירים במקביל", "הסכמי תמ״א/פינוי-בינוי", "מעקב ובקרה בזמן אמת" of signing status, alerts; integrations monday.com, Salesforce, Priority, Make/Zapier, API; iOS and Android apps linked; ISO-27701 and approvals claimed [S].
- **Price:** price list linked, figures not on the page; free trial offered [S].
- **Matrix:** #1 **Partial** (signing status per signer [S]); #11 **Partial** (alerts, channels n/s); #13 **Yes** (iOS/Android apps linked [S]); #15 **Yes**; #17 **Partial** (integrates with CRMs); #18 **Partial** (ISO-27701 claim); others **n/s**.

---

## 14. "מגן דיירים התחדשות עירונית" app (Magen Dayarim)

- **URLs read:** https://apps.apple.com/il/app/מגן-דיירים-התחדשות-עירונית/id1637421586 · https://play.google.com/store/apps/details?id=com.app.tenantshield (raw HTML)
- **Date read:** 26.10.2026
- **Who it is for:** residents who want to run a TAMA 38 / פינוי בינוי project themselves with the company's legal backing [S].
- **What it really offers:** "יחד תוכלו לנהל הצבעות ולבחור נציגות דיירים" plus representing lawyer and developer "בהצבעה בשני סבבים"; view lawyers and construction companies and their offers; project contacts [S].
- **Price:** free; no in-app purchases listed [S]. **Store data:** iOS seller SHTIBEL COM LTD, v1.1.7 dated 29/05/2024, too few ratings; Google Play 100+ downloads, updated 29 May 2024 [S]. Recent notes are bug fixes ("סודרה בעיה בזיהוי כניסת משתמש") [S].
- **Languages:** store lists English; description in Hebrew [S].
- **Matrix:** #13 **Yes** (native iOS + Android); #14 **Yes** (free); #16 **Yes** (two-round votes to pick committee, lawyer, developer); #1–#12, #15, #17, #18 **n/s**. Appears stale (no update since May 2024).

---

## 15. "משתדרגים" app (Ramat Gan urban-renewal administration)

- **URL read:** https://play.google.com/store/apps/details?id=web2application.a271553848083.com.myapplication&hl=he (raw HTML)
- **Date read:** 26.10.2026
- **Who it is for:** Ramat Gan residents, from the municipal renewal administration (developer listed as CloudRocket - Nir Tzin) [S].
- **What it really offers:** information from the administration, "בדיקת סטטוס פרוייקטים", digital contact, "קבלת התראות חשובות"; services free [S]. 500+ downloads; updated 28 March 2024 [S].
- **Matrix:** #11 **Partial** (push notifications from the administration); #13 **Yes** (Android app); #14 **Yes** (free); everything else **n/s**. This is a municipal information app, not a consent tool. It shows that cities give residents an app channel.

---

## 16. Government Urban Renewal Authority (הרשות הממשלתית להתחדשות עירונית, gov.il)

- **URLs attempted:** https://www.gov.il/he/departments/government_authority_for_urban_renewal/govil-landing-page and https://www.gov.il/he/departments/topics/mapa-renewal returned HTTP 403 with a Cloudflare challenge ("Just a moment..."). **Not read; no challenge was solved.** Evidence below is Google snippets only [SERP].
- **Date:** 26.10.2026
- **What Google shows they offer residents:**
  - A service letting residents "לקבל חוות דעת משמאי פינוי בינוי" on an offered deal [SERP].
  - "הממונה על פניות הדיירים" to examine residents' complaints about renewal projects [SERP].
  - "מפת התחדשות עירונית בישראל": click a locality, zoom in to see פינוי בינוי projects [SERP].
  - Resident Q&A hub ("תושבים"), guides including committee-building principles and a residents' guide to contracting with a developer [SERP].
- **Matrix:** no consent tracking, no per-apartment tools, no portal seen. Free public information and complaint channel only. All 18 rows **n/s** except #14 (free) and #6 Partial (guides explain the stages).

---

## Compact matrix (all products)

Y = Yes, P = Partial, N = No, ? = not stated. Columns are the 18 capability rows above.

| Product | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OneStep | Y | Y | Y | Y | P | P | Y | Y | P | Y | Y | Y | P | Y | Y | Y | Y | P |
| BinuGo | Y | ? | Y | P | Y | P | Y | P | P | P | Y | N | Y | Y | Y | Y | P | Y |
| Redirectx | P | ? | Y | P | P | P | P | Y | P | P | Y | P | P | P | Y | P | P | Y |
| BuildLy | Y | Y | Y | P | P | P | Y | P | P | P | P | N | P | Y | Y | N | P | P |
| Asset Rise | P | P | P | P | P | P | P | P | Y | Y | P | P | P | N | Y | Y | P | P |
| Pinui.Info | Y | Y | Y | P | Y | P | P | P | Y | P | P | N | P | Y | ? | P | Y | P |
| GetStatus | P | ? | ? | P | ? | P | ? | ? | ? | P | P | N | P | ? | ? | P | P | ? |
| RolyHome | P | ? | ? | ? | P | P | ? | ? | P | P | P | P | ? | ? | ? | ? | Y | ? |
| VPlans | Y | ? | Y | P | Y | P | ? | ? | P | P | Y | P | Y | Y | Y | P | Y | P |
| BMBY | P | ? | P | P | P | P | ? | ? | P | P | Y | ? | ? | ? | Y | ? | Y | P |
| Nadlan2U | P | ? | ? | ? | ? | ? | ? | P | P | P | Y | ? | P | ? | ? | ? | Y | P |
| ComSign | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | Y | ? | ? | P |
| EasyDo | P | ? | ? | ? | ? | ? | ? | ? | ? | ? | P | ? | Y | ? | Y | ? | P | P |
| Magen Dayarim app | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | Y | Y | ? | Y | ? | ? |
| Mishtadrgim app | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | P | ? | Y | Y | ? | ? | ? | ? |
| Gov URA (gov.il) | ? | ? | ? | ? | ? | P | ? | ? | ? | ? | ? | ? | ? | Y | ? | ? | ? | ? |

Note on row 14: "Y" means a price is published (or the tool is free); it does not mean cheap.

---

## Searches run

Two engines were used on 26.10.2026.

**A. WebSearch tool (US index, thin for Hebrew)**, 4 queries:
- "מערכת לניהול פרויקט התחדשות עירונית": funder.co.il/article/121574 (Ramdor construction PM at Amidar), drushim job ads, TAU social-renewal model PDF, nadlancenter job ad. No product page.
- "אפליקציה לדיירים פינוי בינוי": apps.apple.com/us/app/-/id1637421586 (מגן דיירים), calcalist articles, MyTower (id1097081580), Build App (id1605492474), Dimri tenants app.
- "ניהול חתימות דיירים": Google Signatures article, Deloitte signatories manager, Bank Hapoalim form. Nothing relevant.
- "פורטל דיירים התחדשות עירונית": nadlancenter tag page, TAU / HUJI clinic PDFs, mr.gov.il tender documents, drushim. No product page.

**B. DataForSEO Google SERP** (`/v3/serp/google/organic/live/advanced`, location 2376 Israel, Hebrew or English as noted, desktop, depth 30). Bodies and raw outputs are in the session scratchpad (`dfs/`). Some calls failed with SE error 40101 and were retried; "partial" means only page 1 came back. Top 10 organic results per query (rank. URL | title):

- **מערכת לניהול פרויקט התחדשות עירונית** (status partial (page 1 only); AI Overview block: absent)
  - 1. https://www.green-group.co.il/רשויות-מקומיות/ | רשויות מוניציפליות וחכ"ל - greengroup
  - 2. https://minhelet-j.org.il/מידע-על-תוכניות-פינוי-בינוי/ | מידע על תוכניות פינוי בינוי
  - 3. https://ymag.ynet.co.il/pinuybinuy/ | הבניינים קורסים – אבני דרך בניהול פרוייקט התחדשות עירונית - Ymag
  - 4. https://insight-pro.io/he/product/tasks/ | תוכנה לניהול משימות ובקרת איכות בבנייה - Insight Pro
  - 5. https://apps.apple.com/il/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=he | היישום מגדילים -נדל"ן התחדשות עירונית - App Store
  - 6. https://www.youtube.com/watch?v=zlMfmACwM60 | עשה מהפכה בניהול פרויקטים של התחדשות עירונית עם תוכנת רוליהום
  - 7. https://apps.apple.com/pt/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829 | מגדילים -נדל"ן התחדשות עירונית - App Store - Apple
  - 8. https://shitrit-holdings.co.il/שטרית-יזמות-ובנייה/התחדשות-עירונית/ | התחדשות עירונית - Shitrit החזקות
  - 9. https://www.flowmyhome.com/ | FlowMyHome: איך מנהלים תקציב בנייה ושיפוץ בישראל — תמונת ...
  - 10. https://www.livy.co.il/ | ליבי | תוכנה לניהול ועד בית — תשלום באשראי
- **אפליקציה לדיירים פינוי בינוי** (status ok; AI Overview block: present, source links not captured)
  - 2. https://apps.apple.com/fi/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=fi | מגדילים -נדל"ן התחדשות עירונית - App Store - Apple
  - 3. https://www.facebook.com/groups/335318133184063/ | מינהלת דיירים לפינוי בינוי התחדשות עירונית תמ"א
  - 4. https://osltd.co.il/digital-building-management-apps-and-tools/ | ניהול ועד בית דיגיטלי: אפליקציות וכלים שמשדרגים את איכות החיים בבניין
  - 5. https://apps.apple.com/us/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=vi | Ứng dụng מגדילים -נדל"ן התחדשות עירונית - App Store
  - 6. https://redplus.co.il/blog/how-to-start-pinui-binui | איך לקדם פינוי בינוי בצורה נכונה מדריך מעשי לדיירים ולמארגנים
  - 7. https://play.google.com/store/apps/details?id=com.app.tenantshield | מגן דיירים התחדשות עירונית - Apps on Google Play
  - 8. https://www.build-app.co.il/אפליקציה-מותאמת-אישית-לחברת-ניהול-נכסים/ | אפליקציה מותאמת אישית לחברת ניהול נכסים - Build App
  - 9. https://yara-h.co.il/מאמרים/כך-אפליקציה-לניהול-בניין-משדרגת-את-שיר/ | כך אפליקציה לניהול בניין משדרגת את שירותי הניקיון והתחזוקה המונעת
  - 10. https://elite-urban-renewal-jgspke.sticklight.app/urban-renewal | מדריך התחדשות עירונית - app - Sticklight
  - 11. https://play.google.com/store/apps/details?id=il.co.magdilim.app&hl=gsw | מגדילים -נדל"ן התחדשות עירונית
- **ניהול חתימות דיירים** (status ok; AI Overview block: present, source links not captured)
  - 2. https://magdilim.co.il/100420251421/ | יוצאים לדרך: טיפים לדיירים לקידום פרויקט התחדשות עירונית
  - 3. https://cdn-media.web-view.net/i/zzffxddd22sp/_____________________13.pdf | מצגת של PowerPoint‏
  - 4. https://paragon-c.co.il/כיצד-לנהל-בקרת-תוכניות-שינויי-דיירים-ל/14/ | כיצד לנהל בקרת תוכניות שינויי דיירים לפני ביצוע בצורה מקצועית
  - 5. https://crm.support.apoint.co.il/he/kb/article/327/הגדרת-טפסים-במערכת-בילד-אפ | הגדרת טפסים במערכת בילד אפ
  - 6. https://www.rashuiot.co.il/html5/arclookup.taf?&_id=72635&did=1118&g=1118&title=����� ������ ������ ������� ������� | טיפים לקידום פרויקט התחדשות עירונית
  - 7. https://www.rashuiot.co.il/html5/arclookup.taf?&_id=72635&did=1118&title=����� ������ ������ ������� ������� | טיפים לקידום פרויקט התחדשות עירונית
  - 8. https://bhamim.co.il/שירותים/ | שירותים | בוני העמים - הנדסה ניהול ויזמות
  - 9. https://www.kehilot.co.il/ניהול-ועד/ | ניהול ועד
  - 10. https://www.myavne.co.il/פינוי-בינוי---שירותי-ארגון-דיירים-וניהול-פרויקט-התחדשות-עירונית-מטעם-בעלי-הדירות | פינוי בינוי - שירותי ארגון דיירים וניהול פרויקט התחדשות עירונית ...
  - 11. https://www.2all.co.il/web/files/Sites19/igal12/Files_484847_(15443).pdf | חוברת דיירים 2.2
- **פורטל דיירים התחדשות עירונית** (status ok; AI Overview block: absent)
  - 1. https://gov.il/he/departments/government_authority_for_urban_renewal/govil-landing-page | https://gov.il/he/departments/government_authority...
  - 2. https://www.rashuiot.co.il/html5/portalLookup.taf?_id=44933&did=1118&G=&SM= | החברה להתחדשות עירונית
  - 3. https://www.facebook.com/myavne.co.il/videos/פינוי-בינוי-עושים-בליווי-של-ציון-החדשה/960384221401632/ | ציון החדשה - התחדשות עירונית וחברתית הינה חברה מארגנת, המשמשת ...
  - 4. https://www.b-g.org.il/איך-מתחילים-תהליך-התחדשות-עירונית/ | איך מתחילים פרויקט התחדשות עירונית ופינוי-בינוי?
  - 5. https://magdilim.co.il/120220261055/ | מה זה מארגן דיירים בהתחדשות עירונית?
  - 6. https://meirovich-nadlan.co.il/פינוי-דיירים-התחדשות-עירונית/ | פינוי דיירים התחדשות עירונית, מידע חשוב שצריכים לדעת
  - 7. https://apps.apple.com/il/app/מגן-דיירים-התחדשות-עירונית/id1637421586 | מגן דיירים התחדשות עירונית - App Store - Apple
  - 8. https://dayarimm.co.il/ | דיירים התחדשות עירונית | צוות לארגון וליווי בעלי דירות
  - 9. https://www.facebook.com/groups/335318133184063/ | מינהלת דיירים לפינוי בינוי התחדשות עירונית תמ"א
  - 10. https://www.rashuiot.co.il/html5/portalLookup.taf?_id=44933&did=1118&G=8882&SM=8779 | החברה להתחדשות עירונית
- **CRM לחברה מארגנת** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.boss-sws.com/מערכת-crm/ | מערכת CRM | מערכת ניהול לקוחות
  - 3. https://smartup.co.il/blog/crm-for-small-businesses/ | מערכת CRM לעסקים קטנים: השוואה ובחירה (2026)
  - 4. https://hyp.co.il/blog/crm/ | מערכת CRM לעסק – איך לבחור מערכת ניהול קשרי לקוחות (ב-2026)
  - 5. https://scallacrm.co.il/עסקים-בינוניים/ | מערכת CRM לעסקים בינוניים | Scalla ...
  - 6. https://www.youtube.com/watch?v=EkWGSNpRF4A | השוואת מערכות CRM: איזו מערכת CRM הכי טובה לעסק?
  - 7. https://fixdigitalcrm.com/crm-לעסקים-קטנים-וגדולים/ | CRM לעסקים קטנים וגדולים
  - 8. https://www.voicenter.co.il/בלוג/מערכת-CRM | 5 מערכות CRM מומלצות שיקלו על ניהול העסק שלכם
  - 9. https://www.lastartup.co.il/blog/crm-guide-for-businesses | המדריך להקמת מערכת CRM מנצחת לעסק שלכם
  - 10. https://crmtoday.co.il/crm-system-implementation/ | בניית מערכת CRM לעסק לפי מה שהוא באמת צריך
  - 12. https://www.expert.co.il/reviews/מערכות-crm-מומלצות/ | השוואה בין מערכות CRM מומלצות + איך AI משתלב היום (מעודכן 2026)
- **תוכנה לניהול התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://apps.apple.com/us/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=vi&platform=ipad | Ứng dụng מגדילים -נדל"ן התחדשות עירונית - App Store - Apple
  - 3. https://apps.apple.com/gr/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=el | Εφαρμογή מגדילים -נדל"ן התחדשות עירונית - App Store - Apple
  - 4. https://apps.apple.com/vn/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=vi | Ứng dụng מגדילים -נדל"ן התחדשות עירונית - App Store
  - 5. https://odigital.io/case-studies/urban-renewal/ | מערכת שליטה לפרויקט התחדשות עירונית - ODIGITAL
  - 6. https://play.google.com/store/apps/details?id=il.co.magdilim.app&hl=en_CA | מגדילים -נדל"ן התחדשות עירונית - Apps on ...
  - 7. https://www.arcgis.com/home/item.html?id=18d81e8d301c49a686b9dfcbc82292ce&sublayer=7 | התחדשות עירונית אפליקציה בהתהוות_WFL1 - Overview
  - 8. https://il.appsillon.com/products/property-management-software | תוכנה לניהול נכסים - Appsillon
  - 9. https://stsiconic.com/crm-real-estate/ | מערכת CRM לנדל"ן
  - 10. https://kloyz.io/he/agencies | תוכנת ניהול נכסים לסוכנויות נדל"ן - Kloyz
  - 11. https://elite-urban-renewal-jgspke.sticklight.app/urban-renewal | מדריך התחדשות עירונית - app - Sticklight
- **מערכת ניהול חתימות פינוי בינוי** (status ok; AI Overview block: absent)
  - 1. https://binugo.com/ | BinuGo — מערכת ניהול להתחדשות עירונית, הדיירים בוואטסאפ
  - 2. https://www.comsign.co.il/חתימה-דיגיטלית-על-תמא-38-המהפכה-מגיעה-לה/ | חתימה דיגיטלית על תמ"א 38: המהפכה מגיעה להתחדשות עירונית
  - 3. https://onestep.co.il/software/hitchadshut-ironit | מערכת להתחדשות עירונית 2026: כל המסלולים במערכת אחת | OneStep
  - 4. https://bmby.co.il/התחדשות-עירונית/ | התחדשות עירונית
  - 5. https://asset-rise.byclick.co.il/ | Asset Rise — מערכת ניהול בניין ופינוי בינוי | תוכנת ניהול נדל״ן
  - 6. https://www.b-g.org.il/ | חברה מארגנת להתחדשות עירונית ופינוי בינוי | חברת ניהול וליווי דיירים
  - 7. https://easydo.co.il/solutions/פתרונות-דיגיטליים-לחברות-בנייה/ | פתרונות דיגיטליים לחברות בנייה
  - 8. https://doxi.co.il/חתימה-דיגיטלית-לניהול-תהליכי-שינויי-ד/ | חתימה דיגיטלית לתהליך שינויי דיירים בפרויקטי בנייה - Doxi
  - 9. https://www.gov.il/he/departments/government_authority_for_urban_renewal | הרשות הממשלתית להתחדשות עירונית
  - 10. https://www.crmleader.co.il/articles/crm-management-urban-renewal/ | מערכת CRM לניהול פרויקטים של תמ"א והתחדשות עירונית
- **אזור אישי דיירים התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.gov.il/he/departments/government_authority_for_urban_renewal | הרשות הממשלתית להתחדשות עירונית
  - 3. https://www.azorim.co.il/ | חברת אזורים: דירות למכירה, פרוייקטים חדשים
  - 4. https://www.b-g.org.il/ | חברה מארגנת להתחדשות עירונית ופינוי בינוי | חברת ניהול וליווי דיירים
  - 5. https://www.tel-aviv.gov.il/Residents/Development/Pages/UrbanRenewal.aspx | התחדשות עירונית
  - 6. https://onestep.co.il/software/hitchadshut-ironit | מערכת להתחדשות עירונית 2026: כל המסלולים במערכת אחת | OneStep
  - 7. https://www.kolzchut.org.il/he/מדריך_לתהליך_התחדשות_עירונית | מדריך לתהליך התחדשות עירונית
  - 8. https://azr.bartech-net.co.il/המינהלת-להתחדשות-עירונית/ | המינהלת להתחדשות עירונית - הוועדה המקומית לתכנון ובניה אזור
  - 9. https://search.getstatus.online/he | גט סטטוס | סטטוס הפרויקט, שקיפות והצעות מיזמים ומשרדי עו״ד ...
  - 10. https://auraisrael.co.il/התחדשות-עירונית/ | התחדשות עירונית | אאורה
  - 12. https://www.rom-m.co.il/ | רום התחדשות עירונית
- **אפליקציה תמ"א 38** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.nadlancenter.co.il/article/489 | תמ"א 38 - המדריך השלם לשנת 2026
  - 3. https://www.comsign.co.il/חתימה-דיגיטלית-על-תמא-38-המהפכה-מגיעה-לה/ | חתימה דיגיטלית על תמ"א 38: המהפכה מגיעה להתחדשות עירונית
  - 4. https://www.gov.il/he/pages/tama38-apps | תמ"א 38 ויישומה מינהל התכנון
  - 5. https://he.wikipedia.org/wiki/תמ"א_38 | תמ"א 38
  - 6. https://www.citysquare.co.il/ | תמ"א 38 ופינוי בינוי לפי ערים ויזמים סיטי סקוור בשיתוף TheMarker
  - 7. https://prlaw.co.il/עורך-דין-תמא-38/מה-זה-תמא-38-שאלות-ותשובות-על-תהליך-תמא-38/ | מה זה תמ"א 38: שאלות ותשובות על תהליך תמ"א 38
  - 8. https://handasa.ramat-gan.muni.il/rishui-tama-38/ | רישוי ותמ"א 38 - עיריית רמת גן - הנדסה
  - 9. https://shidrugurbani.co.il/2025/04/11/tama-38-in-israel-the-professional-guide-to-understanding-the-process/ | תמ"א 38 בישראל: המדריך המקצועי להבנת התהליך
  - 10. https://www.amidar.co.il/wps/portal/amidar/main-menu/urban-renewal/tama-38 | תמ"א 38
  - 13. https://www.facebook.com/cramim.pt/videos/אז-מה-ההבדל-בין-תמא-38-חלופת-שקד-ומסלול-פינוי-בינויבשביל-זה-אנחנו-כאןתמא-38-רלוו/1986106692130508/ | אז מה ההבדל בין תמ"א 38, חלופת שקד ומסלול פינוי בינוי? בשביל זה ...
- **חתימה דיגיטלית התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.comsign.co.il/חתימה-דיגיטלית-על-תמא-38-המהפכה-מגיעה-לה/ | חתימה דיגיטלית על תמ"א 38: המהפכה מגיעה להתחדשות עירונית
  - 3. https://www.nadlancenter.co.il/article/7161 | עורכי דין, תכירו: מערכת ההחתמות שמגיעה למאות דיירים בלחיצת ...
  - 4. https://tw-law.co.il/blog/digital-signature-real-estate/ | חתימה דיגיטלית בעסקאות מקרקעין: מותרת מ-2022 — אז למה זה עדיין ...
  - 5. https://www.facebook.com/comsign99/videos/חתימה-דיגיטלית-על-עסקאות-מקרקעין-במהירות-שטרם-היכרת/1796680841330995/ | חתימה דיגיטלית על עסקאות מקרקעין במהירות שטרם היכרת | קומסיין
  - 6. https://easydo.co.il/solutions/פתרונות-דיגיטליים-לחברות-בנייה/ | פתרונות דיגיטליים לחברות בנייה
  - 7. https://www.comsign.co.il/real-estate-tablets/ | נדל"ן Online | מהפכת החתימה הדיגיטלית בעסקאות מקרקעין
  - 8. https://land-registration.lawx.co.il/ArticleDetail?slug=digital-signature-real-estate-transactions-legal-guide | חתימה דיגיטלית בעסקאות מקרקעין: המדריך המשפטי המקיף
  - 9. https://www.gov.il/he/pages/digital_signature | חתימה דיגיטלית מערך הדיגיטל הלאומי
  - 10. https://marina-law.com/?p=596 | חתימה על הסכם התחדשות עירונית: המדריך המלא
  - 12. https://www.kolzchut.org.il/he/מדריך_לתהליך_התחדשות_עירונית | מדריך לתהליך התחדשות עירונית
- **urban renewal software Israel** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.runi.ac.il/en/research-institutes/economics/aiep/policy-papers/housing-market/urban-renewal-in-israel | Urban Renewal in Israel | Reichman University
  - 3. https://www.duns100.co.il/en/The_Urban_Renewal_Corporation | The Urban Renewal Corporation
  - 4. https://www.bsre.co.il/en/המדריך-לאורבניות-מתחדשת-כל-מה-שרציתם-ל/ | Everything You Wanted to Know About Urban Renewal but ...
  - 5. https://ytd38.co.il/en/urban-renewal | YTD Urban Renewal
  - 6. https://www.facebook.com/groups/TelAvivApartments/posts/27136080882649005/ | What is an urban renewal program in Israel and how does ...
  - 7. https://www.wblaw.co.il/en/practice/urban-renewal/ | Urban Renewal - Weksler Bergman & Co Law Firm
  - 8. https://www.ebnlaw.co.il/practice-areas/real-estate/urban-renewal/ | Urban Renewal
  - 9. https://tidhar.co.il/en/urban-renewal/ | Tidhar Urban Renewal
  - 10. https://herzoglaw.co.il/en/practice/real-estate/urban-renewal/ | Urban Renewal - Herzoglaw | Israeli Law Firm
  - 11. https://semerenkogroup.com/urban-renewal/ | Urban Renewal In Israel: TAMA 38 And Pinui Binui
- **pinui binui app** (status ok; AI Overview block: absent)
  - 1. https://www.buyitinisrael.com/guide/what-is-pinui-binui/ | What is Pinui-Binui?
  - 2. https://www.do-israel.com/en/pinui-binui-for-foreign-investors/ | Pinui Binui for Foreign Investors: An Israel Real Estate Guide
  - 3. https://gr-adv.co.il/en/pinui-binui-urban-renewal/ | Pinui-Binui (Urban Renewal) | Gal Rossabi Mor Law Office
  - 4. https://pinuibinui.reisdor.co.il/en/homepage/ | REISDOR Pinui-Binui - beit-shemesh - פרויקט פינוי בינוי - רייסדור
  - 5. https://manosgroup.co.il/en/evacuation-and-reconstruction-pinui-binui/ | Pinui Binui | Evacuation and reconstruction | Manos Group
  - 6. https://semerenkogroup.com/pinui-binui-2/ | Pinui Binui In Israel: Process, Records And Owner Terms
  - 7. https://www.buypropertyinisrael.com/articles/urban-renewal-the-israeli-way | Urban Renewal the Israeli Way | Buy Property In Israel
  - 8. https://www.ma-law.net/pinui-binui/ | Pinui Binui - MA Law
  - 9. https://isrealestate.co.il/guides/check-urban-renewal-and-future-development-plans | Check Pinui-Binui and Tama 38 Before Buying
  - 10. https://www.ytd38.co.il/en/FAQ | FAQ - YTD Urban Renewal
- **מערכת להחתמת דיירים התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.nadlancenter.co.il/article/2165 | חוק המארגנים (חוק התחדשות עירונית) - המדריך השלם לשנת 2026
  - 3. https://www.gov.il/he/departments/government_authority_for_urban_renewal | הרשות הממשלתית להתחדשות עירונית
  - 4. https://bmby.co.il/התחדשות-עירונית/ | התחדשות עירונית
  - 5. https://onestep.co.il/for/meargenim | מערכת למארגן פינוי בינוי | ניהול החתמת דיירים ואחוזי הסכמה | OneStep
  - 6. https://www.comsign.co.il/חתימה-דיגיטלית-על-תמא-38-המהפכה-מגיעה-לה/ | חתימה דיגיטלית על תמ"א 38: המהפכה מגיעה להתחדשות עירונית
  - 7. https://www.b-g.org.il/ | חברה מארגנת להתחדשות עירונית ופינוי בינוי | חברת ניהול וליווי דיירים
  - 8. https://easydo.co.il/solutions/פתרונות-דיגיטליים-לחברות-בנייה/ | פתרונות דיגיטליים לחברות בנייה
  - 9. https://www.kolzchut.org.il/he/מדריך_לתהליך_התחדשות_עירונית | מדריך לתהליך התחדשות עירונית
  - 10. https://asset-rise.byclick.co.il/ | Asset Rise התחדשות עירונית
  - 12. https://www.nadlan2u.co.il/תוכנת נדלן להתחדשות עירונית.html | תוכנה להתחדשות עירונית (תמ"א 38)
- **מנדיי התחדשות עירונית** (status ok; AI Overview block: absent)
  - 1. https://oracle-re.co.il/urban_renewal_projects/?nocache=1791452909 | כל מה שרציתם לדעת על פרויקטים של התחדשות עירונית
  - 2. https://oracle-re.co.il/urban_renewal_projects/?nocache=1791473773 | כל מה שרציתם לדעת על פרויקטים של התחדשות עירונית
  - 3. https://oracle-re.co.il/urban_renewal_projects/?nocache=1780210783 | כל מה שרציתם לדעת על פרויקטים של התחדשות עירונית
  - 4. https://magdilim.co.il/070120218-2/ | "מאות יזמי התחדשות עירונית נקלעו לקשיים בגלל הקורונה"
  - 5. https://www.ynet.co.il/topics/התחדשות_עירונית/29?prof=7755.vgnTopics-41232.Topics | התחדשות עירונית
  - 6. https://www.luach-nadlan.co.il/התחדשות-עירונית-חברות-מובילות/ | החברות המובילות בתחום ההתחדשות העירונית - הפורטל המשפטי לנדל"ן
  - 7. https://www.ynet.co.il/topics/התחדשות_עירונית/20 | התחדשות עירונית
  - 8. https://tld.walla.co.il/item/3675263 | כיצד התחדשות עירונית משנה את פני העיר וחיי הדיירים - טוב לדעת
  - 9. https://www.ynet.co.il/topics/התחדשות_עירונית/19 | התחדשות עירונית
  - 10. https://www.ynet.co.il/topics/התחדשות_עירונית/15 | התחדשות עירונית
- **פיירברי התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.checkid.co.il/company/אדמרל-התחדשות-עירונית-בע~מ-515209682 | אדמרל התחדשות עירונית בע"מ - 515209682 - CheckID
  - 3. https://www.facebook.com/peretzbh/posts/כחברה-שיוזמת-ומקימה-פרויקטים-של-התחדשות-עירונית-ברחבי-הארץ-אנחנו-רואים-את-זה-יום/1666186648846081/ | כחברה שיוזמת ומקימה פרויקטים של התחדשות עירונית ברחבי הארץ ...
  - 4. https://www.madlan.co.il/developer/SAPIR_URBAN_RENEWAL_G_Z | ספיר התחדשות עירונית (ג.ז.) בע"מ | לוח יזמי נדל"ן של ...
  - 5. https://www.mako.co.il/news-business/realestate/Article-1dc1910285f5b71027.htm | מדריך התחדשות עירונית מבית D&B | N12
  - 6. https://easy.co.il/page/9446481 | החברה להתחדשות עירונית - שדרות רוטשילד 11, תל אביב יפו
  - 7. https://www.rashuiot.co.il/html5/portalLookup.taf?_id=44933&did=1118&G=8776&SM=8779 | החברה להתחדשות עירונית
  - 8. https://www.facebook.com/shapir.megurim/photos/התחדשות-עירונית-הפכה-כבר-מזמן-מטרנד-נדלני-למציאות-מתבקשת-יותר-ויותר-רשויות-מקומי/5085351438222055/?locale=ms_MY | Shapir - התחדשות עירונית הפכה כבר מזמן מטרנד נדל ...
  - 9. https://www.fireberry.com/he/solution-catalog/wordpress-to-fireberry | קטלוג פתרונות: WordPress to Fireberry
  - 10. https://www.madlan.co.il/developer/DRUrbanRenewal | ד.ר התחדשות עירונית בע"מ | לוח יזמי נדל"ן של ...
  - 11. https://www.madlan.co.il/developer/DRUrbanRenewal | ד.ר התחדשות עירונית בע"מ | לוח יזמי נדל"ן של ...
- **תוכנה לחברה מארגנת התחדשות עירונית** (status ok; AI Overview block: absent)
  - 1. https://www.b-g.org.il/ | חברה מארגנת להתחדשות עירונית ופינוי בינוי | חברת ניהול וליווי דיירים
  - 2. https://www.gov.il/he/departments/government_authority_for_urban_renewal | הרשות הממשלתית להתחדשות עירונית
  - 3. https://klikatnadlan.co.il/organizingcompany/ | חברה מארגנת או בשמה השני מנהלת דיירים: מי היא ומה תפקידה?
  - 4. https://www.nadlan2u.co.il/תוכנת נדלן להתחדשות עירונית.html | תוכנה להתחדשות עירונית (תמ"א 38)
  - 5. https://www.barlev-nadlan.co.il/התחדשות-העירונית/חברה-מנהלת-להתחדשות-עירונית/ | חברה מנהלת להתחדשות עירונית
  - 6. https://search.getstatus.online/he/magazine/project-organizers | מארגני פרויקטים: המדריך המלא 2026 לבדיקת היתכנות וניהול חכם
  - 7. https://top-360.co.il/מארגן-דיירים/ | מארגן דיירים בהתחדשות עירונית
  - 8. https://yekutiel-law.co.il/חברה_מארגנת_המדריך_המקיף/ | חברה מארגנת: איך היא מסייעת לדיירים, מי משלם לה- וממה צריך להיזהר?
  - 9. https://www.rom-m.co.il/ | רום התחדשות עירונית
  - 10. https://bmby.co.il/התחדשות-עירונית/ | התחדשות עירונית
- **מעקב חתימות דיירים פינוי בינוי** (status ok; AI Overview block: absent)
  - 1. https://liam.org.il/איפה-יש-פינוי-בינוי/ | איך למצוא דירה לפינוי בינוי ומה חשוב לבדוק לפני?
  - 2. https://tasalaw.co.il/בדיקות-מקדימות-לפני-פרויקט-פינוי-בינו/ | בדיקות מקדימות לפינוי-בינוי: המדריך המשפטי המלא
  - 3. https://www.gov.il/he/departments/topics/mapa-renewal | מפת התחדשות עירונית בישראל
  - 4. https://www.facebook.com/groups/3303947573209051/posts/4512101025727027/ | איך לקבל יותר מידע על פרויקט פינוי בינוי לפני שאני נכנס לעסקה
  - 5. https://redplus.co.il/guides/pinui-binui-center | מרכז הידע לדייר
  - 6. https://www.karnafnadlan.com/blog/urban-renewal-how-to-check-2026 | קונים דירה בפינוי בינוי ב-2026: שלבים, לוחות זמנים אמיתיים ומה ...
  - 7. https://bashgroup.co.il/פרויקט-פינוי-בינוי/ | פינוי בינוי – המדריך השלם ושלבי המעקב בפרויקט
  - 8. https://dayarimm.co.il/ | דיירים התחדשות עירונית | צוות לארגון וליווי בעלי דירות
  - 9. https://asset-rise.byclick.co.il/ | Asset Rise — מערכת ניהול בניין ופינוי בינוי | תוכנת ניהול נדל״ן
  - 10. https://search.getstatus.online/he | גט סטטוס | סטטוס הפרויקט, שקיפות והצעות מיזמים ומשרדי עו״ד ...
- **אזור אישי לבעלי דירות התחדשות עירונית יזם** (status ok; AI Overview block: absent)
  - 1. https://www.ashtrom.co.il/articles/מגורים/urban-renewal-ashtrom-megurim | התחדשות עירונית? רק עם אשטרום מגורים
  - 2. https://yeshnadlan.co.il/התחדשות-עירונית-איך-עושים-את-זה-ומה-חש/ | התחדשות עירונית - איך עושים את זה ומה חשוב לדעת לפני יציאה ...
  - 3. https://yetedot.com/התחדשות-עירונית-2/ | התחדשות עירונית
  - 4. https://www.facebook.com/boldgroupnadlan/videos/מתחמי-התחדשות-עירונית-הולכים-ומגדילים-את-היקפיהם-ואיתם-גם-הצורך-בניהול-הפרויקט-ע/245169057795347/ | מתחמי התחדשות עירונית הולכים ומגדילים את היקפיהם, ואיתם גם הצורך ...
  - 5. https://apps.apple.com/il/app/מגדילים-נדל-ן-התחדשות-עירונית/id6502332829?l=he | היישום מגדילים -נדל"ן התחדשות עירונית - App Store
  - 6. https://givatayimplus.co.il/rsm111/ | מוסף התחדשות עירונית - מידע הכרחי בכל בית בישראל -
  - 7. https://m-y-s.com/HE/התחדשות-עירונית | התחדשות עירונית
  - 8. https://www.property-il.co.il/מסלולים-התחדשות-עירונית/ | מסלולים התחדשות עירונית, קראו מה האפשרויות שלכם - נדלן בארץ הקודש
  - 9. https://www.instagram.com/p/Dba0pfEo7Ly/ | העתיד של הבניין שלכם מתחיל בהחלטה אחת. בניינים ותיקים יכולים ...
  - 10. https://sagivgroup.com/בלוג/ | מידע ומאמרים בנושא התחדשות עירונית • Sagiv Group
- **monday.com urban renewal** (status ok; AI Overview block: absent)
  - 1. https://monday.com/ | The AI Workspace for People & Agents | monday.com
  - 2. https://il.linkedin.com/jobs/view/renewal-manager-at-monday-com-4128769462 | ‏monday.com‏ גיוס ‏Renewal Manager‏ עובדים | ‏Tel Aviv-Yafo‏ ...
  - 3. https://axxun.ch/en/monday-for-the-architects/ | Monday for Architects Urban Planners
  - 4. https://www.facebook.com/eyewitnessnewsbah/posts/local-the-urban-renewal-authority-was-officially-launched-on-monday-at-st-joseph/646145281128363/ | LOCAL: The Urban Renewal Authority was officially launched ...
  - 5. https://www.mondayspaces.com/spaces/monday-com-home-dashboard | monday.com Home Dashboard
  - 6. https://en.wikipedia.org/wiki/Monday.com | Monday.com
  - 7. https://monday.com/p/about/ | Our Story - monday.com
  - 8. https://monday.com/help | Contact Us
  - 10. https://uctoday.com/monday-com-repositions-as-ai-work-platform-putting-agents-at-the-centre-of-project-execution | monday.com Relaunches as an AI Work Platform
  - 11. https://community.monday.com/monday-pulse | monday Pulse
- **פריוריטי התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://magdilim.co.il/071220251249/ | יותר ויותר דיירים במתחמים ותיקים מגלים נכונות לקדם תהליכי פינוי בינוי
  - 3. https://re-build.co.il/category/urban-renewal/page/2/ | עמוד 2 – Rebuild - התחדשות עירונית
  - 4. https://tirosh.co.il/מוצרים-ויישומים/ | מוצרים ויישומים - תירוש מערכות מחשוב בע"מ
  - 5. https://www.srugim.co.il/tag/התחדשות-עירונית | התחדשות עירונית
  - 6. https://www.rashuiot.co.il/html5/?_id=8779&did=1118&g=8776&sm=8779&title=������� ������� | התחדשות עירונית
  - 7. https://bereshitgroup.co.il/פינוי-בינוי/ | פינוי בינוי - ניהול וליווי פרויקטים בהתחדשות עירונית
  - 8. https://priority-forums.com/he/forums/users/adma76/engagements/ | aviad
  - 9. https://www.facebook.com/lymwr.gl.mlk/posts/בהתחדשות-עירונית-הדרך-חשובה-לא-פחות-מהיעדלפעמים-יש-רצון-להגיע-כמה-שיותר-מהר-לתוצ/2557855011330559/ | בהתחדשות עירונית, הדרך חשובה לא פחות מהיעד. לפעמים יש רצון ...
  - 10. https://priority-forums.com/he/forums/users/buzagloasher/engagements/ | asherbuzaglo
  - 11. https://priority-forums.com/he/forums/users/talbendor/engagements/ | talbendor
- **מערכת ניהול נציגות דיירים** (status ok; AI Overview block: absent)
  - 1. https://www.minhelet-holon.co.il/events/נציגות-דיירים-תפקידים-אופן-בחירה-והתנ-2/ | נציגות דיירים – תפקידים, אופן בחירה והתנהלות בתאריך 08.02.2026
  - 2. https://www.din.co.il/forum45/514186/ | יצירת נציגות דיירים | פורום פינוי בינוי
  - 3. https://www.gov.il/he/pages/renewal_decision_23122024 | החלטת הממונה בעניין סמכות נציגות דיירים ופניות בעניין רשויות התכנון
  - 5. https://www.facebook.com/hitchadshuteronit/posts/מהי-נציגות-דייריםנציגות-דיירים-היא-התארגנות-נבחרת-ומוסכמת-מטעם-הדיירים-המייצגת-א/2631758793705133/ | הרשות הממשלתית להתחדשות עירונית
  - 6. https://forms-esderot.binaa.co.il/הסמכת-נציגות-דיירים-לקידום-פרויקט-התחדשות-עירונית-שדרות-ניצן-6/ | הסמכת נציגות דיירים לקידום פרויקט התחדשות עירונית שדרות - ניצן 6
  - 7. https://www.kiryat-yam.muni.il/288/ | פרוטוקול אסיפת דיירים לבחירת נציגות
  - 8. https://redirectx.co.il/he/guides/nezigut-dayarim-pinui-binui | נציגות דיירים בפינוי בינוי: תפקיד וסמכויות
  - 9. https://digagroup.co.il/services | השירותים שאנחנו מעניקים לדיירים - קבוצת דיגה
  - 10. https://app.legalup.me/create-wizard?WizardId=1251&OrgWizardId=2031 | פרטיכל אסיפת דיירים למינוי נציגות
  - 11. https://magdilim.co.il/070120261001/ | איך בונים נציגות דיירים טובה ומה התפקיד שלה?
- **תוכנה לעורכי דין התחדשות עירונית ניהול דיירים** (status ok; AI Overview block: absent)
  - 1. https://www.ask-lawyer.co.il/pages/התחדשות-עירונית-פינוי-בינוי-2026 | התחדשות עירונית פינוי בינוי: המדריך המקיף לשנת 2026 - שאל עורך דין
  - 2. https://gazitlaw.co.il/our_services/education-law/ | התחדשות עירונית – איתי גזית – משרד עורכי דין
  - 3. https://ramat-verber.co.il/עורכי-דין-המתמחים-בהתחדשות-עירונית/ | עורכי דין המתמחים בהתחדשות עירונית
  - 4. https://www.mishpati.co.il/article/16195 | הדייר פנה ליועץ לא מקצועי וכמעט שילם על כך בגדול
  - 5. https://agentskills.co.il/he/skills/legal-tech/israeli-urban-renewal-owner-guide | מדריך לבעלי דירות בהתחדשות עירונית - כלי AI
  - 6. https://nadlan.walla.co.il/item/3384261 | האם לשכת עורכי הדין תצליח לטפל בניגוד האינטרסים בהתחדשות עירונית?
  - 7. https://rf-law.co.il/איך-לבחור-עורך-דין-לייצוג-דיירים-בהתחד/pexels-sora-shimazaki-5668772/ | איך לבחור עורך דין לייצוג דיירים בהתחדשות עירונית - המדריך המלא
  - 8. https://newsadv.co.il/ethics/התחדשות-עירונית | מקרקעין והתחדשות עירונית
  - 9. https://www.facebook.com/61559122572967/posts/אחד-הגורמים-הכי-חשובים-בפרויקט-התחדשות-עירונית-הוא-עורך-דין-הדייריםהתפקיד-שלו-הו/122238568304304085/ | אחד הגורמים הכי חשובים בפרויקט התחדשות עירונית הוא עורך דין ...
  - 10. https://www.facebook.com/talkadarishamir/posts/תוהים-מה-תפקיד-עורך-דין-דיירים-בפרויקט-התחדשות-עירוניתעל-השאלה-הזו-בדיוק-ענה-אתמ/1290913466183787/ | תוהים מה תפקיד עורך דין דיירים בפרויקט התחדשות עירונית? על ...
- **אפליקציה ליזמי התחדשות עירונית ניהול דיירים** (status SE error 40101 on both tries; AI Overview block: absent)
  - no organic results returned
- **פורטל דיירים יזם פינוי בינוי עדכונים** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.gov.il/he/departments/government_authority_for_urban_renewal | הרשות הממשלתית להתחדשות עירונית
  - 3. https://magdilim.co.il/ | מגדילים – חדשות הנדל"ן בישראל, התחדשות עירונית, בנייה ויזמות בישראל
  - 4. https://www.kolzchut.org.il/he/מדריך_לתהליך_התחדשות_עירונית | מדריך לתהליך התחדשות עירונית
  - 5. https://www.nadlancenter.co.il/article/565 | פינוי בינוי - המדריך השלם לשנת 2026
  - 6. https://onestep.co.il/blog/pinui-binui-madrich-male | פינוי בינוי 2026: המדריך המלא ליזמים, ארגונים ודיירים | OneStep
  - 7. https://search.getstatus.online/he | גט סטטוס | סטטוס הפרויקט, שקיפות והצעות מיזמים ומשרדי עו״ד ...
  - 8. https://www.facebook.com/groups/3303947573209051/?locale=he_IL | פורום נפגעי התמ"א ופינוי בינוי
  - 9. https://socity.co.il/מדריך-פינוי-בינוי/ | מדריך פינוי בינוי - אל תצאו לפרויקט ב- 2026 בלי שקראתם
  - 10. https://www.tel-aviv.gov.il/Residents/Development/Pages/UrbanRenewal.aspx | התחדשות עירונית
  - 12. https://pinuibinui.org.il/ | החברה להתחדשות עירונית – התחדשות עירונית | פינוי בינוי | התחדשות ...
- **monday פינוי בינוי ניהול דיירים** (status ok; AI Overview block: present, source links not captured)
  - 2. https://magdilim.co.il/240320216/ | מדריך: שלבים חשובים בהליך פינוי הדיירים בפרויקט התחדשות עירונית
  - 3. https://oracle-re.co.il/evacuation_construction/?nocache=1791097080 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 4. https://www.facebook.com/groups/335318133184063/ | מינהלת דיירים לפינוי בינוי התחדשות עירונית תמ"א
  - 5. https://oracle-re.co.il/evacuation_construction/?nocache=1787358553 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 6. https://www.myavne.co.il/פינוי-בינוי---שירותי-ארגון-דיירים-וניהול-פרויקט-התחדשות-עירונית-מטעם-בעלי-הדירות | פינוי בינוי - שירותי ארגון דיירים וניהול פרויקט התחדשות עירונית ...
  - 7. https://oracle-re.co.il/evacuation_construction/?nocache=1789197114 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 8. https://oracle-re.co.il/evacuation_construction/?nocache=1792324275 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 9. https://oracle-re.co.il/Evacuation_Construction/?nocache=1791407829 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 10. https://oracle-re.co.il/evacuation_construction/?nocache=1792328302 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 11. https://www.instagram.com/reel/DeY9YhUujvZ/ | #פינויבינוי #ליווי #התחדשות_עירונית #נדלן #ארגון
- **פאוורלינק פינוי בינוי** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.b-g.org.il/ | חברה מארגנת להתחדשות עירונית ופינוי בינוי | חברת ניהול וליווי דיירים
  - 3. https://afikim38.com/pinuy-binuy/ | פינוי בינוי -מאמרים ותחקירים מקצועיים - פינוי ובינוי | התחדשות עירונית
  - 4. https://ken-hator.com/articles/initiated-evacuation-and-reconstruction | יזם פינוי בינוי: תהליך, יתרונות, ואתגרים בפרויקטים של התחדשות ...
  - 5. https://magdilim.co.il/180120260947/ | פינוי בינוי - המדריך השלם לתהליך התחדשות עירונית 2026
  - 6. https://pinuibinui.org.il/ | החברה להתחדשות עירונית – התחדשות עירונית | פינוי בינוי | התחדשות ...
  - 7. https://oracle-re.co.il/Evacuation_Construction/?nocache=1791206454 | פינוי בינוי - אוראקל יזמות נדל״ן
  - 8. https://top-360.co.il/קידום-פרויקט-פינוי-בינוי/ | קידום פרויקט פינוי בינוי
  - 9. https://bashgroup.co.il/יזם-פינוי-בינוי/ | יזם פינוי בינוי: תפקיד, בחירה וסיכונים
  - 10. https://www.gov.il/he/pages/madrich_pinuy_binuy | מדריך לדיירים לעקרונות התקשרות עם יזם בפרויקטים של פינוי-בינוי
  - 12. https://hl-jerusalem.co.il/ | החברה להתחדשות ירושלים - בעלי דירות מובילים להצלחה
- **docusign התחדשות עירונית** (status partial (page 1 only); AI Overview block: present, source links not captured)
  - 2. https://apps.land.gov.il/IturTabotData/takanonim-h/telmer/5050657.pdf | תכנית מס' 501-0418848 התחדשות עירונית ברחוב הרב ברוט 2,4,6 ...
  - 3. https://www.mako.co.il/news-business/duns_100-podcasts/Article-cdf100eb710c091026.htm | מה צריך לבדוק לפני שבוחרים יזם לפרויקט התחדשות עירונית? | N12
  - 4. https://www.instagram.com/p/DdCHqVBkYAY/?hl=af | יש לכם הסכם התחדשות עירונית ביד? עורך דין בודק את ההסכם. ...
  - 5. https://support.docusign.com/s/document-item?language=it&_LANG=ja&bundleId=zvs1609261769668&topicId=pvd1609261913347.html | Real Estate Forms
  - 6. https://www.docusign.com/en-gb/customer-stories/industry/real-estate | Real estate
  - 7. https://www.instagram.com/reel/C4-ZwqmMg6y/ | הבניין שלכם עובר תהליך התחדשות עירונית? שימו לב על מה היזם ...
  - 8. https://support.docusign.com/s/document-item?language=pt_BR&bundleId=xns1707952462017&topicId=reh1707952571396.html | Rooms for Real Estate
  - 9. https://www.instagram.com/p/DW27LQxl6Ug/ | התחדשות עירונית היא הזדמנות מרגשת לשדרג את איכות החיים, אך ...
  - 10. https://support.docusign.com/s/document-item?language=en_US&nocache=https://support.docusign.com/s/document-item?language=pt_BR&bundleId=zvs1609261769668&topicId=ota1609262703669.html&_LANG=jajp | Add Your Real Estate Form Provider Credentials
- **sign-it פינוי בינוי חתימה** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.comsign.co.il/חתימה-דיגיטלית-על-תמא-38-המהפכה-מגיעה-לה/ | חתימה דיגיטלית על תמ"א 38: המהפכה מגיעה להתחדשות עירונית
  - 3. https://www.gov.il/BlobFolder/generalpage/heskem-pinuy-binuy-ledugma/he/hithadshut_ironit_documents_madrich_heskem_pinuy_binuy.pdf | מדריך להסכם פינוי בינוי
  - 4. https://mitar.co.il/articles/do-you-have-to-sign | האם חייבים לחתום על פינוי בינוי? מה קורה אם לא חותמים - מתאר
  - 5. https://www.nadlancenter.co.il/article/565 | פינוי בינוי - המדריך השלם לשנת 2026
  - 6. https://www.minheletyavne.org.il/מדריך-להסכם-פינוי-בינוי/ | מדריך להסכם פינוי בינוי
  - 7. https://shovalbinui.co.il/north-haifa/urban-renewal-agreement/ | חוזה פינוי בינוי: כל מה שצריך לדעת לפני שחותמים על הסכם עם יזם
  - 8. https://rubin.law/מה-חשוב-לדעת-לפני-חתימה-על-הסכם-פינוי-בי/ | מה חשוב לדעת לפני חתימה על הסכם פינוי-בינוי | עו"ד התחדשות ...
  - 9. https://yonilevy.co.il/עורך-דין-פינוי-בינוי/no-shop-exclusivity-pinui-binui/ | טופס נון-שופ וכתב בלעדיות בפינוי בינוי: האם לחתום?
  - 10. https://www.amidor.co.il/construction-evacuation-agreement/ | הסכם פינוי בינוי: מה חייב להיות בו ומה בודקים לפני שחותמים
  - 12. https://www.gov.il/he/government-service-branches/moh-tel-aviv-doctor-signature-verification | אימות חתימה של רופא ישראלי לצורכי מסמכים בחו"ל - מחוז תל אביב
- **אפליקציה לבעלי דירות פינוי בינוי עדכונים יזם** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.ynet.co.il/economy/article/rkmZKXpbw | איך מזהים מאכער ואילו תוספות מגיעות לכם? כך תדעו שלא עובדים ...
  - 3. https://www.instagram.com/reel/Dcq1dJ-N1tW/ | איפה יהיה פינוי בינוי בעיר שלכם ? האתר הפשוט ביותר להבנה . ...
  - 4. https://magdilim.co.il/3011202119-2/ | מדריך לדיירים: איך ישפיע חוק ההסדרים החדש על מיזמי פינוי-בינוי?
  - 5. https://www.facebook.com/100052215742850/posts/אז-איך-יודעים-שבטוח-יהיה-פינוי-בינויבזמן-האחרון-כולם-רוצים-לקנות-דירה-ש-בטוח-תעב/465925224996905/ | אז איך יודעים שבטוח יהיה פינוי בינוי? בזמן האחרון כולם ...
  - 6. https://www.maariv.co.il/news/law/article-823226 | פרויקט פינוי בינוי: האם מדובר בהזדמנות פז לדירה חדשה בעיר?
  - 7. https://www.lawforums.co.il/question/257280/ | מהן האפשרויות לדיירים במיזם פינוי-בינוי כאשר יש הבדלים בשטח ...
  - 8. https://www.facebook.com/groups/920867992008970/posts/2383194942442927/ | פינוי בינוי - יזמים, קבלנים , תושבים, ועדות , עורכי דין, שמאים ...
  - 9. https://www.ey-group.co.il/פינוי-בינוי-המדריך-המלא-2024/ | פינוי בינוי - המדריך המלא 2024
  - 10. https://magdilim.co.il/220320261140/ | איך מבטיחים ששכר הדירה שהיזם משלם באמת יספיק לאורך כל ...
  - 11. https://www.facebook.com/groups/920867992008970/posts/2383683825727372/ | פינוי בינוי - יזמים, קבלנים , תושבים, ועדות , עורכי דין, שמאים ...
- **מערכת דיגיטלית לליווי דיירים התחדשות עירונית** (status ok; AI Overview block: present, source links not captured)
  - 2. https://www.facebook.com/p/התחדשות-עירונית-100031153226305/?locale=he_IL | התחדשות עירונית | Lod
  - 3. https://www.facebook.com/groups/335318133184063/ | מינהלת דיירים לפינוי בינוי התחדשות עירונית תמ"א
  - 4. https://osltd.co.il/digital-building-management-apps-and-tools/ | ניהול ועד בית דיגיטלי: אפליקציות וכלים שמשדרגים את איכות החיים בבניין
  - 5. https://portal.vplans.com/he/ildc | פורטל דיירים | הכשרת הישוב התחדשות עירונית - VPlans
  - 6. https://go38.co.il/ליווי-דיירים/ | ליווי דיירים: הדרך הבטוחה להצליח בהתחדשות עירונית
  - 7. https://www.instagram.com/reel/DeY9YhUujvZ/ | #פינויבינוי #ליווי #התחדשות_עירונית #נדלן #ארגון
  - 8. https://redirectx.co.il/he/portal | פורטל דיירים - Redirectx פינוי-בינוי
  - 9. https://www.myavne.co.il/פינוי-בינוי---שירותי-ארגון-דיירים-וניהול-פרויקט-התחדשות-עירונית-מטעם-בעלי-הדירות | פינוי בינוי - שירותי ארגון דיירים וניהול פרויקט התחדשות עירונית ...
  - 10. https://www.facebook.com/cityliferenewal/posts/786901200323242/ | סיטי לייף - ליווי דיירים בהתחדשות עירונית
  - 11. https://www.myrishon.co.il/ארגון-וליווי-דיירים-בהתחדשות-עירונית-הדרך-הבטוחה-לבית-חדש | ארגון וליווי דיירים בהתחדשות עירונית - הדרך הבטוחה לבית חדש

Query that never returned results after two tries: "אפליקציה ליזמי התחדשות עירונית ניהול דיירים" (SE error 40101). Queries that returned only generic results (no renewal-specific product): "CRM לחברה מארגנת", "מנדיי התחדשות עירונית", "monday.com urban renewal", "monday פינוי בינוי ניהול דיירים", "פיירברי התחדשות עירונית", "פריוריטי התחדשות עירונית", "פאוורלינק פינוי בינוי", "docusign התחדשות עירונית", "sign-it פינוי בינוי חתימה", "urban renewal software Israel", "pinui binui app".

---

## Looked at and excluded

| Item | URL | Why excluded |
|---|---|---|
| מגדילים app | https://apps.apple.com/il/app/…/id6502332829 · play.google.com il.co.magdilim.app | News and content app (category News), not a management tool [S]. Same seller (SHTIBEL COM LTD) as מגן דיירים. |
| monday.com | monday.com (SERP q14, q19, q25) | No Hebrew urban-renewal template or partner page found in Google. Only generic construction tutorials. EasyDo lists monday as an integration. |
| Fireberry (Powerlink) | fireberry.com/he/solution-catalog/… (SERP q15) | Only generic catalog pages (WordPress connector, service portal). No renewal template found. |
| Priority | priority-forums.com, prioritysoftware (SERP q20) | No renewal-specific offering found; only forum users and a job ad. |
| DocuSign | support.docusign.com, docusign.com real-estate stories (SERP q27) | No Israeli urban-renewal page. Generic real-estate forms. |
| Sign-it / vSign / 2sign / PID Signit / Rivhit | SERP q10, q28 | Generic e-signature vendors; no page targeting urban renewal seen in results. Not read. |
| Cligal | https://cligal.com/cligal-real-estate-signing/ | Real-estate signing for lawyers (SERP: saves multi-signer projects, e.g. at conferences). Not read in full; similar class to ComSign. Follow-up candidate. |
| Doxi | doxi.co.il (SERP) | E-signature for buyer "שינויי דיירים" in new construction, not renewal consent. |
| Edji (אדג׳י) | edji.net | Buyer tenant-change management (plans, change requests). Not renewal. |
| GoMixApp | https://gomixapp.co.il/טפסים-דיגיטליים-מאובטחים-להחתמת-דייר/ | Generic signed digital forms; has a פינוי בינוי form; ₪140/month, ₪1,512/year, ₪3,980/3 years before VAT [S]. A form tool, not a consent manager. Kept as price reference only. |
| Ziv Systems / Assets One | https://ziv.co.il/יזמים/ | Developer ERP; lists פינוי בינוי, "תיק דייר", workflows with "חתימות דיגיטליות"; no resident portal, no consent %; price not published [S]. Developer back-office, not an organizer tool. |
| Mitar (מתאר) | https://mitar.co.il/ | Engineering consulting with free check tools and a national database; ₪399 / ₪599 consults [S]. Not a management system. |
| ODIGITAL | https://odigital.io/case-studies/urban-renewal/ | Custom CRM build case study for one unnamed client; AI layer "planned" [S]. Agency, not a product. |
| CRM Leader article | https://www.crmleader.co.il/articles/crm-management-urban-renewal/ | Generic article on what a CRM for TAMA 38 should do; no product named [S]. |
| ESTIQ | https://www.estiqapp.com/guide/urban-renewal | SERP shows an app with a renewal module (create project, add residents and units, milestones). Not read: follow-up candidate. |
| Sticklight "Urban Elite" | elite-urban-renewal-jgspke.sticklight.app | A renewal company's guide app (content). |
| LegalUp | app.legalup.me/create-wizard?WizardId=1251 | Document wizard for a residents' assembly protocol to appoint a committee. Template, not a tool. Not opened (wizard form). |
| CitySquare | citysquare.co.il | Media/directory of TAMA 38 and pinui-binui projects by city (with TheMarker). |
| asMade "פורטל דיירים" | asmade.co.il/kb/article.asp?g=tenant-portal | Knowledge-base pages of a tenant portal product; SERP suggests building/property management. Not read. Follow-up candidate. |
| House-committee apps (Livy, VaadOS, Build App, MyTower, kehilot) | livy.co.il, vaados.io, build-app.co.il | ועד בית / building management, not renewal. |
| Dimri tenants app (דמרי דיירים) | apps.apple.com id1476189190 | For buyers in Dimri projects, not renewal owners. |
| Kloyz, Appsillon, Insight Pro, FlowMyHome, Kliv | various | Property management, construction QA or budgeting; not renewal consent. |
| Organizer company sites (b-g.org.il, dayarimm.co.il, rom-m.co.il, citylife, mayagroup, minhelet-dayarim, redplus) | various | Service companies' marketing pages; no tool described. |
| Municipal administrations (minhelet-j, minhelet-holon, haminhelet Ramla, Tel Aviv, Jerusalem) | various | Information sites for residents; only Ramat Gan's app (משתדרגים) was kept as an example. |
| gov.il pages | gov.il (several) | Cloudflare challenge (HTTP 403) on automated reading. Kept as product 16 using SERP snippets only; not solved or bypassed. |
| ComSign site | comsign.co.il | Incapsula block. Kept as product 12 using a third-party article and SERP snippets. |
| Amidar / Ramdor | funder.co.il/article/121574 | Construction project management (engineering, budget) at Amidar; not resident consent. |

Not opened on purpose: every login page (app.onestep.co.il, app.binugo.com, app.redirectx.co.il, app.getstatus.online, app.rolyhome.com, asset-rise /login and /register, portal.vplans.com/he/ildc), every demo/contact/sign-up form, every trial.
