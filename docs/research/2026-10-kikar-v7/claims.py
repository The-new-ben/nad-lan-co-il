# -*- coding: utf-8 -*-
"""V7 (C1, Maya's breakthrough): the claim graph for the Kikar Hamedina articles. One fact = one claim_id.

Every claim carries: the statement (English, canonical), the numbers it allows in an article (for the fact check), the date, the
source (S-ids are facts.md's Sources list; A = area.md, B = facts.md "Additions, V7"), the conflict it carries, and how to write it.
Sources are named HERE only: the articles never name a source (the owner, 1.10.2026).

Rules folded in:
- conflicts between sources -> the conservative figure, written with "about" (כ-); the other figure is NOT given;
- asking prices are asking prices, deals are deals; derived numbers are marked derived and written as rounded results;
- the project has no developer: the landowners' company owns it (the owner, 1.10.2026);
- what is not published is written as "not published", never guessed (iron law 3).
"""
import json, os

C = []


def c(cid, topic, claim, nums=(), date="", src="", conflict="", write=""):
    C.append({"claim_id": cid, "topic": topic, "claim": claim, "numbers": [str(n) for n in nums], "date": date,
              "source": src, "conflict": conflict, "write_as": write})


# ---------------- the project ----------------
c("P01", "project", "Name: Kikar Hamedina Towers (מגדלי כיכר המדינה); also called the Spiral Towers (מגדלי הספירלה).",
  src="S1; S6")
c("P02", "project", "The three towers stand inside the round Kikar Hamedina square in north Tel Aviv, ringed by He Be'Iyar street; "
  "Weizmann Street meets the square from the south and Jabotinsky Street from the east. The municipality's neighbourhood name: "
  "'the New North, Kikar Hamedina area' (הצפון החדש - סביבת כיכר המדינה).", src="S5; S6; A (TLV GIS 507, 511)")
c("P03", "project", "The building-permit addresses of the towers: He Be'Iyar 25, 45 and 65.", nums=(25, 45, 65),
  date="record read 30.9.2026", src="A: TLV GIS layer 499, building-site file 61-1-2018-0391")
c("P04", "project", "Three residential towers: two of 40 floors and one of 37 floors (tower B).", nums=(3, 40, 37),
  date="read 30.9.2026", src="S1 Ashtrom; S3 Electra; S5 he.wikipedia",
  conflict="The city's buildings layer lists all three at 40 floors, and its permit record notes a request for 2 more floors "
  "in tower B. Older reports say 42 floors.", write="40, 40 and 37 floors. Optionally: a request for 2 more floors in tower B "
  "was recorded. Never 42.")
c("P05", "project", "Height: about 160 m for towers A and C and about 157 m for tower B.", nums=(160, 157),
  date="read 30.9.2026", src="S5; A (city layer: 160 / 158.2 / 160 m)",
  conflict="Other lists give 156 m or 153 m.", write="'about 160 m' (the conservative wording: 'up to about 160 m').")
c("P06", "project", "Where each tower stands on the plot: tower A to the south-west, tower B to the south-east, tower C to the "
  "north-east (about 75-78 m from the plot centre).", nums=(75, 78), src="A: TLV GIS buildings layer 513")
c("P07", "project", "Each floor is turned 1.25 degrees relative to the floor below; over 40 floors the turn adds up to about "
  "50 degrees (about 46 degrees over 37 floors).", nums=("1.25", 50, 46, 40, 37),
  src="S5; S21; S35; S66", conflict="One supplier case study says 2.5 degrees: never use it.")
c("P08", "project", "The architects' concept: each residential floor steps back slightly from the floor below and turns in a "
  "circular movement inspired by the round shape of the square; the façades are a modern reading of the ring's buildings: "
  "floor slabs and white curtain walls.", src="S38")
c("P09", "project", "The façade: floor-to-ceiling glass and white aluminium curtain walls, insulated glass with built-in electric "
  "shading, aluminium-and-glass shading fins 300 mm deep, full-height pivot windows with inner railings.", nums=(300,),
  src="S35 (façade contractor's project page)")
c("P10", "project", "453 apartments in all; about 150 m² per apartment on average.", nums=(453, 150),
  src="S1; S5; S8; S19; S20", date="2021-2025")
c("P11", "project", "The plan for the compound (in force since 24.6.2013) allows 453 housing units, about 59,175 m² of housing and "
  "6,000 m² of public buildings; the plan area is about 78 dunam (77.743).", nums=(453, "59,175", "6,000", 78, "77.743", 2013),
  src="A: TLV GIS layer 528; S27")
c("P12", "project", "The apartments belong to about 250 rights holders, the heirs of private investors who bought the plots in "
  "1942; they formed an association in 1997 that became the landowners' company. The rights holders received the apartments in "
  "exchange for the land; the order of choice was set by a lottery.", nums=(250, 1942, 1997),
  src="S8; S12; S40", conflict="Other counts: 150, 240, 253, 260+.", write="'about 250 rights holders'. Never the word "
  "'developer' (יזם): 'the landowners' / 'the landowners' company'.")
c("P13", "project", "At most 200 to 250 apartments are expected to be offered for sale, because many owners plan to live in the "
  "towers (a 4.2025 report).", nums=(200, 250), date="19.4.2025", src="S20")
c("P14", "project", "There is no sales office and no price list: the apartments are resold by their owners, usually through "
  "real-estate brokers.", date="23.9.2025", src="S12; S40")
c("P15", "project", "Architects: Yaski Mor Sivan Architects (MYS), chosen in a competition in 2000.", nums=(2000,), src="S8; S10")
c("P16", "project", "Builders: Electra Construction and Ashtrom, jointly, under a construction contract of about ₪1.4 billion "
  "(₪700 million each); they were chosen in November 2021 from six bidding groups.", nums=("1.4", 700, 2021, 6, "11.2021"),
  date="28.11.2021", src="S15")
c("P17", "project", "Project management: Waxman Govrin Geva (WXG), with the project since 2001. Landscape architecture: T.M.A.",
  nums=(2001,), src="S8; S17; S21")
c("P18", "project", "Financing: Bareket Capital with Clal and Migdal, credit of about ₪2.05 billion.", nums=("2.05",),
  date="25.9.2025", src="S13", conflict="Other reports: about ₪1.7-2 billion.", write="'about ₪2 billion' is also fine.")
c("P19", "project", "15 high-speed lifts (4 to 6 metres a second) serve the apartments.", nums=(15, 4, 6), src="S4 (Electra, Hebrew page)")
c("P20", "project", "Air conditioning: a Daikin VRF system (central multi-split).", src="S3; S4")
c("P21", "project", "Garbage chutes and entrance doors are supplied by Rav Bariach.", src="S45 (4.6.2025)")
c("P22", "project", "Construction method: the circular cores rose with imported slip forms, about 1.5 m a working day, which is "
  "5 to 7 floors a month per tower; about 7 floors a month against about 3 in conventional building.",
  nums=("1.5", 5, 7, 3), src="S31; S13")
c("P23", "project", "All three towers are built at the same time, not in phases.", src="S10 (16.9.2023)")
c("P24", "project", "Foundations: about 300,000 m³ of earth excavated; three reinforced rafts on piles.", nums=("300,000", 3),
  src="S33; S1")
c("P25", "project", "Milestones: excavation and shoring permit 12.2018; building permit 12.2022; first concrete pour 18.12.2022; "
  "the city's building-site record lists the stage 'frame completed' (גמר שלד) as of 23.4.2026.",
  nums=("12.2018", "12.2022", "18.12.2022", "23.4.2026", 2018, 2022, 2026), src="S30; S8; A (TLV GIS 499)")
c("P26", "project", "Timeline anchors: 1942 plots bought; 1997 owners' association; 2000 architects chosen; 24.6.2013 the plan "
  "in force; 3.2018 the traffic amendment of the plan in force; 11.2021 builders chosen; 12.2022 building permit and first pour; "
  "4.2026 frame completed.", nums=(1942, 1997, 2000, "24.6.2013", 2013, "3.2018", 2018, "11.2021", "12.2022", "4.2026"),
  src="S8; S27; S29; S15; A")
c("P27", "project", "The plot of the towers is about 28 dunam of residential land (lot 101, about 28,380 m²); 13.8 dunam on the "
  "west of the square hold the school and the community centre.", nums=(28, "28,380", "13.8"), src="A: TLV GIS 837; S26")

# ---------------- delivery ----------------
c("D01", "delivery", "Occupancy: the published estimates range from 2026 to 2028. The builders' published dates are 2026 and "
  "April 2027; a 9.2025 estimate by the project's financier spoke of 'within about two years' (about 2027); a 4.2025 report said "
  "the end of 2028. No official occupancy date (Form 4) has been published.",
  nums=(2026, 2027, 2028, "4.2027", "9.2025", "4.2025"), src="S1; S3; S13; S12; S20",
  write="Give the range 2026-2028 and the most recent estimates without naming who said them by name (roles are fine: "
  "'the builders', 'the financier'). Never one date as fact. For a given apartment, the delivery date is the one in the "
  "seller's contract.")
c("D02", "delivery", "The public works in the square (park, ring street He Be'Iyar) are expected to be completed by the end of "
  "2027 (the municipality's project director, 9.2026). This is the PUBLIC works, not the towers.", nums=(2027,),
  date="24.9.2026", src="S21")

# ---------------- apartments ----------------
c("U01", "apartments", "No official unit mix or floor plans have been published; apartments per floor were not published. "
  "Apartment sizes seen in published deals and listings: 4 rooms of 132, 134, 140 and 148 m²; 5 rooms of 154 m²; 4 rooms of "
  "168 m² (planned as 5); 170 m² and 200 m² units; a penthouse of 258 m² with 57 m² outdoor (a 42 m² terrace and a 15 m² "
  "balcony).", nums=(4, 5, 132, 134, 140, 148, 154, 168, 170, 200, 258, 57, 42, 15),
  src="facts.md 1.5, 1.12, 1.14", write="Write as 'sizes that appeared in published deals and listings', not as a mix.")
c("U02", "apartments", "Listings describe the towers as 4 and 5 rooms (living room plus 3-4 bedrooms) with penthouses on top.",
  nums=(4, 5), src="S56; S57 (marketing listings)")
c("U03", "apartments", "Balconies in published listings: about 12 to 15.5 m² (154 m² + 12; 134 m² + 14; 168 m² + about 14.5; "
  "132 m² + about 15.5).", nums=(12, "15.5", "14.5", 14), src="S50; S25; S49; S52")
c("U04", "apartments", "Specification items that listings advertise (advertised, not an official specification): fishbone "
  "parquet, designer marble, VRF air conditioning, central heating, a safe room (mamad) with a full bathroom, a smart-home "
  "system, high ceilings, security 24/7.", src="S49; S53", write="'as listings describe them'.")
c("U05", "apartments", "Listings show two parking spaces and a storage room with a typical apartment; one listing offers 4 parking "
  "spaces and 2 storage rooms.", nums=(2, 4), src="S41; S49; S51")
c("U06", "apartments", "A published penthouse listing: 258 m² inside and 57 m² outside, 4 bedrooms, 3.5 bathrooms, views to the "
  "north, west and south, 2 parking spaces.", nums=(258, 57, 4, "3.5", 2), src="S53 (about 1.2025)")
c("U07", "apartments", "A published listing on a high floor describes a north-west sea view.", src="S49 (29.1.2026)")
c("U08", "apartments", "The lobby: listings describe a lobby with a security guard.", src="S50")

# ---------------- facilities and parking ----------------
c("F01", "facilities", "On one of the basement levels: a swimming pool, a gym, a spa, treatment rooms and multi-purpose halls. "
  "The city's building-site record lists a spa, a pool of 290 m³ and a gym in the basements.", nums=(290,),
  src="S1; A (TLV GIS 499)")
c("F02", "facilities", "Parking: about 1,620 underground spaces on 3 levels; about 906 of them private for the apartment owners "
  "and about 720 public (14 for disabled drivers).", nums=("1,620", 3, 906, 720, 14),
  src="S1; S8; S21", conflict="1,626 = 906 + 720 in one 2026 report; 4 levels in a 2015 plan.",
  write="'about 1,620 spaces on 3 underground levels'.")
c("F03", "facilities", "A dedicated internal access road serves school drop-off at set hours.", src="S21 (24.9.2026)")
c("F04", "facilities", "The project's own commerce is a few small café kiosks in the park (no shopping mall); the shops stay in "
  "the square's ring.", src="S12; S8; S21", conflict="3 or 4 kiosks.", write="'a few small café kiosks'.")

# ---------------- park, school, community ----------------
c("K01", "park", "A public park of about 40 dunam (about 4 hectares) at the heart of the square.", nums=(40, 4),
  src="S13; S21", conflict="Other figures: 26 to about 50 dunam.", write="'about 40 dunam'.")
c("K02", "park", "An ecological pond 1 m deep with perennial planting, flow channels, bridges and paths.", nums=(1,),
  src="S21; S22", conflict="The pond's area: 3.5 or 8 dunam in older plans.", write="Give the depth, never the area.")
c("K03", "park", "560 new trees planted and 36 existing trees kept.", nums=(560, 36), src="S21; S22")
c("K04", "park", "A 750 m running track; a wide perimeter boulevard with a bike path, three rows of trees, kiosks and shaded "
  "seating; lawns, playgrounds, a dog garden, game tables.", nums=(750, 3), src="S21; S22; S23")
c("K05", "park", "Public works of about ₪150 million.", nums=(150,), src="S21 (24.9.2026)")
c("K06", "park", "A new state primary school inside the square (the north building of the public plot): 18 classes plus 6 "
  "special-education classes, with an underground sports hall and a sunken courtyard; it opened with the start of a school year "
  "(reported 24.9.2026). The city's 2026-27 schools list places two schools at He Be'Iyar 75: the Kikar Hamedina primary school "
  "and the Meir Shalev middle school.", nums=(18, 6, 75, 2026, 27, "2026-27"), src="S26; S21; A (TLV GIS 769)")
c("K07", "park", "A community centre in the south building of the public plot: activity rooms, a dance studio, a multi-purpose "
  "hall, an urban lounge and open courtyards; a café of about 60 m².", nums=(60,), src="S22; S26",
  conflict="4 or 5 floors.", write="No floor count.")
c("K08", "park", "The school and the community centre flank an open walk that continues Jabotinsky Street into the park, on the "
  "west side of the square.", src="S26; A")

# ---------------- the square ----------------
c("Q01", "square", "Kikar Hamedina is described as the largest square in Israel and the largest plaza in Tel Aviv.",
  src="S6; S7", write="'considered the largest square in Israel'.")
c("Q02", "square", "Its plan of 1969 was drawn with Oscar Niemeyer; Israel Lotan and Abba Elhanani designed the ring buildings, "
  "built mostly in the early 1970s. The circle first appeared in a 1939 city plan.", nums=(1969, 1970, 1939), src="S6; S7")
c("Q03", "square", "In the 1950s and 1960s a circus (Medrano) pitched its tent in the sandy centre; on 3.9.2011 about 300,000 "
  "people gathered there in the March of the Million, the peak of the social-justice protests.",
  nums=(1950, 1960, "3.9.2011", 2011, "300,000"), src="S71; S6; S7")
c("Q04", "square", "The ring is Tel Aviv's luxury-fashion address. Houses named in a public list: Gucci, Saint Laurent, Givenchy, "
  "Dior, Valentino, Chloé, Burberry, Fendi, Dolce & Gabbana. Gucci reopened a new store in the ring (reported 1.2025); a watch and "
  "jewellery lounge of about 250 m² opened in 12.2025.", nums=(250, "12.2025", "1.2025"), src="S7; S67; S70",
  write="Shops change: say 'among the houses on the ring' and never promise a specific store today.")
c("Q05", "square", "Cafés and food on the ring, a minute's walk: Bakery Kikar Hamedina, Lechem Erez, Nuchi, Open, Nespresso; "
  "supermarkets City Market and Victory; a Super-Pharm pharmacy on Weizmann.", nums=(1,), src="A (TLV open data, OSM, 30.9.2026)")
c("Q06", "square", "About 13,300 people live near the square, in about 6,000 households (2023 municipal data).",
  nums=("13,300", "6,000", 2023), src="S73")
c("Q07", "square", "The ring around the towers is being renewed too: 16 other building sites within 250 m, most of them "
  "urban-renewal rebuilds of 7 to 9 floors; wider sidewalks, a circular bike path and four new pedestrian and cycle crossings.",
  nums=(16, 250, 7, 9, 4), src="A (TLV GIS 499); S73; S12")

# ---------------- area, transport, services ----------------
c("T01", "transport", "Light rail Purple Line: Ichilov station about 350 m away, about 2 minutes' walk; planned to open in 2028.",
  nums=(350, 2, 2028), src="A; S62")
c("T02", "transport", "Light rail Red Line: Arlozorov station about 860 m away, about 11 minutes' walk; running since 18.8.2023.",
  nums=(859, 860, 11, "18.8.2023", 2023), src="A; S64")
c("T03", "transport", "Tel Aviv Savidor Center railway station: about 850 m, about 9 minutes' walk.", nums=(852, 850, 9), src="A")
c("T04", "transport", "Light rail Green Line on Ibn Gabirol: Arlozorov station about 730 m, about 9 minutes' walk; planned for "
  "2030 in full (southern section 2028).", nums=(730, 9, 2030, 2028), src="A; S63")
c("T05", "transport", "53 bus lines stop within 5 minutes' walk of the ring, 95 within 10 minutes (a normal weekday, 8.9.2026).",
  nums=(53, 5, 95, 10, "8.9.2026"), src="A (Ministry of Transport GTFS via Open Bus)")
c("T06", "transport", "Roads: Weizmann about 140 m, Namir Road about 530 m, Ibn Gabirol about 720 m, the Ayalon Highway about "
  "800 m.", nums=(139, 140, 526, 530, 718, 720, 804, 800), src="A")
c("T07", "area", "Ichilov (Tel Aviv Sourasky) Medical Center: about 0.7-0.85 km, about 9 minutes' walk.",
  nums=("0.7", "0.85", 9), src="A")
c("T08", "area", "Park HaYarkon: its nearest edge about 1 km north, about 13 minutes' walk; Sportek about 22 minutes.",
  nums=(1, 13, 22), src="A", conflict="An old report says 200 m: never use it.")
c("T09", "area", "Schools and kindergartens: the new primary school inside the square (1 minute); Ahavat Zion primary (3 minutes); "
  "Herzliya Hebrew Gymnasium (4 minutes, about 400 m); a municipal kindergarten 1 minute away; several kindergartens on Lisin "
  "Street 4 minutes away.", nums=(1, 3, 4, 400, 406), src="A (TLV 2026-27 layers)",
  write="Registration zones are set by the city every year: never promise a school place.")
c("T10", "area", "Green places within 2-4 minutes: Gan Avraham, Biltmore garden, Pollak garden; a dog park in Lisin grove "
  "(4 minutes).", nums=(2, 4), src="A")
c("T11", "area", "Health: a Clalit clinic 4 minutes; pharmacies 1-3 minutes.", nums=(4, 1, 3), src="A")
c("T12", "area", "Culture: Beit Hahayal theatre 6 minutes; the Tel Aviv Museum of Art about 14 minutes; the Arlozorov 97 community "
  "country club 5 minutes; synagogues from 1 minute (Weizmann 71).", nums=(6, 14, 97, 5, 1, 71), src="A")
c("T13", "view", "What lies in each direction (straight-line distances from the plot; what a given apartment sees depends on its "
  "tower, floor and direction and was not published): the Mediterranean, nearest waterline about 2 km to the north-west; the Tel "
  "Aviv port about 1.9 km north-west; Ramat Aviv about 2.5 km north and Tel Aviv University about 3.2 km north-north-east; Park "
  "HaYarkon to the north and north-east; Azrieli towers about 1.4 km south; Azrieli Sarona about 1.6 km south; Ichilov about "
  "0.7 km south; City Hall and Rabin Square about 1 km south-west; Habima about 1.9 km south-west; the Ayalon and the Savidor "
  "station about 0.8 km east.", nums=(2, "1.9", "2.5", "3.2", "1.4", "1.6", "0.7", 1, "0.8"), src="A (section 11)")
c("T14", "area", "Neighbourhood prices and character are those of north Tel Aviv: Ibn Gabirol, Yehuda HaMaccabi, Arlozorov and "
  "the Tzameret towers around; Ichilov within walking distance.", src="S47")

# ---------------- prices ----------------
c("R01", "prices", "Three published deals in the towers, all 4 rooms of 140 m² on floors 38-39: ₪10.63M on floor 38 (12.2024, "
  "about ₪75,900/m²); ₪9.59M on floor 39 (5.2024, about ₪68,500/m²); ₪9.58M on floor 38 (4.2024, about ₪68,400/m²). Which tower "
  "each was in was not published.",
  nums=("10.63", "9.59", "9.58", 38, 39, 140, 4, "12.2024", "5.2024", "4.2024", "75,900", "68,500", "68,400", "75,913",
        "68,520", "68,405"), src="S11 (2.5.2025); S13")
c("R02", "prices", "The three deals' range is ₪9.58M to ₪10.63M; their average about ₪9.93M, about ₪71,000/m² (derived).",
  nums=("9.58", "10.63", "9.93", "71,000"), src="derived from R01")
c("R03", "prices", "The average deal in the towers is about ₪65,000/m²; on the high floors and in the penthouses ₪80,000 to "
  "₪150,000/m².", nums=("65,000", "80,000", "150,000", "9.2025", "9.2026", 2025, 2026), date="23.9.2025; 24.9.2026", src="S12; S21")
c("R04", "prices", "Asking prices published (asking, not deals): a penthouse on floor 39, 258 m² + 57 m² outdoor: ₪43M (about "
  "₪150,000/m², ~1.2025-4.2025); floor 35, 154 m² + 12 m² balcony, south-east: ₪14.5M; a high floor, 4 rooms of 168 m² + about "
  "14.5 m², north-west sea view: ₪13.7M (1.2026); floor 12, 148 m²: ₪10.3M (4.2025); floor 16, 4 rooms of 132 m² + about "
  "15.5 m²: ₪10M.", nums=(39, 258, 57, 43, "150,000", 35, 154, 12, "14.5", 168, "13.7", "10.3", 148, 16, 132, "15.5", 10,
                          "1.2026", "4.2025"),
  src="S53; S50; S49; S20; S52")
c("R05", "prices", "Low asking prices of about ₪6.25-6.3M appeared for the RIGHTS to an apartment (for example 134 m² on floor 23, "
  "12.2024; 154 m² on floor 4); one such listing says the buyer still pays the construction cost, about ₪28,000 per m². So a "
  "rights price and a finished-apartment price are not comparable.", nums=("6.25", "6.3", "6.29", 134, 23, 154, 4, "28,000",
                                                                            "12.2024"),
  src="S25; S51; S20", write="Explain the difference; never present ₪6.3M as the price of an apartment.")
c("R06", "prices", "Around the square: most apartments sold in the past year went for ₪63,000-66,000/m² (official deal records, "
  "4.2026); the New North / Kikar Hamedina neighbourhood averaged ₪67,747/m² for 3-room deals (7.2025), the 8th most expensive "
  "in Tel Aviv; 148 apartments sold there in a year at an average of ₪68,000/m² and ₪5.66M per deal (data to 6.2024).",
  nums=("63,000", "66,000", "4.2026", "67,747", "7.2025", 8, 148, "68,000", "5.66", "6.2024"), src="S43; S46; Globes 1001481134")
c("R07", "prices", "Rentals in the towers start only after occupancy; no rent has been published for the towers.",
  src="facts.md GAPS", write="Never give a rent figure for the towers.")

# ---------------- buying costs (national rules) ----------------
c("B01", "costs", "Purchase tax for an Israeli resident buying a single (only) apartment: 0% up to ₪1,978,745; 3.5% up to "
  "₪2,347,040; 5% up to ₪6,055,070; 8% up to ₪20,183,565; 10% above. The amounts updated 16.1.2024 were frozen by law, so they "
  "apply in 2026.", nums=(0, "1,978,745", "3.5", "2,347,040", 5, "6,055,070", 8, "20,183,565", 10, "16.1.2024", 2026),
  src="B (Tax Authority directive 2/2024; Economic Efficiency Law 26.12.2024)")
c("B02", "costs", "Purchase tax on an additional apartment, and for a foreign resident: 8% up to ₪6,055,070 and 10% above.",
  nums=(8, "6,055,070", 10), src="B")
c("B03", "costs", "Example (derived), a ₪10,000,000 apartment: about ₪514,000 of purchase tax for an Israeli buying a single "
  "apartment; about ₪879,000 for an additional apartment or a foreign resident.",
  nums=("10,000,000", 10, "514,000", "513,886", "879,000", "878,899"), src="derived from B01-B02")
c("B04", "costs", "New immigrants (olim) have a reduced purchase-tax track under conditions set by law; check it with a tax "
  "advisor.", src="B", write="No rates.")
c("B05", "costs", "Mortgage limits (Bank of Israel, since 11.2012): up to 75% of the value for a first (single) home, up to 70% "
  "for a replacement home, up to 50% for an additional / investment apartment and for a non-resident buyer.",
  nums=(75, 70, 50, 2012), src="B (BoI; Globes 29.10.2012; directive 329)")
c("B06", "costs", "Example (derived), a ₪10,000,000 apartment: own equity of at least ₪2.5M with a 75% mortgage, ₪3M at 70%, "
  "₪5M at 50%.", nums=("10,000,000", "2.5", 75, 3, 70, 5, 50), src="derived from B05")
c("B07", "costs", "A real-estate broker is entitled to a fee only if licensed, holding a signed written order from the client, and "
  "the effective cause of the deal; the fee is what the written order says.", src="B (Real Estate Brokers Law 1996, s.9)")

CLAIMS = C
IDS = [x["claim_id"] for x in C]
assert len(IDS) == len(set(IDS)), "duplicate claim_id"

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(C, open(os.path.join(here, "claims.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(C), "claims ->", os.path.join(here, "claims.json"))
