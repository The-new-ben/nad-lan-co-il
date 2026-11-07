# ExpertAdvisor

**Version 107 (7.11.2026): the NadLan real-estate advisor, a section inside the page where a visitor talks with an AI advisor that carries the working knowledge of 40 years in Israeli real estate.** A prototype for Ben's review, seen only with `?advisor=on` on three test pages (Linear HAD-680).

Ben, 7.11.2026: "like a serious agent with a broker's whole résumé and 40 years of experience ... designed with Claude Design ... to test on certain pages". And: "do not write that it is a broker".

## Benchmark: what the leaders do, and where we go one step further
| | Redfin (Ask Redfin) | Rightmove / Zoopla | Zillow | Madlan AI (22.10.2026) | **Ours** |
|---|---|---|---|---|---|
| **Where** | In the search bar and the listing page | A chat window next to search | Inside the app | A free-text search | **A section inside the guide or the project page, in the reading order. No bubble, nothing fixed on the screen** |
| **Main job** | Questions about the home on screen | Search and compare | Search, affordability | Find apartments | **The whole deal: budget, mortgage, checks, negotiation, contract, delivery** |
| **Numbers** | Listing data | Listing data | Zestimate | Its own data | **Purchase tax, mortgage payment and total cost computed from the site's official data files (Tax Authority, Bank of Israel), each with its source and date** |
| **Honesty** | "No match" answers | | Fair-housing checker | | **Says it is an AI, not a person and not a broker; prices only "according to the page"; no availability it does not have** |
| **Next step** | Book a tour (Redfin is a brokerage) | Lead to the agent | Agent | | **A short form to the NadLan team, with the full privacy notice. No viewings, no offers passed on: the site stays a publisher** |

## Palette and faces (and why it is not the default look)
- NadLan Instruments: ground `#F6F8F9`, surface `#FFFFFF`, ink `#12202A`, ink-2 `#3E4C58`, mute `#5E6A75`, line `#D3DCE2`, sea `#2F6F86`, sea-deep `#1F4B5C`, survey `#C42550`, plan colours open `#4F9A5C` and civic `#8E7CC3` for data bars only.
- Karantina 700 for the Hebrew title (60px desktop, 46px phone), IBM Plex Sans Hebrew for everything read or touched, IBM Plex Mono for every figure. English: IBM Plex Sans Condensed 600 for the title, IBM Plex Sans for text.
- Taken from a surveyor's working sheet and Israeli planning maps: a **title block** (who answers, what it knows, where the numbers come from, the cost), the **stages of a deal** as a numbered track that lights up as the conversation moves, the conversation as **ruled field-log entries** (dashed rules, a small "היועץ · 19:13" line), results as **readout cells** with the one deciding figure underlined in survey red.
- Not the default: no chat bubble, no avatar, no gradient, no cream or gold, no soft-shadow cards, no coloured left border. Borders, not shadows.

## Anatomy
1. Head: kicker "יועץ ממוחשב · ידע של 40 שנה בנדל״ן הישראלי", title "שאלו את יועץ הנדל״ן", one line on what you get.
2. Title block (start side on desktop, on top on a phone): מי עונה, מה הוא יודע, מספרים, עלות.
3. Deal track: תקציב, משכנתא, בחירה, בדיקות, משא ומתן, חוזה, מסירה. The current stage in sea, the past ones outlined.
4. "מה היועץ לא עושה" (collapsed): not a broker, no viewings, no negotiating for you, does not tell you what to buy, does not replace a lawyer, an appraiser or a mortgage adviser, does not invent prices or availability.
5. The log: the visitor's question in a ground cell at the end side; the advisor's answer as plain text: the direct answer first, "מה עושים עכשיו" bullets, one question to move on.
6. Readout cells under an answer when a calculation ran: purchase tax with its brackets, the monthly payment, the cash needed (equity + costs as a bar). Source and date under each, a link to the full calculator.
7. Suggestions: three starting questions per page type, then the two follow-ups the advisor proposes.
8. The question box with a line under it: an AI answers, not a person; general information; questions go to an outside AI provider and are not stored on the site; do not type ID or bank numbers.
9. "לשיחה עם אדם" opens the team form: name, phone, email (optional), the full notice (voluntary, what is kept, by whom, for what, not passed to a developer or broker unless asked, the right to see, correct, delete), a required "מסכימים" box. It posts to the site's existing lead route.

## Placement
- Guide: after the opening section (H1, the answer paragraph, the CTA), before the article. Project page: after the map. The article and the stage keep their order.
- Phone: one column, the title block on top, every control 44px or taller, the question box in the page (the WhatsApp bar keeps its place).

## Rules the advisor follows (in its instructions on the server)
- An AI, never a fake person, never a licence. Never a broker: no matching, no viewings, no negotiating or passing offers, no "buy this one". No contract drafting, no valuation of a specific home.
- Facts about a project only from the page itself; numbers only from the tools and the dated official block; no promises; no steering by any group; no names on negative topics.

## Evidence
- The three previews run the PRODUCTION `advisor.css`, `advisor.js` and the markup printed by `inc/expert-advisor.php`, replaying answers the model actually gave on 7.11.2026 (built by `docs/research/2026-11-07-expert-agent/build/build_preview.py`).
