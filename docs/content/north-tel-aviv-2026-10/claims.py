# -*- coding: utf-8 -*-
"""HAD-460 Stage A: the claim graph for the language versions of the North Tel Aviv hub (/north-tel-aviv/, page 4866) and
Rova 4 (/north-tel-aviv/rova-4/, page 8218). Modelled on docs/research/2026-10-kikar-v7/claims.py. One fact = one claim_id.

    python docs/content/north-tel-aviv-2026-10/claims.py      -> claims.json

Every claim carries: the page it belongs to (hub / rova-4 / both), the statement (English, canonical), the numbers it allows in
an article (as written in the Hebrew source; the checker also accepts their locale forms), the date, the source key and how to
write it. Sources are named HERE only: the articles never name a source (the owner, 1.10.2026).
- Hub claims (H..) follow the Hebrew hub AFTER align-edits.json is applied; source keys: align-check.md section 3.
- Rova 4 claims (R4-..) follow the live Hebrew article; the number after "R4-" is the row id in
  docs/content/rova-4-2026-10/facts.md (R52 -> R4-52), whose source keys and retrieval times are listed there.
- G claims are conventions any page may use (room count, dunam, quarter notation).
Rules folded in: numbers and dates identical to the Hebrew, one to one; nothing added that the Hebrew does not say; asking
prices stay asking prices and deals stay deals; what is not published is written as not published.
"""
import io, json, os

C = []


def c(cid, page, topic, claim, nums=(), date="", src="", conflict="", write=""):
    C.append({"claim_id": cid, "page": page, "topic": topic, "claim": claim, "numbers": [str(n) for n in nums],
              "date": date, "source": src, "conflict": conflict, "write_as": write})


# ======================================================================= G: conventions (both pages)
c("G-01", "both", "convention", "The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; "
  "'2.5 rooms' has a half room.", nums=(2, 3, 4, 5, "2.5"), src="convention",
  write="Explain once for a foreign reader; never convert to bedrooms in a table.")
c("G-02", "both", "convention", "A dunam (the Israeli land unit) is 1,000 m2.", nums=(1, "1,000"), src="convention",
  write="Allowed once, to explain the unit. No other conversions (no sq ft, no acres, no hectares, no dollars or euros).")
c("G-03", "both", "convention", "Quarters: 'the first quarter of 2026' = January to March 2026 (Q1, 1-3.2026); "
  "'the fourth / last quarter' = Q4.", nums=(1, 3, 4, "1-3"), src="convention",
  write="'Q1 2026' or 'the first quarter of 2026'. Keep the year.")

# ======================================================================= H: the hub (after align-edits.json)
c("H-01", "hub", "sde-dov", "The Sde Dov quarter, on the site of the former airfield in the north-west of the city, is "
  "planned for about 16,000 apartments, with mixed uses, public buildings, parks, commerce, hotels and transport.",
  nums=("16,000",), date="municipality page (read 5.8.2026); survey 15.4.2026", src="TLVSD; NC2604",
  write="'about 16,000 apartments planned'. Never a delivery date for the quarter.")
c("H-02", "hub", "neve-avivim", "Neve Avivim: its first houses were built in the mid-1960s and most of the neighbourhood in "
  "the 1970s ('built in the 1960s and 1970s').", nums=(60, 70, 1960, 1970), src="HEWNA",
  write="'built in the 1960s and 1970s'.")
c("H-03", "hub", "neve-avivim", "Urban renewal example in Neve Avivim: on Yehuda HaNasi Street a plan approved in 2023 "
  "replaces five buildings with 80 apartments by three buildings of up to 14 floors with 195 apartments.",
  nums=(2023, 5, 80, 3, 14, 195), date="2.8.2023", src="NC2308",
  conflict="The old page said 'about 40 TAMA 38 projects in Neve Avivim': that count belongs to Neot Afeka B (NC2501). "
  "Never write it for Neve Avivim.", write="One example, dated 2023.")
c("H-04", "hub", "einstein", "Hagag Group's projects on Einstein Street (Ramat Aviv), per the company's January 2026 figures: "
  "six residential buildings with 515 apartments, a shopping centre of about 11,400 m2, a public building of about 3,950 m2 "
  "and an underground car park of 957 spaces; total value estimated at about ₪4 billion. Architect: Moshe Tzur.",
  nums=(2026, "1.2026", 6, 515, "11,400", "3,950", 957, 4), date="20.1.2026", src="NC2601; NC2410 (older figures)",
  conflict="An October 2024 report gave 'a 30-floor and a 28-floor tower, 4 buildings of 14 floors, 13,500 m2 of commerce'; "
  "a March 2024 report gave other floor counts. Use only the January 2026 figures.",
  write="515 is the WHOLE complex, never EINSTEIN TOWER alone.")
c("H-05", "hub", "einstein", "EINSTEIN TOWER, one of the projects in Hagag's Einstein complex: 215 apartments in a 28-floor "
  "tower and two 13-floor buildings above a commercial base; the company estimates completion in the third quarter of 2030.",
  nums=(215, 28, 2, 13, 3, 2030), date="annual report 31.12.2025; permit 9.7.2026", src="DOS (S001, S002, IVS008)",
  write="Completion is the company's estimate, not a contractual date.")
c("H-06", "hub", "einstein", "Ashdar Einstein, on Einstein Street: marketing opened in 2021; three 8-floor buildings with "
  "about 45 apartments.", nums=(2021, 3, 8, 45), date="8.7.2021", src="ICE2107")
c("H-07", "hub", "prices", "Official median deal prices (Tax Authority deals), 4 rooms, first quarter of 2026: Neve Avivim "
  "and surroundings ₪5,370,100; Bavli ₪6,549,400; Shikun Lamed (official name 'Tochnit Lamed') ₪8,425,800; the Old North, "
  "northern part ₪6,542,100; all of Tel Aviv-Yafo ₪5,229,800.",
  nums=("5,370,100", "6,549,400", "8,425,800", "6,542,100", "5,229,800", 4, 1, 2026), date="1-3.2026 (files of 20.8.2026)",
  src="GOVN", write="Full numbers, never rounded to millions. A median is a whole-apartment price, not per m2.")
c("H-08", "hub", "prices", "Prices per m2 in mid-2026: recent deals in Ramat Aviv averaged around ₪55,000 (June 2026); "
  "Ramat Aviv Gimel about ₪51,000 to ₪53,000 on average (August 2026); most new projects in Sde Dov around ₪70,000 (2026).",
  nums=("55,000", "51,000", "53,000", "70,000", 2026, "6.2026", "8.2026"), date="6.6.2026; 2.8.2026; 21.5-6.6.2026",
  src="ICE0606; BZ2608; ICE2105", conflict="The old page's '60,000-95,000 for new construction in Ramat Aviv Gimel' had no "
  "source: never use it.")
c("H-09", "hub", "names", "Names that carry numbers: TAMA 38 (the national plan for strengthening buildings, תמ״א 38); "
  "Rova 3 = the Old North (west of Ibn Gabirol); Rova 4 = the New North and Kikar HaMedina.", nums=(38, 3, 4),
  src="Hebrew source; rova-4 facts R1, R3, R11", write="'TAMA 38' with a short gloss once.")
c("H-10", "hub", "page", "The page was updated in October 2026.", nums=("10.2026", 2026), src="THIS",
  write="Only if a date line is written; the disclaimer itself is added by the site.")
c("H-11", "hub", "transport", "The Green Line of the light rail is planned along Ibn Gabirol, with an Einstein station in the "
  "north (future).", src="DOS (S009: Einstein and Levi Eshkol listed as future stations)",
  write="Future tense; no opening date in the hub.")

# ======================================================================= R4: Rova 4 (live article = article-he.md)
c("R4-01", "rova-4", "where", "Rova 4 = the New North (הצפון החדש), Tel Aviv's 4th quarter: between Ibn Gabirol Street (west) "
  "and the Ayalon highway (east), the Yarkon stream (north) and Shaul HaMelech Boulevard (south); Kikar HaMedina at its centre; "
  "Bavli, Givat Amal B and Park Tzameret inside it.", nums=(4,), src="facts R1, R5, R93")
c("R4-02", "rova-4", "where", "Tel Aviv-Yafo is divided into nine quarters numbered north to south; Rova 4 is one of the four "
  "quarters of the city centre; Ibn Gabirol separates it from Rova 3 (west) and Shaul HaMelech from Rova 6, the business "
  "district (south). The quarters north of the Yarkon are 1 and 2; the Old North is Rova 3. The municipality calls Rova 4 "
  "'the New North'.", nums=(9, 4, 3, 6, 1, 2), src="facts R2, R3")
c("R4-04", "rova-4", "where", "About 51,500 people lived in Rova 4 in 2022 (municipal data).", nums=("51,500", 2022),
  date="2022", src="facts R4", conflict="Other counts 50,829 / 42,746: never used.")
c("R4-06", "rova-4", "where", "Rova 4 was built mostly after 1948 and until the 1980s, so its streets are wider and its plots "
  "about 50% larger than in the Old North; residential towers since the 1980s; planning designates the eastern strip by the "
  "Ayalon for high towers.", nums=(1948, 80, 1980, 50), src="facts R9, R10")
c("R4-07", "rova-4", "plan", "The plan area is about 2,825 dunam; the plan allows about 5,100 additional apartments, assuming "
  "only about half (50%) of the buildings are realised.", nums=("2,825", "5,100", 50), date="4.6.2018", src="facts R19")
c("R4-08", "rova-4", "where", "Inside Rova 4: Kikar HaMedina, the Ichilov medical centre, the Tel Aviv Museum compound (the "
  "Performing Arts Center, Beit Ariela, the courthouse), Tel Aviv Center railway station with the 2000 terminal (מסוף 2000). "
  "Habima and Rabin Square are in Rova 3, not in Rova 4.", nums=(2000, 3, 4), src="facts R6, R7",
  write="'the 2000 Terminal' is a name.")
c("R4-09", "rova-4", "plan", "New buildings by street type (floors include the ground floor, plus partial roof floors): main "
  "streets Pinkas, Namir Road, Jabotinsky, Weizmann: 8 + 1; Arlozorov: 7 + 1 under the quarter plan, while the Arlozorov plan "
  "allows up to 10 floors east of Ibn Gabirol; a street that is not a main street: 6 + 2; the UNESCO declared area (David "
  "HaMelech, Dubnov, Shaul HaMelech): 6 + 1; the low-rise areas: 4 + 1.", nums=(8, 1, 7, 10, 6, 2, 4),
  src="facts R23, R29")
c("R4-10", "rova-4", "plan", "Planning designates the eastern strip for towers of about 40 floors and more (Park Tzameret).",
  nums=(40,), src="facts R10")
c("R4-11", "rova-4", "neighbourhoods", "In the official deal data the area between Ibn Gabirol and Namir Road is three "
  "neighbourhoods all called the New North: the northern part, the Kikar HaMedina area and the southern part; east of Namir "
  "to the Ayalon: Bavli, Givat Amal B, Park Tzameret.", nums=(3,), src="facts R13, R5")
c("R4-13", "rova-4", "plan", "Rights are volumetric: coverage between building lines times the number of floors, plus the "
  "ground floor and setback roof floors. A plot within 25 m of a main street counts as facing it; on a plot of 750 m2 or more "
  "coverage may not exceed 50%; the number of apartments derives from a coefficient of 90 m2 per apartment. The plan covers "
  "ten blocks (gush); check by block and parcel.", nums=(25, 750, 50, 90, 10), src="facts R23, R24")
c("R4-14", "rova-4", "renewal", "Around the square an old 4-floor building typically becomes a boutique building of 8 or 9 "
  "floors (7 to 9 in the renewal section) with almost twice the apartments.", nums=(4, 8, 9, 7, 2), date="5.10.2026",
  src="facts R40")
c("R4-15", "rova-4", "plan", "Additions to an existing building: a building of up to 4 floors on a main street (Pinkas, "
  "Arlozorov, Namir, Jabotinsky, Shaul HaMelech): up to 230% of the roof area, up to 3 more floors and closing the pilotis "
  "floor; other streets: up to 165% and 2 floors and closing the pilotis; a ground-attached condominium of up to 2 floors: up "
  "to 165% and 2 floors; 2 floors over pilotis in the housing-estate area: up to 40 m2 per apartment and up to 65% of the roof "
  "area.", nums=(4, 230, 3, 165, 2, 40, 65), date="4.6.2018", src="facts R22")
c("R4-16", "rova-4", "plan", "Betterment levy: additions under TAMA 38 were exempt; the plan's rights can be levied by the "
  "local committee at half (50%) of the increase in value, valued as of the approval date 23.5.2018; professionals estimated "
  "hundreds of thousands of shekels per apartment; an appeal within 45 days of receiving the assessment; buyers should agree "
  "in the contract who pays.", nums=(38, 50, "23.5.2018", 45), src="facts R25",
  write="'hundreds of thousands of shekels' stays in words.")
c("R4-17", "rova-4", "plan", "Plan TA/3729/A (תא/3729/א), a district committee plan for the residential buildings of the "
  "quarter (without plots on Ibn Gabirol): deposit published 14.11.2012, approved by the district committee 23.5.2018, "
  "published for validity 30.5.2018 ('in force since May 2018'). Before it each building was checked under TAMA 38 and old "
  "plans; it replaced older plans on rights, balconies, roof apartments and roof exits.",
  nums=(3729, "14.11.2012", "23.5.2018", "30.5.2018", 2012, 2018, "5.2018", 38), src="facts R16-R18, R20, R21",
  conflict="'28.5.2018' in one source: never used.")
c("R4-18", "rova-4", "plan", "In 2019 the rear building line in the housing-estate strip between Bnei Dan and Yehuda "
  "HaMaccabi was amended to 4.5 m instead of 5 m.", nums=(2019, "4.5", 5), src="facts R26")
c("R4-19", "rova-4", "plan", "The Arlozorov plan (TA/4474) came into force in 2024: a mixed-use street with commerce and "
  "employment on the ground and mezzanine floors, up to 10 floors in all east of Ibn Gabirol, about 600 more apartments along "
  "the street; the Purple Line is planned along it.", nums=(4474, 2024, 10, 600), src="facts R28, R29")
c("R4-20", "rova-4", "plan", "On 4.12.2024 the local committee decided to promote a plan adding commerce on the ground floors "
  "of Yehuda HaMaccabi, Pinkas, Jabotinsky, Weizmann and Shaul HaMelech (five streets); per the municipality the quarter lacks "
  "about 20,000 m2 of commerce against about 18,000 additional apartments from the quarter plan and other plans; the same "
  "decision recommended no building permits for three years on residential plots on Jabotinsky, Pinkas, Yehuda HaMaccabi and "
  "Weizmann (four streets), with exceptions.", nums=("4.12.2024", 2024, 5, "20,000", "18,000", 3, 4), src="facts R30",
  write="Tell buyers to check the current status of the restriction.")
c("R4-21", "rova-4", "plan", "On 18.5.2026 a further amendment, TA/3729B (תא/3729ב), was published for validity; it changes "
  "the rules for the low-rise areas.", nums=("18.5.2026", 2026, 3729), src="facts R27")
c("R4-22", "rova-4", "buying", "Before choosing an apartment ask four questions (the street and what the plan allows; the "
  "permit restriction on main streets; the renewal agreement's stage, the difference between signature, committee decision "
  "and permit, three different stages; who pays the betterment levy).", nums=(4, 3), src="editorial (facts R25, R30)")
c("R4-52", "rova-4", "prices", "Official median deal price, first quarter of 2026: the New North, northern part: 3 rooms "
  "₪4,434,900; 4 rooms ₪6,042,800; 5 rooms ₪7,704,000.", nums=("4,434,900", "6,042,800", "7,704,000", 2026, 3, 4, 5, 1),
  date="1-3.2026", src="facts R52 (GOV 65209989)", write="Full numbers. A median is a whole-apartment price.")
c("R4-53", "rova-4", "prices", "Median, first quarter of 2026: the New North, Kikar HaMedina area: 3 rooms ₪4,943,500; 4 rooms "
  "₪6,835,800; 5 rooms ₪8,455,800.", nums=("4,943,500", "6,835,800", "8,455,800", 2026, 3, 4, 5, 1), date="1-3.2026",
  src="facts R53 (GOV 65209991)")
c("R4-54", "rova-4", "prices", "Median, first quarter of 2026: the New North, southern part: 3 rooms ₪4,562,000; 4 rooms "
  "₪6,910,000; 5 rooms: no median published.", nums=("4,562,000", "6,910,000", 2026, 3, 4, 5, 1), date="1-3.2026",
  src="facts R54 (GOV 65209993)", write="'not published' for the empty cell.")
c("R4-55", "rova-4", "prices", "Median, first quarter of 2026, all Tel Aviv-Yafo: 3 rooms ₪4,225,800; 4 rooms ₪5,229,800; "
  "5 rooms ₪7,497,700.", nums=("4,225,800", "5,229,800", "7,497,700", 2026, 3, 4, 5, 1), date="1-3.2026",
  src="facts R55 (GOV 5000)")
c("R4-56", "rova-4", "prices", "Gap above the city, Q1 2026 (computed): 4 rooms: Kikar area +30.7%, southern part +32.1%, "
  "northern part +15.5%; 3 rooms: from +4.9% (northern part) to +17.0% (Kikar area).",
  nums=("30.7", "32.1", "15.5", "4.9", "17.0", 4, 3), src="facts R56 (computed)")
c("R4-57", "rova-4", "prices", "4-room median in the first quarter of each year (northern part / Kikar area / southern part / "
  "Tel Aviv-Yafo): 2023: 6,281,300 / 6,573,800 / 7,020,100 / 4,638,500; 2024: 6,001,300 / not published / 6,293,100 / "
  "4,697,600; 2025: 5,681,700 / 6,698,300 / 6,777,900 / 4,723,800; 2026: 6,042,800 / 6,835,800 / 6,910,000 / 5,229,800.",
  nums=("6,281,300", "6,573,800", "7,020,100", "4,638,500", "6,001,300", "6,293,100", "4,697,600", "5,681,700", "6,698,300",
        "6,777,900", "4,723,800", "6,042,800", "6,835,800", "6,910,000", "5,229,800", 2023, 2024, 2025, 2026, 4, 1),
  src="facts R57")
c("R4-58", "rova-4", "prices", "3-room median in the first quarter of each year (northern / Kikar / southern / Tel Aviv-Yafo): "
  "2023: 4,434,300 / 5,100,300 / 4,759,300 / 3,293,800; 2024: 4,310,100 / 5,120,300 / 5,192,200 / 3,672,700; 2025: "
  "4,993,800 / not published / 4,878,400 / 3,704,300; 2026: 4,434,900 / 4,943,500 / 4,562,000 / 4,225,800.",
  nums=("4,434,300", "5,100,300", "4,759,300", "3,293,800", "4,310,100", "5,120,300", "5,192,200", "3,672,700", "4,993,800",
        "4,878,400", "3,704,300", "4,434,900", "4,943,500", "4,562,000", "4,225,800", 2023, 2024, 2025, 2026, 3, 1),
  src="facts R58")
c("R4-59", "rova-4", "prices", "Over these three years (Q1 2023 to Q1 2026) the 4-room median rose 12.7% in Tel Aviv, while in "
  "the three New North neighbourhoods it moved between -3.8% and +4.0%; for 3 rooms: +28.3% in the city, -3.1% in the Kikar "
  "area. One quarter's median depends on what sold in it: read the trend.",
  nums=("12.7", "3.8", "4.0", "28.3", "3.1", 3, 4, 2023, 2026, 1), src="facts R59 (computed)")
c("R4-64", "rova-4", "prices", "Professionals in the quarter estimate prices at 10% to 15% below the peak; appraisers about "
  "11%; premium apartments were barely hit.", nums=(10, 15, 11), date="5.10.2026", src="facts R64")
c("R4-67", "rova-4", "prices", "The official house price index published on 15.9.2026: Tel Aviv district -0.9% over the year.",
  nums=("15.9.2026", "0.9"), src="facts R67")
c("R4-60", "rova-4", "prices", "New buildings around the square: ₪63,000 to ₪68,000 per m2 in recently marketed projects "
  "(marketing price, 10.2026), after ₪70,000 to ₪75,000 per m2 at the peak.",
  nums=("63,000", "68,000", "70,000", "75,000", "10.2026"), date="5.10.2026", src="facts R60",
  write="These are marketing prices, not deals.")
c("R4-61", "rova-4", "prices", "Most apartments sold in the new projects around the square in the past year: ₪63,000 to "
  "₪66,000 per m2 (deals, 4.2026).", nums=("63,000", "66,000", "4.2026"), src="facts R61")
c("R4-62", "rova-4", "prices", "2-to-4-room deals published in 2026 (the table below): ₪59,200 to ₪76,400 per m2.",
  nums=(2, 4, "59,200", "76,400", 2026), src="derived from facts R72-R77")
c("R4-63", "rova-4", "prices", "Penthouses, garden apartments and large apartments: ₪80,000 to ₪110,000 per m2 (deals, "
  "10.2026); this segment barely fell.", nums=("80,000", "110,000", "10.2026"), src="facts R63, R64")
c("R4-65", "rova-4", "prices", "2-room apartments of 40 to 54 m2: ₪2,500,000 to ₪3,700,000 per apartment (deals, 4.2026).",
  nums=(2, 40, 54, "2,500,000", "3,700,000", "2.5", "3.7", "4.2026"), src="facts R62")
c("R4-87", "rova-4", "prices", "In a penthouse or garden apartment the price per m2 is usually on the built area only; a large "
  "balcony or roof counts at a much lower rate in a valuation, so a deal of about ₪93,600 per m2 for a penthouse with a 156 m2 "
  "roof is not the price of an ordinary apartment in the same building. On the ground floor, David Yellin 9 and Mosinzon 17 "
  "closed at about ₪76,400 and ₪70,300 per m2.", nums=("93,600", "156", 9, 17, "76,400", "70,300"), src="facts R87, R68, R72, R73")
c("R4-68", "rova-4", "deals", "Deal: Henkin 3, penthouse, 5 rooms, 188 m2 + 26 m2 balcony + 156 m2 roof, floor 7, "
  "₪17,600,000 (about ₪93,600 per m2), 3.2026.", nums=(3, 5, 188, 26, 156, 7, "17,600,000", "93,600", "3.2026", "17.6"),
  src="facts R68")
c("R4-69", "rova-4", "deals", "Deal: Jabotinsky 133, penthouse with a pool, about 280 m2 + roof about 113 m2 + balcony about "
  "28 m2, floor 8, ₪22,000,000 (about ₪78,600 per m2 of interior), published 12.2025.",
  nums=(133, 280, 113, 28, 8, "22,000,000", "78,600", "12.2025", 22), src="facts R69")
c("R4-70", "rova-4", "deals", "Deal: Remez 27, two penthouses, 277 m2 together, floor not published, ₪22,850,000 (about "
  "₪82,500 per m2), published 10.2026.", nums=(27, 2, 277, "22,850,000", "82,500", "10.2026", "22.85"), src="facts R70")
c("R4-71", "rova-4", "deals", "Deal: Jabotinsky 105, garden apartment, 5 rooms, 156 m2 + garden about 170 m2, ground floor, "
  "about ₪11,000,000 (about ₪70,500 per built m2), 8.2026 per the company.",
  nums=(105, 5, 156, 170, "11,000,000", "70,500", "8.2026", 11), src="facts R71")
c("R4-72", "rova-4", "deals", "Deal: David Yellin 9, 4 rooms, 110 m2, ground floor, ₪8,400,000 (about ₪76,400 per m2), "
  "published 4.2026.", nums=(9, 4, 110, "8,400,000", "76,400", "4.2026", "8.4"), src="facts R72")
c("R4-73", "rova-4", "deals", "Deal: Mosinzon 17, 4 rooms, 102 m2, ground floor, ₪7,170,000 (about ₪70,300 per m2), "
  "published 4.2026.", nums=(17, 4, 102, "7,170,000", "70,300", "4.2026", "7.17"), src="facts R73")
c("R4-74", "rova-4", "deals", "Deal: Shlomzion HaMalka, 4 rooms, 103 m2, floor 1 of 7, ₪6,100,000 (about ₪59,200 per m2), "
  "5.2026.", nums=(4, 103, 1, 7, "6,100,000", "59,200", "5.2026", "6.1"), src="facts R74")
c("R4-75", "rova-4", "deals", "Deal: Epstein 7, 3 rooms, 70 m2, floor 6, ₪4,880,000 (about ₪69,700 per m2), published "
  "4.2026.", nums=(7, 3, 70, 6, "4,880,000", "69,700", "4.2026", "4.88"), src="facts R75")
c("R4-76", "rova-4", "deals", "Deal: Weizmann 50, 3 rooms, 75 m2, floor 2, ₪4,750,000 (about ₪63,300 per m2), published "
  "4.2026.", nums=(50, 3, 75, 2, "4,750,000", "63,300", "4.2026", "4.75"), src="facts R76")
c("R4-77", "rova-4", "deals", "Deal: Ben Saruk 21, 2 rooms, 46 m2, ground floor, ₪3,180,000 (about ₪69,100 per m2), "
  "published 4.2026.", nums=(21, 2, 46, "3,180,000", "69,100", "4.2026", "3.18"), src="facts R77",
  write="Where the deal month was not published the publication month is shown.")
c("R4-78", "rova-4", "asking", "Asking: He Be'Iyar 18, 5 rooms, new from the developer, 161 m2, floor 12, ₪14,500,000 (about "
  "₪90,000 per m2), 10.2026.", nums=(18, 5, 161, 12, "14,500,000", "90,000", "10.2026", "14.5"), src="facts R78")
c("R4-79", "rova-4", "asking", "Asking: He Be'Iyar 2, 4 rooms, new from the developer, 142 m2, floor 23, ₪11,250,000 (about "
  "₪79,200 per m2), 10.2026.", nums=(2, 4, 142, 23, "11,250,000", "79,200", "10.2026", "11.25"), src="facts R79")
c("R4-81", "rova-4", "asking", "Asking: Moshe Sharett Street, 4 rooms, 125 m2, floor 3, ₪6,500,000 after a ₪100,000 cut "
  "(₪52,000 per m2), 10.2026.", nums=(4, 125, 3, "6,500,000", "100,000", "52,000", "10.2026", "6.5"), src="facts R81")
c("R4-80", "rova-4", "asking", "Asking: He Be'Iyar 16, 4 rooms in an old building, 107 m2, floor 4, ₪4,590,000 (about ₪42,900 "
  "per m2), 10.2026. On the same street a new high-floor apartment asks about ₪90,000 per m2.",
  nums=(16, 4, 107, "4,590,000", "42,900", "10.2026", "90,000", "4.59"), src="facts R80, R78")
c("R4-82", "rova-4", "asking", "Asking: David Yellin 10, 2.5 rooms facing the park, 84 m2, floor 1, ₪4,400,000 after a "
  "₪90,000 cut (about ₪52,400 per m2), 10.2026.", nums=(10, "2.5", 84, 1, "4,400,000", "90,000", "52,400", "10.2026", "4.4"),
  src="facts R82")
c("R4-65b", "rova-4", "asking", "In expensive apartments the closing price is usually 5% to 10% below the asking price.",
  nums=(5, 10), date="5.10.2026", src="facts R65")
c("R4-66", "rova-4", "asking", "About 500 apartments are offered for sale in the neighbourhood; developers offer 10% at "
  "signing and the rest toward occupancy, and an exemption from index linkage; there is room to negotiate.",
  nums=(500, 10), date="5.10.2026", src="facts R66")
c("R4-84", "rova-4", "costs", "Purchase tax example on the Q1 2026 4-room median of the Kikar area, ₪6,835,800: about "
  "₪260,750 for a single (only) apartment; about ₪562,479 for an additional apartment (brackets of 16.1.2025, frozen to "
  "15.1.2028).", nums=("6,835,800", "260,750", "562,479", 4, 1, 2026), src="facts R84, R83")
c("R4-34", "rova-4", "kikar", "Kikar HaMedina spans about 78 dunam; at its centre three residential towers are being built, "
  "two of 40 floors and one of 37, with 453 apartments; alongside them a public park of about 40 dunam and a school of 18 "
  "classes plus 6 special-education classes. The ring street, He Be'Iyar, is the quarter's main shopping street.",
  nums=(78, 3, 2, 40, 37, 453, 18, 6), date="5.10.2026; 25.9.2025", src="facts R34, R35, R37",
  write="The towers have no developer: never call their owners 'the developer'.")
c("R4-36", "rova-4", "kikar", "Per published estimates, the towers' occupancy permit is expected at the end of 2026 and "
  "handover will be gradual in the first quarter of 2027; many owners are expected to wait half a year to two years after "
  "occupancy before selling, so supply from the towers will come gradually.",
  nums=(2026, 2027, 1, 2, 6, "0.5"), date="5.10.2026", src="facts R36, R38",
  write="'half a year' may be written '6 months'. Estimates, never a promise.")
c("R4-39", "rova-4", "renewal", "In 2022 almost 40% of the apartments whose construction began in Tel Aviv-Yafo that year were "
  "in Rova 4, and so was 33% of the residential construction-start area.", nums=(2022, 40, 33), src="facts R39")
c("R4-41", "rova-4", "renewal", "In the published projects the old residents receive an apartment larger by about 18 to 22 m2, "
  "in some also a balcony, a safe room (mamad), storage and parking.", nums=(18, 22), src="facts R41-R43")
c("R4-44", "rova-4", "renewal", "Be'eri 36 to 56 (even side): 11 buildings, about 190 apartments, up to about 500 apartments "
  "by the company's estimate; Adam Shuster won the tenants' tender, 3.2026. The Be'eri compound is 13 dunam between Weizmann "
  "and Henrietta Szold, north of Ichilov: the largest renewal project in the quarter.",
  nums=(36, 56, 11, 190, 500, "3.2026", 13), src="facts R44, R90")
c("R4-45", "rova-4", "renewal", "Jabotinsky 135 to 137: 32 apartments -> 9 floors, 68 apartments; Africa Renewal and Bayit "
  "VeGag; execution contract signed, 8.2024.", nums=(135, 137, 32, 9, 68, "8.2024"), src="facts R45")
c("R4-43", "rova-4", "renewal", "Jabotinsky 152: 4 floors, 20 apartments -> 8 floors, 38 apartments; Bayit VeGag; completion "
  "expected in the last quarter of 2028.", nums=(152, 4, 20, 8, 38, 2028), src="facts R43")
c("R4-46", "rova-4", "renewal", "Jabotinsky 133: 16 apartments -> 9 floors, 33 apartments; Bayit VeGag; the old building was "
  "demolished, 11.2025.", nums=(133, 16, 9, 33, "11.2025"), src="facts R46")
c("R4-50", "rova-4", "renewal", "Zichron Yaakov 16: 3 floors on pillars, 12 apartments -> 7 floors, 26 apartments; Levinstein "
  "Group; demolition began 24.11.2024; occupancy expected in the second half of 2028.",
  nums=(16, 3, 12, 7, 26, "24.11.2024", 2028, 2), src="facts R50")
c("R4-47", "rova-4", "renewal", "Remez 44: 7 floors, 25 apartments; Anshei HaIr; building permit 9.12.2025; works expected to "
  "start 18 to 24 months after the permit. Remez 22, 25 and 42: 32, 26 and 20 apartments (committee approval; residents "
  "moved out; permit request).", nums=(44, 7, 25, "9.12.2025", 18, 24, 22, 42, 32, 26, 20), src="facts R47, R91")
c("R4-42", "rova-4", "renewal", "Remez 27: 4 floors, 14 apartments -> 9 floors, 24 apartments; demolished 2.2026. Zlotzisti 4: "
  "4 floors, 12 apartments -> 8 floors, 22 apartments; demolished 2.2026. Developers not published.",
  nums=(27, 4, 14, 9, 24, "2.2026", 12, 8, 22), src="facts R41, R42")
c("R4-49", "rova-4", "renewal", "Sharett 30: 4 floors, 11 apartments -> 8 floors, 24 apartments; Lisin 27: 4 floors, 12 "
  "apartments -> 7 floors, 21 apartments; both Yaaz Development, building permits 7.2026. Henkin 3: Noga, under construction, "
  "the penthouse sold in 3.2026.", nums=(30, 4, 11, 8, 24, 27, 12, 7, 21, "7.2026", 3, "3.2026"), src="facts R48, R49, R51")
c("R4-40", "rova-4", "renewal", "Many other developers work in the quarter (Rothstein, Carasso, Netanel Group, Rogovin, Yoshpe, "
  "Ram-Mograbi-Arditi). Concentrated construction gives buyers choice and is one reason new-build prices per m2 fell from the "
  "peak. An apartment in an old building with an approved project is usually priced on its future potential.",
  src="facts R40, R88, R89")
c("R4-31", "rova-4", "transport", "The Red Line has run since August 2023, with an Arlozorov station by Tel Aviv Center "
  "station; the Purple Line is planned along Arlozorov, to Ichilov, ending at Tel Aviv Center, opening planned for June 2028; "
  "the Green Line is planned in a tunnel under Ibn Gabirol, on the quarter's western edge, full operation planned for 2030.",
  nums=(2023, "8.2023", 2028, "6.2028", 2030), src="facts R31-R33",
  write="Separate a running line from a planned one.")
c("R4-11b", "rova-4", "rova-3", "Rova 3 is the Old North: from the sea to Ibn Gabirol and from the Yarkon to Bograshov, Ben "
  "Zion Boulevard and Marmorek; built mainly in the 1930s and 1940s under the Geddes plan; most of the White City (UNESCO) is "
  "there; its quarter plan (approved early 2018) allows about 8,000 additional apartments, with preservation limits.",
  nums=(3, 30, 40, 1930, 1940, "8,000", 2018), src="facts R11, R12, R94")
c("R4-93", "rova-4", "fit", "Works around the square: on many streets several building sites run at once, some expected to "
  "last until 2028.", nums=(2028,), src="facts R43, R50 (2028 completions)")

CLAIMS = C
IDS = [x["claim_id"] for x in C]
assert len(IDS) == len(set(IDS)), "duplicate claim_id"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    io.open(os.path.join(here, "claims.json"), "w", encoding="utf-8").write(json.dumps(C, ensure_ascii=False, indent=1) + "\n")
    print(len(C), "claims ->", os.path.join(here, "claims.json"),
          {p: sum(1 for x in C if x["page"] == p) for p in ("hub", "rova-4", "both")})
