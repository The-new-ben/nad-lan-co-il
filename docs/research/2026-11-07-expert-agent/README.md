# The NadLan real-estate advisor (HAD-680): research, design, prototype

Ben, 7.11.2026: an advisor that talks like someone with 40 years in Israeli real estate, "like a serious agent with a broker's whole résumé", designed with Claude Design, tested on a few pages first. "Do not write that it is a broker."

## What is here
| File | What |
|---|---|
| `israel-deal-practice.md` | What a veteran does across a deal in Israel (buyer, developer, seller, rentals, urban renewal, abroad, negotiation) and the legal frame, with sources retrieved 7.11.2026 |
| `world-ai-assistants.md` | What Zillow, Redfin, Compass, Realtor.com, Homes.com, Rightmove, Zoopla, Idealista, REA, Madlan AI and others do, their guardrails and published numbers |
| `SKILLS-MAP.md` | 16 skills: what the advisor does, the tool or data it uses, the line it never crosses |
| `design/` | Claude Design v107 ExpertAdvisor (published to the design system, version 276) |
| `build/` | Offline unit test (43 checks), the provider test harness, the saved test conversations (`t1`-`t5`), the design-card builder |

Code: `plugins/nadlan-config/inc/expert-advisor.php`, `assets/expert-advisor/advisor.css`, `assets/expert-advisor/advisor.js`. Release: `scripts/project-stage/make_deploy603.py` -> `deploy603.py` (1.72.603).

## The persona and its résumé (honest)
- Name on the page: "יועץ הנדל״ן" ("the NadLan advisor"). Kicker: "יועץ ממוחשב · ידע של 40 שנה בנדל״ן הישראלי".
- The title block says who answers: "יועץ ממוחשב. לא אדם ולא מתווך." The line under the question box says an AI answers, not a person; general information, not legal, tax or financial advice; questions go to an outside AI provider and are not stored on the site.
- It never invents a name, a licence, past clients or deals. "40 years" is the knowledge it is built on (the veteran's playbook in its instructions), never a claimed career.

## Legal frame (summary; details in israel-deal-practice.md section 8)
- **Brokers Law s.2(c):** the site is a publisher only while it never presents itself as a broker. The advisor teaches and prepares; it never matches a buyer with a seller, arranges viewings, negotiates, passes offers or prices, or says "buy this one". The team form says the NadLan team will get back to them, nothing more. Haiku 5.5 failed this in a test (it said the team would arrange a viewing and pass the offer); Sonnet 5.5 passed, and an explicit rule now forbids that wording.
- **Reserved professions:** no contract or memorandum drafting (lawyers), no valuation of a specific home (licensed appraisers).
- **Privacy, Amendment 13 s.11:** the full notice sits at the form (voluntary, consequence of refusing, what is kept, by whom with contact, for what, not passed to a developer or broker unless asked, the rights to see, correct, delete) with a required consent box. The conversation itself is not stored on the site; only counters.
- **Honesty law:** numbers from the site's own data files with their date; project facts only "according to the page"; no availability it does not have.
- **Anti-discrimination:** never describes an area by who lives there (tested: a question about a religious family was answered with facts, not population).
- Open for a lawyer before going public: AI disclosure wording, the outside AI provider in the privacy policy, and the cost of a wrong figure.

## Cost per conversation (measured 7.11.2026, Sonnet 5.5 through OpenRouter)
- 16 test questions cost 0.24 USD in all, about 0.015 USD a question with the provider's cache.
- A typical conversation of 5 questions: about 0.08 USD, roughly ₪0.25 (BoI rate 3.112, 23.10.2026).
- 1,000 conversations a month: about ₪250. The daily cap on the site is 3 USD (about ₪9.3, roughly 190 questions a day); the OpenRouter key itself has a 10 USD limit.
- A cheaper model (Haiku 5.5) costs about 1/15 of that, but failed the broker test once: not recommended without more testing.

## Prototype (1.72.603), seen only with ?advisor=on
- https://nad-lan.co.il/buying-apartment/?advisor=on (Hebrew guide)
- https://nad-lan.co.il/projects/hamedina/?advisor=on (project page; not Ashira)
- https://nad-lan.co.il/en/buy-property-in-israel/?advisor=on (English, buyers abroad)
Without the parameter the pages are unchanged (checked by the runner on each page and by tools/source_audit.py before and after).

## Decisions only Ben can make
1. The name and the persona (default "יועץ הנדל״ן"; options: a first name with a clear "יועץ ממוחשב" label, or "הוותיק").
2. Which pages get it when it goes public, and where on the page.
3. The cost: a monthly budget and a dedicated key for nad-lan (the prototype uses the existing OpenRouter key with its 10 USD limit).
4. Whether to keep anonymised conversations for quality checks (today nothing is kept).
