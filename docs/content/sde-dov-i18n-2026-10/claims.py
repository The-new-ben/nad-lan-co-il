# -*- coding: utf-8 -*-
"""HAD-439 Stage A: the claim graph for the language versions of the Sde Dov hub (/sde-dov/, page 4730) and the Sde Dov
prices page (/sde-dov/prices/, page 4758). Modelled on docs/content/north-tel-aviv-2026-10/claims.py. One fact = one claim_id.

    python docs/content/sde-dov-i18n-2026-10/claims.py      -> claims.json

Every claim carries: the page it belongs to (sde-dov-hub / sde-dov-prices / both), the statement (English, canonical), the
numbers it allows in an article (as written in the Hebrew source, plus the full form of every "X million" so both forms
pass; the checker also accepts their locale forms), the date, the source key and how to write it. Sources are named HERE
only: the articles never name a source (the owner, 1.10.2026).
- Hub claims (SDH-..) follow the Hebrew hub AFTER align-edits.json is applied; source keys: align-check.md section 3.
- Prices claims (SDP-..) follow the live Hebrew prices page (aligned on 7.10.2026 by docs/content/sde-dov-prices-2026-10/);
  source keys: scripts/project-stage/price_guide/sde-dov-prices.json "sources" and that folder's align-check.md section 3.
- SD-.. claims are facts both pages state; G-.. are conventions any page may use.
Rules folded in: numbers and dates identical to the Hebrew, one to one; nothing added that the Hebrew does not say; deals
stay deals, price lists stay price lists, estimates stay estimates; what is not published is written as not published.
"""
import io, json, os

C = []


def c(cid, page, topic, claim, nums=(), date="", src="", conflict="", write=""):
    C.append({"claim_id": cid, "page": page, "topic": topic, "claim": claim, "numbers": [str(n) for n in nums],
              "date": date, "source": src, "conflict": conflict, "write_as": write})


# ======================================================================= G: conventions (both pages)
c("G-01", "both", "convention", "The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; "
  "a '1-room' unit is a studio.", nums=(1, 2, 3, 4, 5), src="convention",
  write="Explain once for a foreign reader; never convert to bedrooms in a table.")
c("G-02", "both", "convention", "A dunam (the Israeli land unit) is 1,000 m2.", nums=(1, "1,000"), src="convention",
  write="Allowed once, to explain the unit. No other conversions (no sq ft, no acres, no hectares, no dollars or euros).")
c("G-03", "both", "convention", "Quarters: 'the first quarter of 2026' = January to March 2026 (Q1, 1-3.2026).",
  nums=(1, 3, "1-3"), src="convention", write="'Q1 2026' or 'the first quarter of 2026'. Keep the year.")

# ======================================================================= SD: facts both pages state
c("SD-01", "both", "plan", "The Sde Dov quarter (rova), on the site of the former airfield in north-west Tel Aviv-Yafo, is "
  "planned for about 16,000 apartments ('16 thousand') in three compounds: Eshkol (south-east), the Centre and the North.",
  nums=("16,000", 16, 3), date="plan approved 2020; municipal page read 7.10.2026", src="TLVSD; NC2003",
  write="'about 16,000 apartments planned'. Never a delivery date for the whole quarter.")
c("SD-02", "both", "prices", "A survey of the developers' annual reports published in April 2026: about 1,280 apartments sold "
  "in the quarter so far; their average price about ₪83,000 per m2; a 4-room apartment sold for about ₪9.45 million on "
  "average.", nums=("1,280", "83,000", "9.45", "9,450,000", 4, 2026, "4.2026"), date="15.4.2026 (published 4.2026)",
  src="NC2604; ICE1904", conflict="An older page figure 'about 81,000' and an average 'about 7 million per deal' have no "
  "source: never use them.", write="'about ₪83,000 per m2' (an average of sold units, not an asking price).")
c("SD-03", "both", "prices", "In 2026 most projects in the quarter sell at about ₪70,000 per m2.",
  nums=("70,000", 2026, "5.2026", "6.2026"), date="21.5.2026; 6.6.2026", src="ICE2105; ICE0606")
c("SD-04", "both", "prices", "Per the developers' 2025 reports, the sales averages of the projects in the Eshkol compound "
  "ranged from about ₪63,400 to about ₪82,600 per m2, VAT included.", nums=("63,400", "82,600", 2025), date="2025 reports",
  src="NC2604; ICE1904")
c("SD-05", "both", "deals", "The largest deal published in the quarter: an apartment of about 390 m2 with a balcony of about "
  "200 m2 on floor 38 of a tower in the Central compound, sold in December 2025 for more than ₪42 million.",
  nums=(390, 200, 38, 42, "42,000,000", 2025, "12.2025"), date="18.12.2025; 13.4.2026", src="BZ2512; NC2604F",
  conflict="'43.75 million for 508 m2' had no source: never use it.", write="'more than ₪42 million'.")

# ======================================================================= SDH: the hub (after align-edits.json)
c("SDH-01", "sde-dov-hub", "history", "Sde Dov (Dov Hoz airport) was inaugurated on 23 September 1938, with the Tel Aviv - "
  "Haifa - Beirut air line; it closed on 1 July 2019 and its evacuation was completed early in 2020.",
  nums=(23, 1938, "23.9.1938", 1, 2019, "1.7.2019", 2020), src="HEWSD",
  write="The city is Tel Aviv; the line name keeps the three cities.")
c("SDH-02", "sde-dov-hub", "land", "The quarter covers about 1,300 dunam along the sea in north Tel Aviv; its coastal front "
  "(the coastal park) is about 2 km long.", nums=("1,300", 2), date="12.3.2020; GIS read 7.10.2026; 10.2.2025",
  src="TLVSD; NC2003; GIS528 (1,304,428 m2); NC2502P",
  conflict="'1,500 dunam' (also 1,490 / 1,600 in some press and marketing) has no official basis: never use it.",
  write="'about 1,300 dunam'. 'about 1.3 km2' is NOT allowed (a new number).")
c("SDH-03", "sde-dov-hub", "land", "Boundaries: the Tzukei Aviv neighbourhood and Propes Street (north); Neve Yam, Program L "
  "(Tochnit Lamed) and Levi Eshkol Street (east); Kochav HaTzafon, the Reading compound and Shai Agnon Street (south); the "
  "beach and the promenade (west).", src="TLVSD", write="No distances. The port of Tel Aviv is NOT a boundary.")
c("SDH-04", "sde-dov-hub", "plan", "The master plan describes a mixed-use quarter of about 16,000 apartments for about 40,000 "
  "residents; it came into force in August 2020.", nums=("16,000", "40,000", 2020, "8.2020"), date="9.8.2020",
  src="TLVSD; GIS528", write="'about 40,000 residents' (41,000 appears in some press: never use it).")
c("SDH-05", "sde-dov-hub", "plan", "Per the plan approved in 2020: about 500,000 m2 of public buildings, about 125,000 m2 of "
  "hotels and about 365 dunam of parks and public gardens; of the 16,000 apartments about 2,400 are for affordable housing at a "
  "reduced price and about 4,500 for special housing (student dormitories, assisted living, rental housing).",
  nums=("500,000", "125,000", 365, "2,400", "4,500", "16,000", 2020), date="12.3.2020", src="NC2003",
  conflict="'4,500 to 6,900 special-housing units' misreads the source (6,900 = 2,400 + 4,500): never write 6,900.")
c("SDH-06", "sde-dov-hub", "plan", "The three compounds: Eshkol (TAMAL/3001) about 4,800 apartments, about 45,000 m2 of "
  "commerce, about 145,000 m2 of employment; the Centre about 7,100 apartments (7,128 in the approved plan), about 60,000 m2 of "
  "commerce, about 155,000 m2 of employment and about 800 hotel rooms; the North about 4,000 apartments, about 20,000 m2 of "
  "commerce, about 30,000 m2 of employment and about 1,150 hotel rooms. No separate hotel figure for Eshkol.",
  nums=("4,800", "45,000", "145,000", "7,100", "7,128", "60,000", "155,000", 800, "4,000", "20,000", "30,000", "1,150", 3),
  date="municipal page read 7.10.2026; 3.2.2025", src="TLVSD; NC2502", write="The Eshkol hotel cell stays without a number.")
c("SDH-07", "sde-dov-hub", "plan", "Dates in force: the master plan August 2020; the Eshkol detailed plan May 2021; the "
  "Centre and North detailed plans 2025.", nums=(2020, "8.2020", 2021, "5.2021", 2025),
  date="9.8.2020; 20.5.2021; 13.2.2025; 8.6.2025", src="GIS528; TLVSD",
  conflict="'Eshkol preceded the master plan' is wrong: never write it.")
c("SDH-08", "sde-dov-hub", "tenders", "In February and March 2025, eight land tenders closed for 6,666 apartments, more than "
  "40% of the apartments planned in the quarter.", nums=(2025, "2.2025", "3.2025", 8, "6,666", 40, "16,000"),
  date="19.2.2025; 26.3.2025", src="BZ2503; NC2502T (3,922 + 2,744 = 6,666; 6,666 / 16,000 = 41.7%)",
  write="'eight tenders' in words or 8; never 41.7% (not in the Hebrew).")
c("SDH-09", "sde-dov-hub", "projects", "Rainbow Tel Aviv (Israel Canada, Eshkol compound): a tower of 39 to 40 floors and "
  "boutique buildings; 459 apartments per the developer (the land tender spoke of 480); the main contractor Ashtrom was chosen "
  "in January 2026; delivery in stages, the last stage expected in 2030.",
  nums=(39, 40, 459, 480, 2026, "1.2026", 2030), date="1.1.2026", src="NC2601R; AMS; GL2608",
  conflict="'480 per marketing / 459 per permit' were wrong attributions: never use them.",
  write="2030 is the expected last stage, not a contractual date.")
c("SDH-10", "sde-dov-hub", "projects", "Project facts (as the area map cards): FIRST, a 45-floor tower and three boutique "
  "buildings of 9 floors, 350 apartments; ASHIRA, 406 apartments in four buildings including a 35-floor tower; DIMRI YAMA, 458 "
  "apartments in a 40-floor tower, a 16-floor mid-rise (towerlet) and two 9-floor buildings; ZOHI, about 230 apartments; GINDI "
  "VOGUE, 708 apartments on two lots in the Centre, including a 45-floor tower and three 20-floor towers; UTOPIA, 337 apartments "
  "in four buildings around a shared courtyard in Eshkol.",
  nums=(45, 3, 9, 350, 406, 4, 35, 458, 40, 16, 2, 230, 708, 20, 337), src="AMS; NC2507; NC2502T; NC2604; ICE2105",
  write="Only if the Hebrew row carries it (the six table cells are optional edits).")
c("SDH-11", "sde-dov-hub", "prices", "Rainbow Tel Aviv: the average of all apartments sold up to March 2026 was about ₪81,800 "
  "per m2.", nums=("81,800", 2026, "3.2026"), date="29.5.2026 (to the end of Q1 2026: 81,782)", src="BZ2605",
  conflict="'about 82,000' was the rounded, undated form: use 81,800 with its date.")
c("SDH-12", "sde-dov-hub", "prices", "At these prices (about ₪70,000 to ₪83,000 per m2) a 100 m2 apartment costs about ₪7 to "
  "₪8.3 million (a calculation, as the price calculator on the prices page).",
  nums=(100, 7, "8.3", "7,000,000", "8,300,000", "70,000", "83,000"), src="CALC from SD-02 and SD-03",
  conflict="'a 100 m2 apartment about 8 million' was 100 x an unsourced 80,000: never use it.",
  write="Say it is a calculation.")
c("SDH-13", "sde-dov-hub", "land", "Land prices in the tenders: about ₪3.3 million per apartment on average in the 2022 "
  "tenders (development costs included); about ₪1.7 to ₪2.2 million per apartment in the February 2025 tenders.",
  nums=(2022, "3.3", "3,300,000", 2025, "2.2025", "1.7", "2.2", "1,700,000", "2,200,000"), date="19.2.2025",
  src="ICE2502; BZ2502; NC2502T", conflict="'over 3 million per unit' without a year: never use it.")
c("SDH-14", "sde-dov-hub", "deals", "Luxury deals of ₪14 million and more have been published in the quarter (since 10.2024).",
  nums=(14, "14,000,000"), date="28.10.2024", src="GL2410")
c("SDH-15", "sde-dov-hub", "planning", "Public participation: five meetings during the master plan; four topic meetings for the "
  "detailed plans (traffic and transport; building and urban design; building and programme; housing).", nums=(5, 4),
  src="TLVSP", write="Words or digits.")
c("SDH-16", "sde-dov-hub", "planning", "'In a new neighbourhood you buy the apartment and also the first ten years of the "
  "neighbourhood being built around it' (the page's own line).", nums=(10,), src="Hebrew source (editorial)")
c("SDH-17", "sde-dov-hub", "page", "The page was checked and updated in October 2026 (7.10.2026).",
  nums=(2026, "10.2026", "7.10.2026"), src="THIS", write="Only in the Hebrew page; the translations carry no date line.")

# ======================================================================= SDP: the prices page (live, aligned 7.10.2026)
c("SDP-01", "sde-dov-prices", "deals", "In December 2025 three apartments on floors 38, 39 and 43 of a tower facing the sea "
  "sold for about ₪107,700 to ₪119,200 per m2 of built area (balconies not counted).",
  nums=(3, 38, 39, 43, "107,700", "119,200", 2025, "12.2025"), date="18.12.2025", src="BZ2512 (CALC on the built area)")
c("SDP-02", "sde-dov-prices", "deals", "March 2026: two deals for 5-room apartments of 132 m2 on floor 9 in one project, "
  "₪7.16 to ₪7.57 million, about ₪54,200 to ₪57,300 per m2 ('deals of 54,000-57,000 per m2').",
  nums=(5, 132, 9, 2, "7.16", "7.57", "7,160,000", "7,570,000", "54,200", "57,300", "54,000", "57,000", 2026, "3.2026"),
  date="3.5.2026 (deals of 3.2026)", src="ICE0305")
c("SDP-03", "sde-dov-prices", "prices", "The range of deals in the April 2026 survey: about ₪60,200 to ₪138,000 per m2.",
  nums=("60,200", "138,000", 2026, "4.2026"), date="15.4.2026", src="NC2604")
c("SDP-04", "sde-dov-prices", "prices", "Tel Aviv-Yafo: the median of deals in the two years to October 2025 (October 2023 to "
  "October 2025) was ₪52,856 per m2.", nums=("52,856", 2023, 2025, "10.2023", "10.2025", 2), date="10.2023-10.2025",
  src="TA (Tax Authority deals; the site's Tel Aviv card)", write="A median of deals, not an average.")
c("SDP-05", "sde-dov-prices", "prices", "In one project in the quarter the average rose from about ₪64,700 per m2 in the first "
  "quarter of 2026 to about ₪81,600 per m2 in the eight deals after it (VAT included).",
  nums=("64,700", "81,600", 1, 2026, 8, "1-3"), date="6.6.2026", src="BZ2606",
  write="'eight deals' (a small sample).")
c("SDP-06", "sde-dov-prices", "prices", "In June 2026 one developer valued its unsold apartments at about ₪73,200 per m2 incl. "
  "VAT, below its 2025 deals average of about ₪82,500.", nums=("73,200", "82,500", 2025, 2026, "6.2026"), date="6.6.2026",
  src="BZ2606; GL2609", write="An estimate, not a deal.")
c("SDP-07", "sde-dov-prices", "prices", "The official (list) prices in the projects: ₪75,000 to ₪85,000 per m2 before "
  "financing benefits.", nums=("75,000", "85,000", 2026, "6.2026"), date="6.6.2026", src="BZ2606",
  write="List prices before financing benefits, not deals.")
c("SDP-08", "sde-dov-prices", "prices", "Per one developer in the quarter (December 2025), selected apartments sold at "
  "₪90,000 to ₪100,000 per m2.", nums=("90,000", "100,000", 2025, "12.2025"), date="11.12.2025", src="ICE2512")
c("SDP-09", "sde-dov-prices", "rooms", "2 rooms: recent deals in one Eshkol project ₪2.8 to ₪3.1 million (May 2026); in its "
  "presale ₪2.4 to ₪2.7 million. Another 2-room deal: 54 m2, floor 9, ₪3.665 million, about ₪67,900 per m2 (2026).",
  nums=(2, "2.8", "3.1", "2,800,000", "3,100,000", "2.4", "2.7", "2,400,000", "2,700,000", 54, 9, "3.665", "3,665,000",
        "67,900", 2026, "5.2026"), date="21.5.2026; 3.5.2026", src="ICE2105; ICE0305")
c("SDP-10", "sde-dov-prices", "rooms", "3 rooms of 82-83 m2: recent deals in the same Eshkol project ₪4.6 to ₪4.8 million "
  "(May 2026).", nums=(3, 82, 83, "4.6", "4.8", "4,600,000", "4,800,000", 2026, "5.2026"), date="21.5.2026", src="ICE2105")
c("SDP-11", "sde-dov-prices", "rooms", "4-5 rooms of 104-126 m2 on floors 10-13, four deals: ₪6.49 to ₪7.73 million, about "
  "₪61,300 to ₪62,800 per m2 (2026).", nums=(4, 5, 104, 126, 10, 13, "6.49", "7.73", "6,490,000", "7,730,000", "61,300",
                                             "62,800", 2026), date="3.5.2026", src="ICE0305")
c("SDP-12", "sde-dov-prices", "rooms", "5 rooms of 139.7 m2 on floor 18 (of 20), on one project's price list: ₪11.954 million, "
  "about ₪85,600 per m2 (October 2025); in round words 'up to ₪11.95 million on one price list'.",
  nums=(5, "139.7", 18, "11.954", "11,954,000", "11.95", "11,950,000", "85,600", 2025, "10.2025"), date="26.10.2025",
  src="ICE2510", write="A price-list (asking) price, not a deal.")
c("SDP-13", "sde-dov-prices", "rooms", "Summaries of the published deals and price lists: 2-room apartments sold in 2026 for "
  "about ₪2.8 to ₪3.7 million; 5-room apartments of 126-132 m2 sold in 2026 for about ₪7.2 to ₪7.7 million; 5 rooms in deals and "
  "price lists from about ₪7.2 to about ₪12 million; 4 and 5 rooms about ₪6.5 to ₪12 million.",
  nums=(2, 4, 5, "2.8", "3.7", "2,800,000", "3,700,000", 126, 132, "7.2", "7.7", "7,200,000", "7,700,000", 12, "12,000,000",
        "6.5", "6,500,000", 2026), src="ICE2105; ICE0305; ICE2510; NC2604",
  write="Ranges as written in the Hebrew; no new averages.")
c("SDP-14", "sde-dov-prices", "deals", "A 1-room apartment of 32 m2 on floor 4 of one of the towers sold in July 2023 for "
  "₪3.1 million.", nums=(1, 32, 4, "3.1", "3,100,000", 2023, "7.2023"), date="29.11.2023 (deal of 7.2023)", src="GL2311",
  conflict="'2.3 million for 32 m2' had no source: never use it.")
c("SDP-15", "sde-dov-prices", "projects", "FIRST (Hagag Group, Central compound): by July 2025, about 94 apartments plus 8 more "
  "agreements were marketed for about ₪853 million, about ₪8.4 million per apartment on average; its 2025 average about "
  "₪75,500 per m2.", nums=(94, 8, "853", "853,000,000", "8.4", "8,400,000", "75,500", 2025, "7.2025"),
  date="17.7.2025; 18.12.2025; 15.4.2026", src="NC2507; BZ2512; NC2604")
c("SDP-16", "sde-dov-prices", "prices", "Eshkol: in one project the recent deals were at ₪60,000 to ₪62,000 per m2 (May "
  "2026); the Centre and the North have no separate published average.",
  nums=("60,000", "62,000", 2026, "5.2026"), date="21.5.2026", src="ICE2105", write="'no separate average published'.")
c("SDP-17", "sde-dov-prices", "compare", "Ramat Aviv: recent deals average about ₪55,000 per m2 (June 2026); Ramat Aviv "
  "Gimel about ₪51,000 to ₪53,000 per m2 (August 2026). Park Tzameret: depends on the tower and the floor (no figure).",
  nums=("55,000", "51,000", "53,000", 2026, "6.2026", "8.2026"), date="6.6.2026; 2.8.2026", src="ICE0606; BZ2608",
  conflict="'Park Tzameret 90,000-120,000' had no source: never use it.")
c("SDP-18", "sde-dov-prices", "forecast", "In March 2025 the developer Yigal Dimri estimated that in a decade or two prices in "
  "the quarter could reach ₪150,000 per m2: a very optimistic forecast against today's average of about ₪83,000.",
  nums=("150,000", 2025, "3.2025", 10, 20), date="3.3.2025", src="NC2503", write="A forecast; 'a decade or two'.")
c("SDP-19", "sde-dov-prices", "method", "Counts in the page's own words: four main price factors; three markets (small "
  "apartments, family apartments, premium); at least ten parameters for comparing two apartments.", nums=(4, 3, 10),
  src="Hebrew source (editorial)", write="Words or digits.")

CLAIMS = C
IDS = [x["claim_id"] for x in C]
assert len(IDS) == len(set(IDS)), "duplicate claim_id"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    io.open(os.path.join(here, "claims.json"), "w", encoding="utf-8").write(json.dumps(C, ensure_ascii=False, indent=1) + "\n")
    print(len(C), "claims ->", os.path.join(here, "claims.json"),
          {p: sum(1 for x in C if x["page"] == p) for p in ("sde-dov-hub", "sde-dov-prices", "both")})
