# Meier on Rothschild EN-FR independent QA review

Audit date: 2026-08-05  
Scope: read-only review of `meier-on-rothschild-en.md` and `meier-on-rothschild-fr.md` against `00-source-ledger.md`, `01-live-google-intent-ledger.md` and the frozen EN/FR delivery gates. No article, site, code, media or other package was edited.

## Verdict

The French article passes the frozen content, factual, language and parity gates. It uses the same project facts, dated market evidence, source uncertainties and buyer safeguards as the English article. It is a native French buyer product rather than a literal translation. No invented price, inventory, address, completion promise, apartment feature, view, amenity entitlement, financing result, tax outcome, yield or appreciation claim was found.

One shared release dependency remains outside the factual and language copy: both articles link contextually to the site's existing percent-encoded Hebrew city slug. That URL returns HTTP 200, but it conflicts with the site's ASCII-only public URL governance. No tested ASCII city alternative currently resolves. Exact affected lines and handling are recorded under Findings. This is not an EN-FR parity defect, and the articles should not be pointed to a guessed 404 replacement.

## Frozen inputs and line-reference integrity

All line references below are 1-based and apply to these exact file snapshots:

| File | Lines | Bytes | SHA-256 |
|---|---:|---:|---|
| `00-source-ledger.md` | 134 | 15,959 | `3d67e1ee1c53f3305dd5c930fa3c255157dd3b49fc4b7b85c5cddc1818c5af7e` |
| `01-live-google-intent-ledger.md` | 187 | 11,515 | `a2df0bff692d756f18793e695d0b6b20e7adcf41d9f4aff87a152800bd735e2c` |
| `meier-on-rothschild-en.md` | 427 | 47,303 | `c1d62db74b9ce41522c621b982775b09ee20897ea3060165103ad0475d1a7fd3` |
| `meier-on-rothschild-fr.md` | 486 | 62,976 | `6ded2abcb018cfee57f5cb68f1c44ad7570974d85a76d371bf07e63b590a5fd7` |

## Structural acceptance matrix

| Gate | English evidence | French evidence | Result |
|---|---|---|---|
| One project-first H1 | Exact H1 at EN line 1 | Exact required H1 at FR line 1: `Meier on Rothschild appartement à vendre à Tel Aviv - prix, revente et vérifications avant achat` | Pass |
| Localized primary query in H1 | `Meier on Rothschild apartments for sale` at EN line 1 | `Meier on Rothschild appartement à vendre` at FR line 1 | Pass |
| Data-rich opening | Completed and occupied status, 36 Rothschild, Tel Aviv, inventory status, current price-list status, resale and unit verification at EN line 3 | Same decision facts and uncertainty at FR line 3 | Pass |
| First 150 words | Contains Meier on Rothschild, Tel Aviv, apartments, price, buying, completed, resale and unit-specific verification in EN lines 1-3 | Contains Meier on Rothschild, Tel Aviv, appartement/appartements, prix, achat/acheter, achevée, occupée, revente and unit-specific verification in FR lines 1-3 | Pass |
| At least 5,000 lexical words before Sources | 6,480 | 8,841 | Pass |
| Exactly nine H2s | EN lines 7, 44, 78, 135, 199, 223, 261, 318 and 408 | FR lines 7, 50, 96, 175, 254, 276, 314, 373 and 467 | Pass |
| Required H2 order | Overview; Location and surroundings; The tower and apartments; Prices and estimates; The developer; Project stages; Who it suits; Frequently asked questions; Sources | Vue d'ensemble; Emplacement et environnement; La tour et les appartements; Prix et estimations; Le promoteur; Étapes du projet; À qui cela convient; Questions fréquentes; Sources | Pass |
| Exactly four contextual internal links before Sources | EN lines 34, 52, 181 and 183 | FR lines 34, 58, 232 and 236 | Pass |
| Exactly ten image-alt suggestions | EN heading at line 120 and items at lines 124-133 | FR heading at line 160 and items at lines 162-171 | Pass |
| Independent-site statement | EN line 5 | FR line 5 | Pass |
| Required estimate wording | `estimate, not binding` at EN line 166 | Exact `estimation, non contractuelle` at FR lines 208 and 210 | Pass |
| No em dash or en dash | Zero `—`; zero `–` | Zero `—`; zero `–` | Pass |
| No forbidden robotic phrases | No English equivalent of the frozen forbidden phrases found | No `Il est important de noter`, `En conclusion`, `Il ne fait aucun doute`, `À l'ère` or `Dans un monde où` found | Pass |
| No target-language leak | English body is consistently English apart from names and official terms | French body has no Hebrew, Arabic or Cyrillic characters and no English fallback sentence; English strings are proper names such as The Skyscraper Center and Richard Meier & Partners | Pass |

The four-link count excludes S01 in the mandatory Sources list. S01 is a source-parity requirement, not a contextual body link.

## Fact and uncertainty parity matrix

| Fact area | English evidence | French evidence | Ledger treatment retained | Result |
|---|---|---|---|---|
| Identity, address and current state | EN lines 3, 11 and 19 | FR lines 3, 11 and 19 | 36 Rothschild Boulevard at Allenby, Tel Aviv-Yafo; completed and occupied; not Shadal | Pass |
| Current inventory and project-wide price list | EN lines 3, 23-24 and 137-141 | FR lines 3, 23-24 and 177-181 | Neither a complete current inventory nor a current project-wide price list is published | Pass |
| Principal architect and architect of record | EN lines 13 and 201-207 | FR lines 13 and 256-266 | Richard Meier & Partners; Barely Levitzky Kassif Architects identified in the tall-building record | Pass |
| Height, floors and apartment count | EN lines 21-22 and 82-90 | FR lines 13, 21-22 and 100-112 | 154 metres; 147 apartments in architect-published data; 42/41/37 source conflict disclosed without averaging | Pass |
| Building use and materials | EN lines 11 and 82-86 | FR lines 11 and 100-106 | Residential tower on retail base; concrete, aluminium and curtain wall; no hotel/office/Shadal conflation | Pass |
| Development history | EN lines 203-215 | FR lines 258-270 | Berggruen Residential, Hagag and Cohen-brothers history; no claim that Hagag sells every current resale | Pass |
| Amenities and pool conflict | EN lines 106-112 and 356-370 | FR lines 136-150 and 415-429 | Amenities attributed; current access and unit rights not assumed; pool length withheld because sources differ | Pass |
| Parking, storage and wine-cellar rights | EN lines 104, 112 and 368-370 | FR lines 144-150 and 427-429 | Building-level language is not converted into a unit entitlement | Pass |
| White City, Red Line and beach relationship | EN lines 46-58 and 68-75 | FR lines 52-72 and 82-93 | Urban context retained; station facts retained; no invented walking time, beachfront claim or project-wide sea view | Pass |
| Menora Allenby planning context | EN lines 60-66 and 392-394 | FR lines 74-80 and 455-457 | 19 March 2025 decision, area between Yavne/Allenby/Yehuda Halevi, up to 45 floors subject to conditions; effect remains unit-specific | Pass |
| Dated price evidence | EN lines 143-152 | FR lines 187-198 | All six examples carry the same dates, areas, floors, NIS amounts and limitations | Pass |
| Asking price versus transaction | EN lines 147 and 334-338 | FR lines 191 and 383-385 | NIS 75 million remains a January 2026 asking price for one atypical duplex, not a project price or proven sale | Pass |
| Completion chronology | EN line 227 | FR lines 280-282 | 2010 construction start, 2016 project year, 2017 completion record and current occupied classification are kept as different source conventions | Pass |
| Title, tax and finance process | EN lines 166-193 and 211-215 | FR lines 208-244 and 288-304 | Input-based model only; current extract, official tax assumptions and lender-specific mortgage outcome | Pass |

### Price parity detail

The published examples agree exactly in substance:

1. January 2026 duplex asking price: NIS 75 million, about 430 m², one 50 m² balcony, two 30 m² balconies, storage, three parking spaces and reported 2016 purchase at NIS 80 million. EN line 147; FR line 191.
2. December 2024 reported transaction: 145 m², floor 30, NIS 14 million, about NIS 97,000 per m². EN line 148; FR line 192.
3. February 2024 reported transaction: 196 m², floor 7, NIS 9.5 million, about NIS 48,000 per m². EN line 149; FR line 193.
4. Reported 2018 transaction: 434 m², floor 38, NIS 45 million, about NIS 104,000 per m². EN line 150; FR line 194.
5. 2019 report: 540 m² duplex on floors 38-39, NIS 50 million, about NIS 92,000 per m² and about 40 m² of balconies. EN line 151; FR line 195.
6. 2013 construction-period report: 395 m² half-floor unit, NIS 21 million, about NIS 53,000 per m². EN line 152; FR line 196.

Neither article turns these examples into a current project range, current availability, an appraisal or a guaranteed price per square metre.

## Source-parity audit

Both source sections contain exactly 18 entries:

- English S01-S18: EN lines 410-427.
- French S01-S18: FR lines 469-486.
- Expected source sequence: `00-source-ledger.md` S01-S18.

The URL sequence is byte-for-byte identical in both articles and in the frozen ledger. The joined URL-sequence SHA-256 is the same for all three: `524ce4611768a0d22de1f5466a02a8509551ebd79a34e391a25b6893bf90e44e`.

No extra external source appears in either article before Sources. Localized source labels do not change source identity or order.

## French native-language and cultural review

### Natural buyer language

The French version uses the vocabulary a francophone buyer needs: `appartement à vendre`, `revente`, `pied-à-terre`, `achat à distance`, `procuration`, `extrait du registre foncier`, `taxe d'acquisition`, `prix demandé`, `transaction enregistrée`, `risque EUR/NIS`, `remise des clés` and `prise de possession`. The sequencing is French-buyer specific rather than translated from the English article:

- remote purchase and EUR/NIS planning are developed at FR lines 232-244 and 294-304;
- pied-à-terre operations are treated at FR lines 326-332;
- alyah and relocation are kept as a conditional branch, not an assumed identity or tax result, at FR lines 334-340;
- patrimonial and rental analysis is handled without a yield promise at FR lines 342-348;
- the remote buyer receives a document, inspection and funds-control workflow at FR lines 296-304 and 350-356.

### Israeli legal reality retained

The French body contains none of the prohibited or misleading one-to-one French-system terms: `VEFA`, `notaire`, `acte authentique`, `compromis de vente`, `syndic` or `copropriété`. It correctly names an independent Israeli lawyer, current registry evidence, a transaction-specific power of attorney, authentication requirements and Israeli purchase tax. It does not claim that a French translation overrides the controlling signed documents.

### AI-tell review

The body is project-specific. It repeatedly anchors buyer decisions to 36 Rothschild, Allenby, the 42/41/37 floor-count conflict, the 147-apartment architectural record, Menora Allenby, the dated Meier transactions and the operating-tower cost questions. It does not expose search-intent, SEO, keyword, AI-writing or production language. Paragraph and question patterns vary, and the French cultural material does not assign every francophone buyer the same motive.

Result: native-language and AI-tell review passes.

## Findings requiring attention

### F1. Shared city link uses a percent-encoded Hebrew public slug

Severity: release dependency outside the factual article copy.  
Affected lines:

- EN line 52: `https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/`
- FR line 58: the same destination.

Observed state on 2026-08-05:

- the existing percent-encoded destination returns HTTP 200;
- `/cities/tel-aviv-yafo/`, `/cities/tel-aviv/` and `/city/tel-aviv-yafo/` return HTTP 404.

Why it matters: the contextual links satisfy the frozen four-link and destination-parity gates, but the destination conflicts with the site's ASCII-only public URL governance. Replacing it now with a guessed ASCII path would create a broken link. The durable resolution is a real ASCII canonical city URL with an exact redirect from the old path, followed by a coordinated update across every language package. That platform action is outside this content-only review.

No other factual, structural, source, cultural, legal-equivalence or language issue was found.

## Final acceptance result

| Area | Result |
|---|---|
| French article against frozen content gates | Pass |
| EN-FR factual and uncertainty parity | Pass |
| Dated price parity | Pass |
| Address, status, developer and amenity parity | Pass |
| S01-S18 URL order and identity | Pass |
| Native French cultural intent | Pass |
| French legal-system equivalence guard | Pass |
| AI-tell and language-leak guard | Pass |
| Contextual internal-link count | Pass |
| Site-wide ASCII URL governance | Pending platform-level city URL migration; current live link remains 200 |

The French article is acceptable as a content artifact. The city-link migration should be tracked at platform level rather than solved by inventing a replacement inside this file.
