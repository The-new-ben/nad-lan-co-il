# Greece property price list: asking prices by place (retrieved 22 October 2026)

Companion of `prices.json` (built by `build_prices.py`, rendered by `make_md.py`). Every number has its provider, period and URL in the JSON; this page shows the short code.

## How to read it

- **Primary value = Indomio.gr, September 2026** (one provider, one month, sale + rent + yoy for almost every place: 248 of 263 priced places). Where Indomio has nothing, the next source is used (order: Spitogatos Q3 2026, Spitogatos SPI Q2 2026, Spitogatos Q2 blog, xe.gr Q3 2026, Spitogatos regional reports, RE/MAX, Numbeo). Other values stay in "Other sale values" and in `sale_alt` / `rent_alt`.
- These are **asking prices** (listings). Deeds and bank valuations are lower; the Bank of Greece index is the official trend.
- **Gross yield** = asking rent x 12 / asking sale price, same provider and month only. It is before costs, tax, vacancy and furnishing.
- Indomio island rents below 4 €/m², with yoy beyond ±100%, or implying under 2% yield (Kos, Milos, Sifnos, Serifos, Kythnos, Skiathos, Skopelos, Methoni and others) are tiny seasonal samples and were **dropped**, not replaced.
- **GV** = golden-visa minimum (800k: Attica, Thessaloniki regional unit, Mykonos, Santorini, islands over 3,100 inhabitants; 400k elsewhere; "mixed" = unit spans both; "check" = island population near 3,100 or Evia status unverified). **Border permit** = prior permit needed for non-EU buyers (Law 1892/1990); "partial" = only part of the unit; "check" = city not verified. **STR freeze** = no new short-term-rental registrations until 31 Dec 2026 (Athens districts 1-3, Thessaloniki 1st community).
- Coordinates in the JSON are approximate (set by hand to the town or area centre).

**Source codes:** IND = Indomio Sep 2026 (https://www.indomio.gr/en/agora-akiniton/), SQ3 = Spitogatos Q3 2026 press release 22.10.2026 (newmoney.gr / insider.gr), SPI = Spitogatos SPI Q2 2026 (https://www.spitogatos.gr/deiktis-timon), SQ2 = Spitogatos Q2 2026 blog 4.8.2026, XE = xe.gr Q3 2026 (https://www.xe.gr/property/times-akiniton, listing-weighted mean of 3 size bands computed by us), ISL = Spitogatos islands Q2 2026 (16.9.2026), HOL = Spitogatos holiday homes Q2 2026 (24.9.2026), NG = Spitogatos North Greece Q1 2026 (3.7.2026), THS / EPI = Spitogatos Thessaly / Epirus reports (Q3 2025), STU = Spitogatos student housing Q2 2026, RMX = RE/MAX (closed deals, not asking), NUM = Numbeo (crowd-sourced).

## Whole country

| Measure | Value | Period | Source |
|---|---|---|---|
| Indomio asking sale | 2,790 €/m² (+4.7%; Sep 2025 2,664) | 2026-09 | IND |
| Indomio asking rent | 10.68 €/m²/month (+3.8%) | 2026-09 | IND |
| Indomio sale change 3 / 5 years | +14.3% / +38.5% | to 2026-09 | IND |
| Spitogatos asking sale yoy | +5.7% (Q3 2025: +10.0%); Attica +5.0%, Thessaloniki +6.7% | 2026-Q3 | SQ3 |
| Spitogatos asking rent yoy | 0.0% (Q3 2025: +7.2%); Attica +5.0%, Thessaloniki +5.3% | 2026-Q3 | SQ3 |
| Spitogatos Q2 sale yoy | +6.1%; Attica +5.3%, Thessaloniki +7.7%, rest of Greece +7.1% | 2026-Q2 | SPI |
| Bank of Greece apartment index | 114.25 (2007=100), +5.5% yoy; new +6.2%, old +5.0% | 2026-Q2 | BoG (facts.json) |

## Administrative regions and provider groupings (16)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Aegean islands (Indomio grouping) | איי הים האגאי (קיבוץ של Indomio) | 3,627 | +4.1% | 9.71 | +0.9% | 3.2% | IND 2026-09 | ISL 2,941 | mixed | partial | no |
| Attica | אטיקה | 3,218 | +4.6% | 12.48 | +3.0% | 4.7% | IND 2026-09 |  | 800k | no | no |
| Ionian Islands | האיים היוניים | 3,083 | +7.4% | 9.71 | +2.1% | 3.8% | IND 2026-09 | ISL 2,531 | mixed | partial | no |
| Crete | כרתים | 2,603 | +5.0% | 9.82 | +7.6% | 4.5% | IND 2026-09 | ISL 2,250 | 800k | no | no |
| Macedonia excl. Thessaloniki (Indomio grouping) | מקדוניה ללא סלוניקי (קיבוץ של Indomio) | 2,054 | +6.6% | 6.52 | +3.0% | 3.8% | IND 2026-09 |  | mixed | partial | no |
| Peloponnese | פלופונס | 1,832 | +6.1% | 8.24 | +4.6% | 5.4% | IND 2026-09 |  | 400k | no | no |
| Epirus | אפירוס | 1,728 | +4.7% | 8.06 | +2.3% | 5.6% | IND 2026-09 |  | 400k | partial | no |
| Thrace (Evros, Xanthi, Rodopi) | תרקיה (אברוס, קסנתי, רודופי) | 1,572 | +7.1% | 8.03 | +8.1% | 6.1% | IND 2026-09 |  | 400k | yes | no |
| Thessaly | תסליה | 1,478 | +11.2% | 7.52 | +3.0% | 6.1% | IND 2026-09 |  | 400k | no | no |
| Central Greece (Sterea Ellada) | יוון המרכזית (סטריאה אלדה) | 1,465 | +6.8% | 6.86 | +10.1% | 5.6% | IND 2026-09 |  | mixed | no | no |
| Central Macedonia | מקדוניה המרכזית |  |  |  |  |  | not published |  | mixed | partial | no |
| East Macedonia & Thrace | מקדוניה המזרחית ותרקיה |  |  |  |  |  | not published |  | 400k | partial | no |
| West Macedonia | מקדוניה המערבית |  |  |  |  |  | not published |  | 400k | partial | no |
| Western Greece | יוון המערבית |  |  |  |  |  | not published |  | 400k | no | no |
| North Aegean | צפון הים האגאי |  |  |  |  |  | not published |  | mixed | yes | no |
| South Aegean | דרום הים האגאי |  |  |  |  |  | not published |  | mixed | partial | no |

Notes: **Aegean islands (Indomio grouping):** Cyclades, Dodecanese, Lesvos, Chios, Samos, Sporades. **Macedonia excl. Thessaloniki (Indomio grouping):** Indomio grouping across Central, West and East Macedonia (not an administrative region). **Peloponnese:** Indomio "Peloponnese" also includes Achaia and Ilia (administratively Western Greece). **Thessaly:** Indomio Thessaly = Larissa, Magnesia, Trikala, Karditsa; the Sporades (administratively Thessaly) are counted by Indomio in Aegean Islands. **Central Greece (Sterea Ellada):** Indomio "Central Greece" also includes Aitoloakarnania (administratively Western Greece). Evia is an island (>3,100 inhabitants), so EUR 800k may apply there; mainland units EUR 400k. **Central Macedonia:** No provider publishes this administrative region as one figure; see Thessaloniki, Halkidiki, Serres, Pieria, Imathia, Pella, Kilkis entries. **East Macedonia & Thrace:** No single published figure; Indomio "Thrace" grouping (Evros, Xanthi, Rodopi) is a separate entry; Kavala and Drama are in Indomio "Macedonia". **West Macedonia:** No single published figure; see Kozani, Kastoria, Florina, Grevena. **Western Greece:** No single published figure; see Achaia/Patras, Ilia, Aitoloakarnania. **North Aegean:** No single published figure; see Lesvos, Chios, Samos. **South Aegean:** No single published figure; see Cyclades and Dodecanese.

## Regional units (prefectures) (47)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Cyclades | הקיקלאדים | 4,565 | +3.4% | 12.64 | -5.9% | 3.3% | IND 2026-09 | SQ3 4,091; SPI 4,063 | mixed | partial | no |
| Chania (regional unit, Crete) | מחוז חאניה | 3,175 | +6.4% | 10.4 | +5.6% | 3.9% | IND 2026-09 | SQ3 3,125; SPI 3,102; ISL 3,102 | 800k | no | no |
| Corfu (regional unit, incl. Paxoi) | מחוז קורפו | 3,032 | +10.7% | 9.98 | -0.4% | 4.0% | IND 2026-09 | SPI 2,417 | mixed | partial | no |
| Halkidiki | חלקידיקי | 2,937 | +5.8% | 12.38 | -5.0% | 5.1% | IND 2026-09 | SPI 2,759 | 400k | no | no |
| Argosaronic islands (Aegina, Hydra, Spetses, Poros, Salamina) | איי הים הסרוני | 2,900 | +10.9% | 7.82 | +1.8% | 3.2% | IND 2026-09 | SPI 2,366 | 800k | no | no |
| Sporades (Skiathos, Skopelos, Alonnisos) | ספוראדס | 2,872 | +6.1% |  |  |  | IND 2026-09 | SPI 2,647 | mixed | no | no |
| Kefalonia (regional unit, incl. Ithaca) | מחוז קפלוניה | 2,717 | +5.7% | 8.15 | -4.8% | 3.6% | IND 2026-09 | SPI 2,531 | mixed | no | no |
| Dodecanese | הדודקנסוס | 2,696 | +14.1% | 9.94 | +4.0% | 4.4% | IND 2026-09 | SPI 2,219 | mixed | yes | no |
| Lasithi (Agios Nikolaos, Elounda) | לסיתי | 2,678 | -5.7% | 8.25 | +17.7% | 3.7% | IND 2026-09 | SPI 1,944; ISL 1,944 | 800k | no | no |
| Argolida (Nafplio, Porto Heli) | ארגוליס | 2,441 | +3.2% | 8.09 | +2.8% | 4.0% | IND 2026-09 | SPI 2,111 | 400k | no | no |
| Thessaloniki (regional unit) | מחוז סלוניקי | 2,413 | +5.3% | 9.28 | +6.1% | 4.6% | IND 2026-09 |  | 800k | no | no |
| Rethymno (regional unit, Crete) | מחוז רתימנו | 2,410 | +8.6% | 9.49 | -1.0% | 4.7% | IND 2026-09 | SPI 2,202; ISL 2,202 | 800k | no | no |
| Messinia (Kalamata, Pylos) | מסיניה | 2,261 | +7.0% | 8.71 | +10.7% | 4.6% | IND 2026-09 | SPI 2,008 | 400k | no | no |
| Heraklion (regional unit, Crete) | מחוז הרקליון | 2,150 | +7.0% | 9.82 | +8.4% | 5.5% | IND 2026-09 | SPI 1,917; ISL 2,200 | 800k | no | no |
| Kavala (regional unit, incl. Thassos) | מחוז קוואלה | 2,090 | +9.3% | 6.48 | +7.5% | 3.7% | IND 2026-09 | SPI 2,222 | mixed | no | no |
| Preveza (Parga) | פרבזה | 2,029 | +3.3% | 6.86 | +14.9% | 4.1% | IND 2026-09 | SPI 2,011 | 400k | yes | no |
| Thesprotia (Igoumenitsa, Syvota) | תספרוטיה | 1,947 | +4.7% | 6.18 | -1.3% | 3.8% | IND 2026-09 | SPI 1,875 | 400k | yes | no |
| Corinthia (Corinth, Loutraki) | קורינתיה | 1,842 | +7.2% | 7.78 | +7.8% | 5.1% | IND 2026-09 | SPI 1,700 | 400k | no | no |
| Evros (Alexandroupoli) | אברוס | 1,770 | +8.5% | 8.9 | +9.3% | 6.0% | IND 2026-09 | SPI 1,800 | 400k | yes | no |
| Ioannina (regional unit) | מחוז יואנינה | 1,687 | +6.0% | 8.23 | +2.2% | 5.9% | IND 2026-09 | SPI 1,596 | 400k | partial | no |
| Evia (Euboea) | אוויה | 1,675 | +8.1% | 8.04 | +10.1% | 5.8% | IND 2026-09 | SPI 1,538 | mixed | partial | no |
| Lakonia (Sparti, Monemvasia) | לקוניה | 1,623 | +2.1% | 6.82 | +8.4% | 5.0% | IND 2026-09 | SPI 1,359 | 400k | no | no |
| Achaia (Patras) | אכאיה | 1,621 | +7.5% | 8.36 | +4.0% | 6.2% | IND 2026-09 | SPI 1,485 | 400k | no | no |
| Magnesia (Volos, Pelion) | מגנסיה | 1,600 | +11.0% | 7.81 | +2.5% | 5.9% | IND 2026-09 | SPI 1,472 | 400k | no | no |
| Fokida (Amfissa, Galaxidi) | פוקידה | 1,566 | +2.5% | 6.29 | +24.6% | 4.8% | IND 2026-09 | SPI 1,500 | 400k | no | no |
| Arkadia (Tripoli) | ארקדיה | 1,477 | +5.2% | 6.67 | +2.5% | 5.4% | IND 2026-09 | SPI 1,207 | 400k | no | no |
| Viotia (Livadeia, Thiva) | בויאוטיה | 1,454 | +8.8% | 5.88 | +7.9% | 4.9% | IND 2026-09 | SPI 1,400 | 400k | no | no |
| Larissa (regional unit) | מחוז לריסה | 1,422 | +16.8% | 7.73 | +6.6% | 6.5% | IND 2026-09 | SPI 1,349 | 400k | no | no |
| Pieria (Katerini) | פיאריה | 1,363 | +5.7% | 6.53 | +12.0% | 5.8% | IND 2026-09 | SPI 1,235 | 400k | no | no |
| Evrytania (Karpenisi) | אבריטניה | 1,264 | +3.0% | 5.44 | +4.4% | 5.2% | IND 2026-09 | SPI 1,111 | 400k | no | no |
| Xanthi (regional unit) | מחוז קסנתי | 1,243 | +7.5% | 5.89 | +6.1% | 5.7% | IND 2026-09 | SPI 1,214 | 400k | yes | no |
| Aitoloakarnania (Agrinio, Mesolongi) | אטוליה-אקרנניה | 1,228 | +10.6% | 5.89 | +9.1% | 5.8% | IND 2026-09 | SPI 1,031 | 400k | no | no |
| Rodopi (Komotini) | רודופי | 1,220 | +5.7% | 5.77 | +1.4% | 5.7% | IND 2026-09 | SPI 1,190 | 400k | yes | no |
| Fthiotida (Lamia) | פתיוטידה | 1,167 | -1.5% | 5.96 | +8.2% | 6.1% | IND 2026-09 | SPI 1,071 | 400k | no | no |
| Trikala (regional unit, Meteora) | מחוז טריקלה | 1,154 | +7.7% | 6.87 | +5.4% | 7.1% | IND 2026-09 | SPI 1,028 | 400k | no | no |
| Ilia (Pyrgos) | איליה | 1,013 | +0.8% | 5.54 | +4.5% | 6.6% | IND 2026-09 | SPI 940 | 400k | no | no |
| Serres (regional unit) | מחוז סרס | 963 | +8.0% | 5.15 | +2.4% | 6.4% | IND 2026-09 | SPI 909 | 400k | partial | no |
| Arta | ארטה | 924 | +1.7% | 6.55 | +2.7% | 8.5% | IND 2026-09 | SPI 893 | 400k | no | no |
| Imathia (Veria) | אימתיה | 903 | +5.7% | 4.52 | +0.7% | 6.0% | IND 2026-09 | SPI 825 | 400k | no | no |
| Pella (Edessa, Giannitsa) | פלה | 891 | +3.6% | 4.51 | +3.9% | 6.1% | IND 2026-09 | SPI 864 | 400k | partial | no |
| Drama | מחוז דרמה | 886 | +2.5% | 5.05 | +3.7% | 6.8% | IND 2026-09 | SPI 843 | 400k | partial | no |
| Karditsa | קרדיצה | 875 | +0.9% | 6.36 | +1.0% | 8.7% | IND 2026-09 | SQ3 806; SPI 741 | 400k | no | no |
| Kilkis | קילקיס | 772 | +9.0% | 4.65 | +11.2% | 7.2% | IND 2026-09 | SQ3 700; SPI 707 | 400k | yes | no |
| Kozani (regional unit) | מחוז קוזאני | 741 | +3.9% | 4.59 | -1.1% | 7.4% | IND 2026-09 | SQ3 667; SPI 682 | 400k | no | no |
| Grevena | גרבנה | 730 | -6.4% | 4.49 | +1.6% | 7.4% | IND 2026-09 | SPI 850 | 400k | no | no |
| Kastoria | קסטוריה | 690 | +7.6% | 5 | +8.0% | 8.7% | IND 2026-09 | SQ3 577; SPI 585 | 400k | yes | no |
| Florina | פלורינה | 662 | +2.6% | 5.34 | -4.6% | 9.7% | IND 2026-09 | SQ3 690; SPI 673 | 400k | yes | no |

Notes: **Cyclades:** Border permit needed on Santorini (Thira) only. GV: Mykonos, Santorini and islands above 3,100 inhabitants EUR 800k; smaller islands EUR 400k. **Corfu (regional unit, incl. Paxoi):** Border-zone list covers the Diapontia islands only (not Corfu main island). **Halkidiki:** Spitogatos SPI Q2 2026 rent 21.11 (Q2 2025 32.14, -34.3%) looks like small-sample volatility; not used. **Sporades (Skiathos, Skopelos, Alonnisos):** Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 3.15 EUR/m2, yoy -0.513). **Dodecanese:** Entire Dodecanese is a border zone (non-EU buyers need a permit). **Kavala (regional unit, incl. Thassos):** Thassos (island, >3,100 inhabitants) EUR 800k; mainland Kavala EUR 400k. **Evia (Euboea):** Evia island is above 3,100 inhabitants (EUR 800k likely applies on the island; verify); Skyros (border zone) is in this unit.

## Attica: sub-areas (8)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Athens South suburbs (Riviera) | הפרברים הדרומיים של אתונה (הריביירה) | 4,231 | +3.4% | 14.05 | +2.0% | 4.0% | IND 2026-09 | SQ3 4,257; SPI 4,231 | 800k | no | no |
| Athens North suburbs | הפרברים הצפוניים של אתונה | 3,713 | +5.5% | 12.85 | +2.3% | 4.2% | IND 2026-09 | SQ3 3,505; SPI 3,519 | 800k | no | no |
| Athens Centre (Municipality of Athens) | מרכז אתונה (עיריית אתונה) | 2,844 | +5.9% | 12.51 | +5.0% | 5.3% | IND 2026-09 | SPI 2,500; XE 3,029; NUM 3,616 | 800k | no | partial |
| Piraeus (municipality) | פיראוס | 2,709 | +5.4% | 10.96 | +5.3% | 4.9% | IND 2026-09 | SPI 2,606; XE 3,053 | 800k | no | no |
| Athens East suburbs (Mesogeia) | הפרברים המזרחיים של אתונה | 2,505 | +7.5% | 9.54 | +5.2% | 4.6% | IND 2026-09 | SPI 2,500 | 800k | no | no |
| Athens West suburbs | הפרברים המערביים של אתונה | 2,347 | +8.4% | 9.19 | +7.1% | 4.7% | IND 2026-09 | SPI 2,288 | 800k | no | no |
| Piraeus suburbs | פרברי פיראוס | 2,314 | +7.4% | 9.35 | +11.3% | 4.9% | IND 2026-09 | SPI 2,253 | 800k | no | no |
| Rest of Attica (East + West Attica) | שאר אטיקה (מזרח ומערב) | 2,287 | +1.9% | 10.06 | +1.8% | 5.3% | IND 2026-09 | SPI 2,105 | 800k | no | no |

Notes: **Athens Centre (Municipality of Athens):** STR freeze applies only in Athens municipal districts 1-3.

## Athens: neighbourhoods inside the Municipality of Athens (21)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Plaka | פלאקה | 6,116 | +7.4% | 17.33 | -5.6% | 3.4% | IND 2026-09 |  | 800k | no | yes |
| Syntagma | סינטגמה | 6,067 |  | 17.67 |  | 3.5% | IND 2026-09 |  | 800k | no | yes |
| Kolonaki - Lykavittos | קולונקי | 5,516 | +2.6% | 18.83 | +4.6% | 4.1% | IND 2026-09 |  | 800k | no | yes |
| Akropoli (Makrygianni side) | אקרופולי | 5,462 | +3.5% | 15.82 | +3.0% | 3.5% | IND 2026-09 |  | 800k | no | yes |
| Thiseio | תיסיו | 5,168 | +18.4% | 14.39 | +3.7% | 3.3% | IND 2026-09 |  | 800k | no | yes |
| Athens Historic Centre | המרכז ההיסטורי של אתונה | 5,159 | +6.9% | 16.01 | -0.1% | 3.7% | IND 2026-09 |  | 800k | no | yes |
| Monastiraki | מונסטירקי | 4,545 | +3.6% | 17.78 | -4.3% | 4.7% | IND 2026-09 |  | 800k | no | yes |
| Mets - Kallimarmaro | מטס | 4,348 | +5.0% | 15.18 | +2.7% | 4.2% | IND 2026-09 |  | 800k | no | yes |
| Psyrri | פסירי | 3,859 |  | 17.69 |  | 5.5% | IND 2026-09 |  | 800k | no | yes |
| Koukaki - Makrygianni | קוקאקי | 3,847 | -0.2% | 14.92 | +8.0% | 4.7% | IND 2026-09 |  | 800k | no | yes |
| Pangrati | פנגרטי | 3,573 | +5.0% | 12.44 | +5.2% | 4.2% | IND 2026-09 |  | 800k | no | yes |
| Athens commercial centre (Syntagma-Omonoia) | מרכז העסקים של אתונה (סינטגמה-אומוניה) | 3,420 | +5.8% | 14.8 | +5.7% | 5.2% | IND 2026-09 |  | 800k | no | yes |
| Ilisia | איליסיה | 3,361 | +3.4% | 12.72 | +2.2% | 4.5% | IND 2026-09 |  | 800k | no | yes |
| Neos Kosmos | נאוס קוסמוס | 3,346 | +10.5% | 11.86 | +4.9% | 4.2% | IND 2026-09 |  | 800k | no | yes |
| Ampelokipoi - Pentagon | אמפלוקיפי | 3,168 | +8.5% | 12.13 | +5.7% | 4.6% | IND 2026-09 |  | 800k | no | no |
| Exarcheia - Neapoli | אקסרכיה | 2,941 | +7.7% | 11.99 | +7.8% | 4.9% | IND 2026-09 |  | 800k | no | yes |
| Petralona | פטרלונה | 2,903 | +5.1% | 11.77 | -0.4% | 4.9% | IND 2026-09 |  | 800k | no | yes |
| Gazi - Metaxourgeio - Votanikos | גאזי - מטקסורגיו | 2,814 | +17.3% | 11.69 | +6.4% | 5.0% | IND 2026-09 |  | 800k | no | yes |
| Gyzi - Pedion Areos | גיזי - פדיון אראוס | 2,631 | +4.3% | 10.85 | +4.9% | 5.0% | IND 2026-09 |  | 800k | no | no |
| Kypseli | קיפסלי | 2,183 | +5.2% | 9.88 | +4.1% | 5.4% | IND 2026-09 |  | 800k | no | no |
| Patisia | פטיסיה | 1,777 | +5.2% | 9.44 | +1.5% | 6.4% | IND 2026-09 | SQ3 1,739 | 800k | no | no |

## Attica: municipalities and Piraeus districts (63)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Vouliagmeni | ווליאגמני | 7,710 | +0.5% | 22.1 | +2.7% | 3.4% | IND 2026-09 | SQ3 7,442; SQ2 7,364 | 800k | no | no |
| Voula | וולה | 6,198 | +4.0% | 17.51 | +4.5% | 3.4% | IND 2026-09 | SQ3 6,389; SQ2 6,250; XE 6,766 | 800k | no | no |
| Elliniko (Ellinikon) | אליניקו | 5,745 | +7.3% | 15.31 | +0.5% | 3.2% | IND 2026-09 | SQ3 5,849; SQ2 5,688; XE 6,113 | 800k | no | no |
| Palaio Psychiko | פליאו פסיכיקו | 5,510 | +4.4% | 17.67 | +3.7% | 3.9% | IND 2026-09 | SQ3 5,603; SQ2 5,182 | 800k | no | no |
| Glyfada | גליפדה | 5,388 | +3.3% | 17.17 | +4.3% | 3.8% | IND 2026-09 | SQ3 5,758; SQ2 5,669; XE 6,136 | 800k | no | no |
| Filothei | פילותאי | 4,927 | -0.1% | 16.58 | +10.8% | 4.0% | IND 2026-09 |  | 800k | no | no |
| Alimos | אלימוס | 4,821 | +1.6% | 13.74 | +3.6% | 3.4% | IND 2026-09 | XE 5,275 | 800k | no | no |
| Vari - Varkiza | וארי - ורקיזה | 4,706 | +1.9% | 16.66 | +2.0% | 4.2% | IND 2026-09 | XE 5,020 | 800k | no | no |
| Vrilissia | ורליסיה | 4,331 | +11.8% | 12.13 | +7.3% | 3.4% | XE 2026-Q3 |  | 800k | no | no |
| Kifisia | קיפיסיה | 4,231 | +7.8% | 13.71 | +4.7% | 3.9% | IND 2026-09 | XE 4,467 | 800k | no | no |
| Neo Psychiko | נאו פסיכיקו | 4,217 | +12.7% | 13.91 | +11.5% | 4.0% | IND 2026-09 |  | 800k | no | no |
| Argyroupoli | ארגירופולי | 4,078 | +16.2% | 11.01 | +4.1% | 3.2% | IND 2026-09 | XE 4,371 | 800k | no | no |
| Palaio Faliro | פליאו פלירו | 4,076 | +2.8% | 12.54 | +4.9% | 3.7% | IND 2026-09 | XE 4,284 | 800k | no | no |
| Cholargos | חולרגוס | 4,034 | +7.3% | 12.08 | +6.4% | 3.6% | XE 2026-Q3 |  | 800k | no | no |
| Agia Paraskevi | אגיה פרסקבי | 3,907 | +5.3% | 12.06 | +2.0% | 3.7% | XE 2026-Q3 |  | 800k | no | no |
| Marousi | מרוסי | 3,805 | +8.5% | 14.16 | -1.5% | 4.5% | IND 2026-09 | XE 3,886 | 800k | no | no |
| Melissia | מליסיה | 3,797 | +5.9% | 10.91 | +0.5% | 3.5% | XE 2026-Q3 |  | 800k | no | no |
| Ekali | אקאלי | 3,565 | +6.6% | 11.4 | -0.3% | 3.8% | IND 2026-09 |  | 800k | no | no |
| Chalandri | חלנדרי | 3,551 | +1.7% | 13.35 | +4.4% | 4.5% | IND 2026-09 | XE 3,753 | 800k | no | no |
| Ilioupoli | איליופולי | 3,532 | +5.9% | 10.03 | +2.2% | 3.4% | IND 2026-09 | XE 3,767 | 800k | no | no |
| Nea Smyrni | ניאה סמירני | 3,515 | +5.3% | 11.09 | +1.6% | 3.8% | IND 2026-09 | XE 3,530 | 800k | no | no |
| Saronida | סרונידה | 3,446 | +0.2% | 11.65 | +4.0% | 4.1% | IND 2026-09 | XE 3,659; HOL 3,200 | 800k | no | no |
| Agios Dimitrios | אגיוס דימיטריוס | 3,406 | +8.4% | 10.67 | +11.1% | 3.8% | IND 2026-09 | XE 3,709 | 800k | no | no |
| Nea Erythraia | ניאה אריתראה | 3,314 | -0.1% | 11.94 | -2.7% | 4.3% | IND 2026-09 | XE 3,453 | 800k | no | no |
| Dafni | דפני | 3,130 | +12.5% | 10.23 | +1.7% | 3.9% | IND 2026-09 | SQ3 3,571; SQ2 3,500; XE 3,469 | 800k | no | no |
| Kaisariani | קייסריאני | 3,120 | -1.4% | 12.19 | +10.2% | 4.7% | IND 2026-09 | XE 3,215 | 800k | no | no |
| Gerakas | גרקס | 3,119 | +11.4% | 10.52 | +10.9% | 4.0% | IND 2026-09 | XE 3,242 | 800k | no | no |
| Moschato | מוסחטו | 3,107 | +8.2% | 11.11 | +16.5% | 4.3% | IND 2026-09 | XE 3,739 | 800k | no | no |
| Kastella - Passalimani (Piraeus) | קסטלה - פסלימני (פיראוס) | 3,079 | +4.9% | 11.13 | +4.2% | 4.3% | IND 2026-09 |  | 800k | no | no |
| Anavyssos | אנביסוס | 3,067 | +0.2% | 11.28 | -2.3% | 4.4% | IND 2026-09 | HOL 2,941 | 800k | no | no |
| Kallithea | קליתאה | 3,012 | +5.8% | 10.88 | +8.0% | 4.3% | IND 2026-09 | XE 3,320 | 800k | no | no |
| Neo Faliro (Piraeus) | נאו פלירו (פיראוס) | 2,925 | +4.2% | 11.24 | +8.9% | 4.6% | IND 2026-09 |  | 800k | no | no |
| Zografou | זוגרפו | 2,884 | +5.3% | 10.8 | +2.0% | 4.5% | IND 2026-09 | XE 2,921 | 800k | no | no |
| Vyronas | וירונס | 2,821 | +3.3% | 10.88 | +8.7% | 4.6% | IND 2026-09 | XE 2,989 | 800k | no | no |
| Galatsi | גלאצי | 2,804 | +3.6% | 9.44 | +6.2% | 4.0% | IND 2026-09 | XE 2,953 | 800k | no | no |
| Petroupoli | פטרופולי | 2,781 | +7.3% | 9.52 | +13.2% | 4.1% | IND 2026-09 | XE 2,907 | 800k | no | no |
| Porto Rafti | פורטו רפטי | 2,745 | +7.6% | 12.64 | +11.2% | 5.5% | XE 2026-Q3 | HOL 2,667 | 800k | no | no |
| Glyka Nera | גליקה נרה | 2,716 | +6.8% | 9 | +2.4% | 4.0% | IND 2026-09 |  | 800k | no | no |
| Pallini (Attica) | פליני (אטיקה) | 2,705 | +4.4% | 9.19 | +2.9% | 4.1% | IND 2026-09 | XE 2,920 | 800k | no | no |
| Palaia Fokaia | פליאה פוקאיה | 2,701 | +5.1% | 11.79 | -9.8% | 5.2% | IND 2026-09 | HOL 2,556 | 800k | no | no |
| Nea Ionia | ניאה יוניה | 2,696 | +8.5% | 10.1 | +9.2% | 4.5% | IND 2026-09 | SQ3 3,012; XE 3,165 | 800k | no | no |
| Rafina | רפינה | 2,622 | +0.9% | 9.59 | +1.6% | 4.4% | IND 2026-09 | HOL 2,500 | 800k | no | no |
| Markopoulo Mesogaias | מרקופולו | 2,574 | +13.3% | 10.35 | +6.8% | 4.8% | IND 2026-09 |  | 800k | no | no |
| Kalyvia Thorikou | קליוויה תוריקו | 2,546 | -2.3% | 11.41 | +6.4% | 5.4% | IND 2026-09 | XE 2,789 | 800k | no | no |
| Koropi | קורופי | 2,424 | +3.6% | 9.59 | +3.7% | 4.8% | IND 2026-09 | XE 2,443 | 800k | no | no |
| Peristeri | פריסטרי | 2,396 | +12.1% | 9.33 | +3.8% | 4.7% | IND 2026-09 | XE 2,754 | 800k | no | no |
| Ilion | איליון | 2,359 | +12.1% | 8.34 | +5.8% | 4.2% | IND 2026-09 | XE 2,465 | 800k | no | no |
| Chaidari | חיידרי | 2,336 | +5.2% | 9.24 | +3.6% | 4.8% | IND 2026-09 | XE 2,508 | 800k | no | no |
| Korydallos | קורידלוס | 2,334 | +11.4% | 9.28 | +10.3% | 4.8% | IND 2026-09 | XE 2,514 | 800k | no | no |
| Aigaleo | אגלאו | 2,315 | +13.2% | 10.39 | +9.6% | 5.4% | IND 2026-09 | XE 2,589 | 800k | no | no |
| Nea Makri | ניאה מקרי | 2,234 | +2.3% | 9.12 |  | 4.9% | IND 2026-09 | HOL 2,276 | 800k | no | no |
| Nikaia | ניקאיה | 2,219 | +4.2% | 9.3 | +10.8% | 5.0% | IND 2026-09 | XE 2,432 | 800k | no | no |
| Nea Filadelfeia | ניאה פילדלפיה | 2,157 | +12.9% | 8.76 | +9.6% | 4.9% | IND 2026-09 | SQ3 2,193; SQ2 2,128 | 800k | no | no |
| Keratsini | קרצ'יני | 2,078 | +9.4% | 8.9 | +12.4% | 5.1% | IND 2026-09 | XE 2,230 | 800k | no | no |
| Marathon | מרתון | 2,049 | -4.7% | 8.73 | +1.0% | 5.1% | IND 2026-09 | HOL 2,013 | 800k | no | no |
| Lagonisi | לגוניסי | 2,000 |  |  |  |  | RMX 2025 |  | 800k | no | no |
| Keratea | קרטאה | 1,979 | +1.8% | 8.71 | +6.2% | 5.3% | IND 2026-09 | HOL 1,875 | 800k | no | no |
| Lavrio | לבריו | 1,974 | -3.2% | 10.06 | -30.8% | 6.1% | IND 2026-09 |  | 800k | no | no |
| Artemida (Loutsa) | ארטמידה (לוצה) | 1,950 | +5.7% | 9.95 | +7.1% | 6.1% | IND 2026-09 | XE 2,106; HOL 1,862 | 800k | no | no |
| Perama | פרמה | 1,785 | -4.0% | 7.93 | +10.4% | 5.3% | IND 2026-09 | SQ3 1,731 | 800k | no | no |
| Megara | מגרה | 1,752 | +4.4% | 8.42 | +9.1% | 5.8% | IND 2026-09 |  | 800k | no | no |
| Acharnes | אחרנס | 1,708 | +6.7% | 7.61 | +11.6% | 5.3% | IND 2026-09 | SQ3 1,680; XE 1,907 | 800k | no | no |
| Agia Varvara | אגיה ורורה | 1,575 | +5.4% | 8.28 | +2.6% | 6.3% | IND 2026-09 | SQ3 1,500 | 800k | no | no |

## Thessaloniki: city, neighbourhoods and suburbs (23)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Kalamaria | קלמריה | 3,142 | +7.9% | 9.56 | +5.6% | 3.6% | IND 2026-09 | SQ3 3,243; SQ2 3,175; XE 3,220 | 800k | no | no |
| Thessaloniki Centre | מרכז סלוניקי | 3,090 | +2.6% | 11.22 | +7.2% | 4.4% | IND 2026-09 | SQ3 3,075; SQ2 3,056 | 800k | no | yes |
| Pylaia | פילאיה | 2,862 | +5.2% | 8.78 | +4.3% | 3.7% | IND 2026-09 | SQ3 2,962; SQ2 2,962 | 800k | no | no |
| Analipsi - Botsari - Nea Paralia | אנאליפסי - נאה פרליה | 2,799 | +6.0% | 9.36 | -0.6% | 4.0% | IND 2026-09 |  | 800k | no | no |
| Panorama | פנורמה | 2,714 | +5.6% | 9 | +11.5% | 4.0% | IND 2026-09 |  | 800k | no | no |
| Thessaloniki (municipality) | סלוניקי (העירייה) | 2,696 | +3.5% | 9.91 | +6.6% | 4.4% | IND 2026-09 | SPI 2,714; XE 2,838; NUM 3,303 | 800k | no | partial |
| Thermi | תרמי | 2,655 | +7.4% | 8.91 | +4.0% | 4.0% | IND 2026-09 |  | 800k | no | no |
| Charilaou | חרילאו | 2,647 | +6.0% | 8.67 | +4.2% | 3.9% | IND 2026-09 | SQ3 3,000; SQ2 2,857 | 800k | no | no |
| Toumba | טומבה | 2,581 | +0.2% | 8.71 | +7.4% | 4.0% | IND 2026-09 | SQ3 2,870; SQ2 2,850 | 800k | no | no |
| 40 Ekklisies - Evangelistria | 40 אקליסייס | 2,552 | +8.8% | 9.28 | +6.4% | 4.4% | IND 2026-09 |  | 800k | no | no |
| Peraia (Thermaikos) | פראיה (תרמאיקוס) | 2,352 | +12.5% | 8.28 | +8.4% | 4.2% | IND 2026-09 | RMX 1,400 | 800k | no | no |
| Thessaloniki suburbs | פרברי סלוניקי | 2,230 | +10.3% | 8.04 | +6.3% | 4.3% | IND 2026-09 | SPI 2,121 | 800k | no | no |
| Vardaris - Lachanokipoi | ורדריס | 2,211 | +9.3% | 9.74 | +8.5% | 5.3% | IND 2026-09 |  | 800k | no | no |
| Ano Poli | אנו פולי | 2,143 | +3.2% | 9.35 | +8.5% | 5.2% | IND 2026-09 |  | 800k | no | no |
| Evosmos | אבוסמוס | 1,971 | +10.4% | 7.25 | +4.5% | 4.4% | IND 2026-09 |  | 800k | no | no |
| Oraiokastro | אוראיוקסטרו | 1,935 | +17.5% | 6.31 | +8.2% | 3.9% | IND 2026-09 |  | 800k | no | no |
| Stavroupoli | סטברופולי | 1,783 | +21.2% | 6.99 | +2.2% | 4.7% | IND 2026-09 |  | 800k | no | no |
| Sykies (Neapoli-Sykies) | סיקייס | 1,741 | +2.7% | 7.56 | +12.7% | 5.2% | IND 2026-09 |  | 800k | no | no |
| Menemeni | מנמני | 1,516 | +5.6% | 6.95 | +12.6% | 5.5% | IND 2026-09 |  | 800k | no | no |
| Neapoli (Neapoli-Sykies) | ניאפולי | 1,515 | +9.9% | 7.54 | +8.8% | 6.0% | IND 2026-09 |  | 800k | no | no |
| Ampelokipoi (Thessaloniki) | אמפלוקיפי (סלוניקי) | 1,482 | +10.8% | 7.63 | +20.3% | 6.2% | IND 2026-09 |  | 800k | no | no |
| Epanomi | אפנומי | 1,444 | +7.9% | 7 | +8.9% | 5.8% | IND 2026-09 |  | 800k | no | no |
| Rest of Thessaloniki prefecture | שאר מחוז סלוניקי | 1,352 | +17.1% | 4.55 | +17.6% | 4.0% | IND 2026-09 | SPI 1,211 | 800k | no | no |

Notes: **Thessaloniki (municipality):** STR freeze applies in the 1st Municipal Community (historic and commercial centre) only. **Peraia (Thermaikos):** Peraia has no figure of its own; Indomio publishes it inside Thermaikos municipality. **Oraiokastro:** Spitogatos Q3 2026: sale asking price +27.2% yoy (level not published). **Menemeni:** Spitogatos Q3 2026: rent +22.6% yoy (level not published). **Epanomi:** Spitogatos Q3 2026: rent +30.5% yoy (level not published).

## Cities (25)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Agios Nikolaos (incl. Elounda) | אגיוס ניקולאוס (כולל אלונדה) | 3,901 | -2.2% | 9.71 | +29.8% | 3.0% | IND 2026-09 |  | 800k | no | no |
| Chania (city) | חאניה | 3,704 | +4.4% | 11.39 | +5.2% | 3.7% | IND 2026-09 | NUM 3,693 | 800k | no | no |
| Rethymno (town) | רתימנו | 3,008 | +7.1% | 10.52 | +5.8% | 4.2% | IND 2026-09 |  | 800k | no | no |
| Nafplio | נפפליו | 2,850 | +8.9% | 9.19 | +4.0% | 3.9% | IND 2026-09 | HOL 2,778 | 400k | no | no |
| Kalamata | קלמטה | 2,688 | +9.1% | 9.43 | +10.2% | 4.2% | IND 2026-09 | HOL 2,892 | 400k | no | no |
| Hersonissos | חרסוניסוס | 2,552 | +10.0% | 9.86 | +0.9% | 4.6% | IND 2026-09 |  | 800k | no | no |
| Heraklion (city) | הרקליון | 2,351 | +9.7% | 10.14 | +10.3% | 5.2% | IND 2026-09 | XE 2,813; NUM 3,197 | 800k | no | no |
| Loutraki - Perachora | לוטרקי | 2,328 | +10.2% | 9.2 | +9.1% | 4.7% | IND 2026-09 | HOL 2,619 | 400k | no | no |
| Alexandroupoli | אלכסנדרופוליס | 2,052 | +7.2% | 9.61 | +8.3% | 5.6% | IND 2026-09 | NG 2,000 | 400k | yes | no |
| Kavala (city) | קוואלה | 2,042 | +11.6% | 6.74 | +5.3% | 4.0% | IND 2026-09 | HOL 2,286; NG 1,993 | 400k | no | no |
| Ioannina (city) | יואנינה | 1,950 | +7.5% | 8.39 | +2.2% | 5.2% | IND 2026-09 | EPI 1,739 | 400k | check | no |
| Chalkida | חלקיס | 1,827 | +13.3% | 8.8 | +12.8% | 5.8% | IND 2026-09 |  | check | no | no |
| Volos | וולוס | 1,779 | +13.0% | 8.07 | +3.2% | 5.4% | IND 2026-09 | THS 1,577 | 400k | no | no |
| Patras | פטרה | 1,758 | +8.0% | 8.49 | +3.5% | 5.8% | IND 2026-09 | XE 1,885; NUM 1,826 | 400k | no | no |
| Corinth (Korinthos) | קורינתוס | 1,678 | +9.0% | 7.14 | -0.7% | 5.1% | IND 2026-09 |  | 400k | no | no |
| Larissa (city) | לריסה | 1,673 | +18.0% | 7.87 | +6.9% | 5.6% | IND 2026-09 | THS 1,598 | 400k | no | no |
| Komotini | קומוטיני | 1,300 |  | 7.6 |  | 7.0% | NG 2026-Q1 |  | 400k | yes | no |
| Xanthi (city) | קסנתי | 1,282 |  | 7.3 |  | 6.8% | NG 2026-Q1 |  | 400k | yes | no |
| Trikala (city) | טריקלה | 1,138 |  |  |  |  | THS 2025-Q3 |  | 400k | no | no |
| Katerini | קטריני | 1,108 |  | 6.2 |  | 6.7% | NG 2026-Q1 |  | 400k | no | no |
| Serres (city) | סרס | 1,085 | +0.9% | 5.25 | +3.3% | 5.8% | IND 2026-09 | NG 1,047 | 400k | check | no |
| Veria | ורויה | 1,000 |  | 5 |  | 6.0% | NG 2026-Q1 |  | 400k | no | no |
| Drama (city) | דרמה | 1,000 |  | 5.8 |  | 7.0% | NG 2026-Q1 |  | 400k | check | no |
| Lamia | למיה | 876 | -0.8% | 5.85 | +9.6% | 8.0% | IND 2026-09 |  | 400k | no | no |
| Kozani (city) | קוזאני | 838 |  | 5.9 |  | 8.5% | NG 2026-Q1 |  | 400k | no | no |

Notes: **Agios Nikolaos (incl. Elounda):** Elounda belongs to the Agios Nikolaos municipality; no Elounda-only price is published. **Ioannina (city):** Lies in a regional unit only partly in the border zone; the city itself was not verified as inside or outside it. **Chalkida:** Chalkida is on Evia island (>3,100 inhabitants): EUR 800k likely applies; verify before relying on it. **Serres (city):** Lies in a regional unit only partly in the border zone; the city itself was not verified as inside or outside it. **Drama (city):** Lies in a regional unit only partly in the border zone; the city itself was not verified as inside or outside it.

## Islands (45)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Mykonos | מיקונוס | 7,633 | +0.1% | 19.43 | -5.0% | 3.0% | IND 2026-09 | ISL 7,059 | 800k | no | no |
| Antiparos | אנטיפארוס | 7,420 | +14.5% |  |  |  | IND 2026-09 | ISL 7,600 | 400k | no | no |
| Hydra | הידרה | 7,188 | +7.0% |  |  |  | IND 2026-09 |  | 800k | no | no |
| Meganisi | מגניסי | 6,303 | +11.3% |  |  |  | IND 2026-09 |  | 400k | no | no |
| Paros | פארוס | 5,656 | +5.5% | 14.86 | +3.6% | 3.1% | IND 2026-09 | ISL 5,263 | 800k | no | no |
| Paxoi | פקסוס | 5,495 | +5.1% |  |  |  | IND 2026-09 | ISL 3,846 | 400k | no | no |
| Spetses | ספצס | 5,495 | +16.4% |  |  |  | IND 2026-09 | HOL 4,615 | 800k | no | no |
| Patmos | פטמוס | 4,694 | +11.7% |  |  |  | IND 2026-09 | ISL 5,000 | check | yes | no |
| Santorini (Thira) | סנטוריני | 4,537 | -1.6% | 13.37 | -16.6% | 3.5% | IND 2026-09 | ISL 4,096 | 800k | yes | no |
| Folegandros | פולגנדרוס | 4,462 | -1.0% |  |  |  | IND 2026-09 | ISL 4,746 | 400k | no | no |
| Kythnos | קיתנוס | 4,368 | +6.6% |  |  |  | IND 2026-09 | ISL 4,583 | 400k | no | no |
| Milos | מילוס | 4,336 | +19.4% |  |  |  | IND 2026-09 | ISL 3,695 | 800k | no | no |
| Skiathos | סקיאתוס | 3,946 | +10.0% |  |  |  | IND 2026-09 | ISL 3,521 | 800k | no | no |
| Ios | איוס | 3,872 | +1.1% |  |  |  | IND 2026-09 | ISL 4,167 | 400k | no | no |
| Lefkada | לפקדה | 3,816 | +1.8% | 10.55 | +12.7% | 3.3% | IND 2026-09 | SQ3 3,500; SPI 3,302; ISL 3,302 | 800k | no | no |
| Sifnos | סיפנוס | 3,798 | -5.1% |  |  |  | IND 2026-09 | ISL 3,846 | 400k | no | no |
| Naxos | נקסוס | 3,697 | -2.0% | 9.39 | +12.1% | 3.0% | IND 2026-09 | ISL 3,846 | 800k | no | no |
| Serifos | סריפוס | 3,674 | +1.8% |  |  |  | IND 2026-09 | ISL 4,154 | 400k | no | no |
| Kea (Tzia) | קאה (צ'יה) | 3,607 | +6.5% | 10.89 | -1.0% | 3.6% | IND 2026-09 | ISL 3,333 | 400k | no | no |
| Astypalaia | אסטיפליאה | 3,490 | +10.8% |  |  |  | IND 2026-09 | ISL 4,000 | 400k | yes | no |
| Poros | פורוס | 3,120 | +13.0% | 8.41 | +15.5% | 3.2% | IND 2026-09 | HOL 3,207 | 800k | no | no |
| Tinos | טינוס | 3,098 | +6.8% | 8.56 | +9.5% | 3.3% | IND 2026-09 | ISL 3,004 | 800k | no | no |
| Ithaca | איתקה | 3,079 | +5.2% |  |  |  | IND 2026-09 | ISL 2,455 | check | no | no |
| Corfu | קורפו | 2,993 | +11.6% | 9.98 | -0.4% | 4.0% | IND 2026-09 | ISL 2,417 | 800k | no | no |
| Zakynthos | זקינתוס | 2,895 | +0.3% | 7.93 | +6.3% | 3.3% | IND 2026-09 | SPI 2,300; ISL 2,300 | 800k | no | no |
| Symi | סימי | 2,843 | -3.0% |  |  |  | IND 2026-09 | ISL 2,157 | 400k | yes | no |
| Aegina | אגינה | 2,723 | +8.5% | 9.19 | -8.6% | 4.0% | IND 2026-09 | HOL 2,692 | 800k | no | no |
| Kalymnos | קלימנוס | 2,697 | +11.5% | 8.4 | +9.7% | 3.7% | IND 2026-09 | ISL 2,759 | 800k | yes | no |
| Skyros | סקירוס | 2,693 | +20.2% |  |  |  | IND 2026-09 | ISL 2,402 | 400k | yes | no |
| Alonnisos | אלוניסוס | 2,638 | -2.2% |  |  |  | IND 2026-09 | ISL 2,667 | 400k | no | no |
| Kefalonia | קפלוניה | 2,630 | +5.0% | 8.15 | -4.8% | 3.7% | IND 2026-09 | ISL 2,531 | 800k | no | no |
| Rhodes | רודוס | 2,612 | +13.7% | 10.27 | +3.5% | 4.7% | IND 2026-09 | ISL 2,105 | 800k | yes | no |
| Amorgos | אמורגוס | 2,578 | +6.7% |  |  |  | IND 2026-09 | ISL 2,143 | 400k | no | no |
| Syros | סירוס | 2,535 | +2.1% | 9.55 | +0.2% | 4.5% | IND 2026-09 | ISL 2,363 | 800k | no | no |
| Leros | לרוס | 2,497 | +35.0% | 6.64 | +66.8% | 3.2% | IND 2026-09 | ISL 2,422 | 800k | yes | no |
| Skopelos | סקופלוס | 2,496 | +7.0% |  |  |  | IND 2026-09 | ISL 2,154 | 800k | no | no |
| Thassos | תאסוס | 2,318 | +5.3% | 9.02 | +18.8% | 4.7% | IND 2026-09 |  | 800k | no | no |
| Andros | אנדרוס | 2,214 | +1.9% | 7.66 | +11.3% | 4.2% | IND 2026-09 | ISL 2,051 | 800k | no | no |
| Karpathos | קרפתוס | 2,100 | +8.4% |  |  |  | IND 2026-09 |  | 800k | yes | no |
| Kos | קוס | 2,014 | +7.2% |  |  |  | IND 2026-09 | ISL 2,125 | 800k | yes | no |
| Salamina | סלמינה | 1,734 | +8.2% | 7.05 | +14.6% | 4.9% | IND 2026-09 |  | 800k | no | no |
| Chios | כיוס | 1,727 | +9.7% | 7.51 | +13.3% | 5.2% | IND 2026-09 | SPI 1,533; ISL 1,533 | 800k | yes | no |
| Samothraki | סמותרקי | 1,449 | +13.7% |  |  |  | IND 2026-09 |  | 400k | yes | no |
| Lesvos | לסבוס | 1,302 | +5.3% | 6.66 | +7.1% | 6.1% | IND 2026-09 | SPI 1,136; ISL 1,136 | 800k | yes | no |
| Samos | סאמוס | 1,204 | +0.8% | 6.56 | +4.0% | 6.5% | IND 2026-09 | SPI 1,059; ISL 1,059 | 800k | yes | no |

Notes: **Antiparos:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Meganisi:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Paxoi:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Patmos:** Population close to the 3,100 threshold; golden-visa tier must be checked against the 2021 census. **Folegandros:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Kythnos:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 3.29 EUR/m2, yoy 1.611). **Milos:** Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 1.33 EUR/m2, yoy None). **Skiathos:** Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 2.23 EUR/m2, yoy -0.241). **Ios:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Lefkada:** Island values = whole regional unit. **Sifnos:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. Indomio rent implies gross yield under 2%: seasonal/small-sample value, not used (published 4.11 EUR/m2, yoy -0.355). **Serifos:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. Indomio rent implies gross yield under 2%: seasonal/small-sample value, not used (published 4.02 EUR/m2, yoy 0.305). **Kea (Tzia):** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Astypalaia:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Ithaca:** Population close to the 3,100 threshold; golden-visa tier must be checked against the 2021 census. **Corfu:** Corfu main island is not on the border-zone list (the Diapontia islets are). **Zakynthos:** Island values = whole regional unit. **Symi:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Skyros:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Alonnisos:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Rhodes:** Indomio "Rhodes" = Rhodes municipality (whole island). **Amorgos:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Skopelos:** Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 1.08 EUR/m2, yoy -0.077). **Karpathos:** Indomio rent yoy beyond +/-100%: small-sample value, not used (published 6.47 EUR/m2, yoy 1.557). **Kos:** Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 3.25 EUR/m2, yoy -0.311). **Chios:** Island values = whole regional unit. **Samothraki:** Island below ~3,100 inhabitants (approximate, 2021 census) so EUR 400k; verify population before relying on it. **Lesvos:** Island values = whole regional unit. **Samos:** Island values = whole regional unit.

## Resort and coastal areas (Halkidiki, Peloponnese coast, Pelion, Evia) (21)

| Place | עברית | Sale €/m² | yoy | Rent €/m²/mo | yoy | Gross yield | Source (period) | Other sale values | GV | Border permit | STR freeze |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|---|
| Halkidiki - Kassandra peninsula north (Pallini unit: Kallithea, Afytos) | חלקידיקי - צפון קסנדרה (פליני) | 3,611 | +6.7% | 18.65 | -5.7% | 6.2% | IND 2026-09 |  | 400k | no | no |
| Halkidiki - Sithonia | חלקידיקי - סיתוניה | 3,418 | +11.8% | 13.65 | -15.6% | 4.8% | IND 2026-09 | HOL 3,000 | 400k | no | no |
| Halkidiki - Kassandra (Kassandra unit) | חלקידיקי - קסנדרה | 3,095 | +3.4% | 14 | -14.1% | 5.4% | IND 2026-09 | HOL 2,895 | 400k | no | no |
| Pylos (Costa Navarino area) | פילוס (אזור קוסטה נבארינו) | 3,065 | -14.5% | 8.7 | +19.8% | 3.4% | IND 2026-09 |  | 400k | no | no |
| Ermioni | ארמיוני | 3,061 | +7.1% | 10.04 | -18.2% | 3.9% | IND 2026-09 |  | 400k | no | no |
| Porto Heli (Kranidi unit, Ermionida) | פורטו חלי | 2,967 | -4.2% | 9.26 | +19.3% | 3.8% | IND 2026-09 |  | 400k | no | no |
| Syvota (Thesprotia) | סיבוטה | 2,795 | +15.3% |  |  |  | HOL 2026-Q2 |  | 400k | yes | no |
| Methoni | מתוני | 2,777 | -3.5% |  |  |  | IND 2026-09 | HOL 2,273 | 400k | no | no |
| Kardamyli - Stoupa (Lefktro unit, Mani) | קרדמילי - סטופה | 2,604 | +4.1% | 7.74 | +16.0% | 3.6% | IND 2026-09 | HOL 2,292 | 400k | no | no |
| Halkidiki - Nea Moudania | חלקידיקי - ניאה מודניה | 2,344 | +10.9% | 10.35 | -13.4% | 5.3% | IND 2026-09 |  | 400k | no | no |
| Halkidiki - Kallikrateia | חלקידיקי - קליקרטיה | 2,295 | +4.5% | 11.12 | +60.5% | 5.8% | IND 2026-09 | HOL 2,513 | 400k | no | no |
| Evia - Karystos | אוויה - קריסטוס | 2,201 | +11.2% | 9.1 | +13.0% | 5.0% | IND 2026-09 |  | check | no | no |
| Koroni | קורוני | 2,171 | +6.1% | 6.88 | +45.5% | 3.8% | IND 2026-09 | HOL 2,250 | 400k | no | no |
| Pelion - Mouresi (Tsagarada) | פליון - מורסי (צגרדה) | 2,008 | +7.6% | 4.85 | +9.0% | 2.9% | IND 2026-09 | HOL 2,134 | 400k | no | no |
| Nafpaktos | נאפקטוס | 1,867 | +17.3% |  |  |  | HOL 2026-Q2 |  | 400k | no | no |
| Xylokastro | קסילוקסטרו | 1,759 | +7.5% | 6.25 | +2.6% | 4.3% | IND 2026-09 | HOL 1,700 | 400k | no | no |
| Evia - Eretria | אוויה - ארטריה | 1,734 | +3.8% | 7.65 | +3.5% | 5.3% | IND 2026-09 | HOL 1,635 | check | no | no |
| Pelion - Milies | פליון - מיליס | 1,703 | +4.0% | 7.82 | -5.1% | 5.5% | IND 2026-09 | HOL 1,644 | 400k | no | no |
| Pelion - Argalasti (south Pelion) | פליון - ארגלסטי | 1,600 | +17.6% |  |  |  | IND 2026-09 |  | 400k | no | no |
| Pelion - Portaria | פליון - פורטריה | 1,488 | +2.5% | 5.85 | -14.6% | 4.7% | IND 2026-09 |  | 400k | no | no |
| Pelion - Zagora | פליון - זגורה | 1,371 | +4.3% |  |  |  | IND 2026-09 | HOL 1,171 | 400k | no | no |

Notes: **Halkidiki - Kassandra peninsula north (Pallini unit: Kallithea, Afytos):** Kassandra municipality = Kassandra + Pallini units; Indomio publishes both separately. **Halkidiki - Kassandra (Kassandra unit):** Kassandra municipality = Kassandra + Pallini units; Indomio publishes both separately. **Pylos (Costa Navarino area):** Engel & Völkers 2026 gives Pylos/Gialova 3,000-6,000 EUR/m2 (holiday homes, broker range). **Porto Heli (Kranidi unit, Ermionida):** Porto Heli lies in the Kranidi municipal unit; Engel & Völkers 2026: 4,000-6,000, prime up to 12,000+. **Methoni:** Indomio rent yoy beyond +/-100%: small-sample value, not used (published 7.93 EUR/m2, yoy 2.389). **Evia - Karystos:** On Evia island (>3,100 inhabitants): EUR 800k likely applies; verify. **Evia - Eretria:** On Evia island (>3,100 inhabitants): EUR 800k likely applies; verify. **Pelion - Zagora:** Indomio rent below 4 EUR/m2: implausible small-sample value, not used (published 2.52 EUR/m2, yoy None).

## Rankings (primary values)

**10 most expensive places:** Vouliagmeni 7,710; Mykonos 7,633; Antiparos 7,420; Hydra 7,188; Meganisi 6,303; Voula 6,198; Plaka 6,116; Syntagma 6,067; Elliniko (Ellinikon) 5,745; Paros 5,656.

**10 cheapest places:** Florina 662; Kastoria 690; Grevena 730; Kozani (regional unit) 741; Kilkis 772; Kozani (city) 838; Karditsa 875; Lamia 876; Drama 886; Pella (Edessa, Giannitsa) 891.

**Biggest asking-price risers (yoy):** Leros +35.0%; Stavroupoli +21.2%; Skyros +20.2%; Milos +19.4%; Thiseio +18.4%; Larissa (city) +18.0%; Pelion - Argalasti (south Pelion) +17.6%; Oraiokastro +17.5%; Gazi - Metaxourgeio - Votanikos +17.3%; Nafpaktos +17.3%; Rest of Thessaloniki prefecture +17.1%; Larissa (regional unit) +16.8%; Spetses +16.4%; Argyroupoli +16.2%; Syvota (Thesprotia) +15.3%. Leros, Skyros, Milos and Samothraki are thin island samples.

**Fallers:** Pylos (Costa Navarino area) -14.5%; Grevena -6.4%; Lasithi (Agios Nikolaos, Elounda) -5.7%; Sifnos -5.1%; Marathon -4.7%; Porto Heli (Kranidi unit, Ermionida) -4.2%; Perama -4.0%; Methoni -3.5%.

**Highest computed gross yields:** Florina 9.7%; Karditsa 8.7%; Kastoria 8.7%; Arta 8.5%; Kozani (city) 8.5%; Lamia 8.0%; Kozani (regional unit) 7.4%; Grevena 7.4%; Kilkis 7.2%; Trikala (regional unit, Meteora) 7.1%.

**Lowest computed gross yields:** Pelion - Mouresi (Tsagarada) 2.9%; Agios Nikolaos (incl. Elounda) 3.0%; Mykonos 3.0%; Naxos 3.0%; Paros 3.1%; Leros 3.2%; Elliniko (Ellinikon) 3.2%; Poros 3.2%; Argosaronic islands (Aegina, Hydra, Spetses, Poros, Salamina) 3.2%; Argyroupoli 3.2%.

## Price by type

- **New vs old, Bank of Greece (Q2 2026):** new flats (up to 5 years) +6.2% yoy, older +5.0%; index new 120.0 vs old 110.6 (2007=100).
- **New vs older, Spitogatos asking 2025** (source https://www.spitogatos.gr/blog/energeiaki-apodosi-etos-kataskevis-katoikies-times-enoikiasi-pwlisi, 31.3.2026). New-builds were about 7% of homes for sale and 3% of rentals in the Municipality of Athens.

| Area | Older sale €/m² | New sale €/m² | Premium | Older rent | New rent | Premium |
|---|---:|---:|---:|---:|---:|---:|
| Athens Centre | 2,250 | 4,000 | +77.8% | 11.3 | 15.5 | +37.2% |
| Athens East | 2,077 | 3,195 | +53.8% | 8.9 | 10.3 | +15.7% |
| Athens North | 2,800 | 4,495 | +60.5% | 11.3 | 15.2 | +34.5% |
| Athens South | 3,226 | 5,122 | +58.8% | 12.6 | 18.8 | +49.2% |
| Athens West | 1,888 | 3,333 | +76.5% | 8.7 | 11.5 | +32.2% |
| Piraeus | 2,364 | 3,723 | +57.5% | 10.1 | 12.0 | +18.8% |
| Piraeus suburbs | 1,856 | 3,235 | +74.3% | 8.6 | 11.6 | +34.9% |
| Thessaloniki municipality | 2,455 | 3,190 | +29.9% | 10.0 | 13.4 | +34.0% |
| Thessaloniki suburbs | 1,554 | 2,667 | +71.6% | 7.5 | 9.7 | +29.3% |

**Energy class, Spitogatos asking 2025** (high = A+ to B):

| Area | High sale | Mid sale | Low sale | High rent | Mid rent | Low rent |
|---|---:|---:|---:|---:|---:|---:|
| Athens Centre | 3,529 | 2,412 | 1,915 | 12.6 | 11.3 | 10.6 |
| Athens East | 2,949 | 2,075 | 1,949 | 10.0 | 8.8 | 8.8 |
| Athens North | 4,286 | 2,787 | 2,667 | 12.5 | 11.0 | 10.9 |
| Athens South | 4,925 | 3,238 | 2,481 | 15.6 | 12.3 | 10.7 |
| Athens West | 3,133 | 1,944 | 1,584 | 9.6 | 8.6 | 8.2 |
| Piraeus | 3,450 | 2,526 | 2,000 | 11.5 | 10.0 | 9.4 |
| Piraeus suburbs | 3,130 | 1,964 | 1,531 | 9.4 | 8.6 | 7.8 |
| Thessaloniki municipality | 3,000 | 2,500 | 2,027 | 11.0 | 10.0 | 9.5 |
| Thessaloniki suburbs | 2,460 | 1,585 | 1,200 | 8.1 | 7.4 | 7.0 |

**Size bands, xe.gr Q3 2026 asking €/m²** (up to 80 m² / 81-120 m² / 121 m²+), selected markets:

| Market | Sale ≤80 | Sale 81-120 | Sale 121+ | Rent ≤80 | Rent 81-120 | Rent 121+ |
|---|---:|---:|---:|---:|---:|---:|
| Αθήνα | 3,087 | 2,874 | 3,086 | 13.13 | 11.0 | 12.92 |
| Πάτρα | 2,082 | 1,730 | 1,548 | 10.03 | 6.39 | 5.96 |
| Περιστέρι | 2,931 | 2,699 | 2,296 | 10.63 | 7.75 | 7.69 |
| Κηφισιά | 4,819 | 4,439 | 4,434 | 16.07 | 13.87 | 13.04 |
| Ζωγράφου | 2,922 | 3,009 | 2,575 | 12.29 | 9.42 | 8.91 |
| Αγ. Παρασκευή | 3,991 | 3,926 | 3,841 | 13.78 | 12.24 | 10.33 |
| Άλιμος | 4,248 | 5,053 | 5,807 | 15.65 | 13.32 | 13.86 |
| Βούλα | 5,973 | 6,795 | 6,866 | 20.27 | 18.81 | 18.13 |
| Νέα Ιωνία | 3,454 | 3,072 | 2,415 | 11.32 | 9.3 | 7.85 |
| Ηλιούπολη | 3,713 | 3,740 | 3,867 | 12.84 | 9.78 | 9.02 |
| Αγ. Δημήτριος Αττικής | 3,890 | 3,607 | 3,524 | 12.66 | 9.71 | 8.06 |
| Πειραιάς | 3,245 | 2,931 | 2,573 | 12.37 | 9.43 | 8.56 |
| Νίκαια | 2,448 | 2,452 | 2,325 | 10.39 | 8.4 | 6.22 |
| Αιγάλεω | 2,794 | 2,351 | 2,054 | 12.54 | 8.08 | 10.05 |
| Γέρακας | 3,782 | 3,550 | 2,698 | 11.7 | 10.62 | 9.24 |
| Βύρωνας | 3,006 | 3,089 | 2,734 | 11.96 | 8.79 | 8.92 |
| Ίλιον | 2,535 | 2,528 | 1,929 | 10.4 | 7.81 | 7.1 |
| Βάρη | 4,845 | 5,564 | 4,928 | 17.06 | 16.52 | 15.09 |
| Ηράκλειο, Αττική | 3,288 | 3,652 | 3,346 | 11.4 | 9.89 | 8.59 |
| Αχαρνές | 2,169 | 1,941 | 1,693 | 9.19 | 7.84 | 9.6 |
| Ηράκλειο, Κρήτη | 2,711 | 3,063 | 2,615 | 12.06 | 9.36 | 8.47 |
| Γαλάτσι | 2,872 | 3,156 | 2,575 | 10.85 | 8.33 | 7.55 |
| Θεσσαλονίκη | 2,936 | 2,529 | 2,803 | 12.13 | 8.82 | 8.63 |
| Χολαργός | 3,892 | 4,209 | 3,978 | 13.46 | 10.6 | 12.7 |
| Κορυδαλλός | 2,663 | 2,393 | 2,422 | 10.41 | 8.17 | 6.47 |
| Βριλήσσια | 4,955 | 4,444 | 4,117 | 13.31 | 11.77 | 12.07 |
| Αργυρούπολη | 4,596 | 4,209 | 4,367 | 12.34 | 10.89 | 10.01 |
| Κερατσίνι | 2,286 | 2,220 | 2,079 | 10.31 | 7.27 | 6.71 |
| Νέα Ερυθραία | 4,798 | 3,556 | 3,321 | 12.45 | 12.6 | 11.22 |
| Δάφνη Αττικής | 3,605 | 3,434 | 2,810 | 12.72 | 8.95 | 9.6 |
| Καισαριανή | 3,172 | 3,285 | 3,259 | 15.08 | 10.69 | 9.27 |
| Ελληνικό | 6,484 | 5,216 | 6,507 | 16.52 | 13.18 | 19.78 |
| Πετρούπολη | 2,894 | 2,956 | 2,767 | 10.44 | 8.87 | 8.33 |
| Γλυφάδα | 5,498 | 5,432 | 6,682 | 17.53 | 15.97 | 19.18 |
| Χαϊδάρι | 2,526 | 2,604 | 2,342 | 10.53 | 8.46 | 8.37 |
| Μεταμόρφωση | 3,313 | 3,164 | 2,759 | 11.14 | 9.04 | 8.53 |
| Καλύβια Θορικού | 3,427 | 2,796 | 2,724 | 13.53 | 12.68 | 11.71 |
| Μελίσσια | 3,842 | 4,303 | 3,359 | 13.05 | 10.75 | 10.12 |
| Μοσχάτο | 4,058 | 3,566 | 3,122 | 12.68 | 9.84 | 10.11 |
| Άρτεμις | 2,556 | 2,298 | 1,930 | 12.02 | 9.04 | 7.89 |
| Πόρτο Ράφτη | 3,645 | 3,196 | 2,309 | 14.27 | 11.53 | 9.63 |
| Παλλήνη | 3,264 | 3,059 | 2,664 | 11.91 | 9.51 | 8.24 |
| Καλαμαριά | 3,194 | 3,130 | 3,349 | 11.31 | 9.4 | 9.14 |
| Κορωπί | 3,094 | 2,497 | 2,263 | 11.03 | 8.8 | 9.29 |
| Καλλιθέα | 3,326 | 3,313 | 3,312 | 12.1 | 9.36 | 11.8 |
| Σαρωνίδα | 3,819 | 3,789 | 3,577 | 15.29 | 13.84 | 11.43 |
| Παλαιό Φάληρο | 3,999 | 4,307 | 4,489 | 15.02 | 11.62 | 12.09 |
| Χαλάνδρι | 4,028 | 3,842 | 3,558 | 14.57 | 13.0 | 11.78 |
| Νέα Σμύρνη | 3,472 | 3,657 | 3,380 | 12.68 | 10.17 | 9.97 |
| Μαρούσι | 4,028 | 4,093 | 3,625 | 14.86 | 12.57 | 11.61 |

- **Transactions, new vs older (RE/MAX closed sales 2025):** East Thessaloniki 1,840 vs 2,800; West Thessaloniki 1,306 vs 2,107; Peraia 1,400 vs 2,000; Lagonisi 2,000 vs 3,000 €/m².
- **Apartment vs house:** No provider publishes EUR/m2 for apartments vs detached houses per area in 2026. AADE transfer-values registry 2025: 21,354 apartments worth EUR 2.25 bn and 4,278 houses worth EUR 451.11m were posted (a subset of all deals).

## Ten-year history

No year-by-year Spitogatos SPI EUR/m2 series by region for 2016-2025 is published in open form (searched: press, Spitogatos blog, SPI page, Datawrapper chart behind the SPI page = demand map only). Official 10-year history = Bank of Greece index below.

**Bank of Greece apartment price index, annual average (2007=100):**

| Series | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026-Q2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| whole_country_all | 59.6 | 59.0 | 60.1 | 64.4 | 67.3 | 72.4 | 81.1 | 92.3 | 100.7 | 109.1 | 114.2 |
| whole_country_new | 61.2 | 60.7 | 61.9 | 66.7 | 70.0 | 75.7 | 85.1 | 96.1 | 106.0 | 114.3 | 120.0 |
| whole_country_old | 58.6 | 57.9 | 58.9 | 63.0 | 65.6 | 70.4 | 78.5 | 89.9 | 97.5 | 105.8 | 110.6 |
| greater_athens_all | 56.8 | 56.2 | 57.8 | 63.9 | 68.9 | 75.6 | 86.1 | 98.0 | 106.5 | 113.5 | 118.3 |
| thessaloniki_all | 55.2 | 54.5 | 55.1 | 58.9 | 61.8 | 66.5 | 74.9 | 87.3 | 97.5 | 107.0 | 111.9 |
| other_cities_all | 62.4 | 61.6 | 62.2 | 64.5 | 64.6 | 68.3 | 75.8 | 87.2 | 93.8 | 103.5 | 108.2 |
| other_areas_all | 64.6 | 64.1 | 64.8 | 67.7 | 69.0 | 72.5 | 78.3 | 87.4 | 97.0 | 106.3 | 112.8 |
| urban_areas_all | 58.6 | 58.0 | 59.0 | 63.4 | 66.4 | 71.7 | 80.6 | 92.0 | 100.1 | 108.1 | 113.0 |

Change Q2 2016 to Q2 2026: whole country +91.5%, Athens +108.0%, Thessaloniki +102.6%, other cities +73.2%, other areas +74.6%. Trough 2017-Q3; 2026-Q2 is a series high.

- Spitogatos national asking-price yoy: 2025 year +9.6%; Q2 2025 +9.7%; Q3 2025 +10.0%; Q1 2026 +7.9%; Q2 2026 +6.1%; Q3 2026 +5.7%. Attica 2025 +8.1%.
- Spitogatos islands Q2 2021 to Q2 2026: Aegean 2,071 to 2,941; Ionian 1,719 to 2,531; Crete 1,500 to 2,250 €/m².
- Spitogatos North Greece 2022 to Q1 2026: Macedonia (excl. Thessaloniki) sale +53.7%, Thrace +38.3%, Alexandroupoli +51.3%, Xanthi +45.3%, Komotini +38.5%, Drama +32.4%, Veria +25.5%, Katerini +23.3%, Serres +19.6%, Kozani +4.0%.
- Thessaly asking price +35.3% from 2019 to Q3 2025 (1,273 €/m²); Peloponnese +30.7% 2019-2024; Epirus 1,538 €/m² in 2025 (+7.3%), rent 6.1 (2019) to 8.9 €/m².
- Indomio whole country: sale +14.3% in 3 years, +38.5% in 5 years, +48.3% since early 2020; rent +43.9% in 5 years.
- GEOAXIS Mykonos typical holiday home: 2,141 (2017) to 2,969 €/m² (2026).

## Market activity

| Year | ELSTAT notarial property sales (all property types) |
|---|---:|
| 2014 | 43,443 |
| 2015 | 54,631 |
| 2016 | 60,540 |
| 2017 | 69,826 |
| 2018 | 79,532 |
| 2019 | 96,662 |
| 2020 | 74,769 |
| 2021 | 104,746 |
| 2022 | 112,283 |
| 2023 | 122,123 |
| 2024 | 145,765 |

2025 not yet published by ELSTAT. Other measures (all property types):

- AADE 2024: 225,000 declarations; EUR 23.0 bn; declarations (one per co-owner/right), all property types; ~EUR 1.5 bn mortgage-funded (https://www.newmoney.gr/roh/palmos-oikonomias/oikonomia/i-aade-xeskonizi-45-000-metavivasis-akiniton-sto-mikroskopio-ta-simvolea/, 2025-05-16).
- AADE 2025: 223,000 declarations; myPROPERTY sale declarations; transfer-tax revenue EUR 607.93m (2024: 656.49m) (https://www.tovima.gr/2026/03/05/finance/akinita-posa-allaksan-xeria-o-xartis-ton-xryson-metavivaseon/, 2026-03-05).
- AADE 2025: EUR 23.5 bn; AADE total value of properties that changed hands (all types) (https://greekreporter.com/2026/07/20/foreign-investment-greece-real-estate-2019-2025/, 2026-07-20).
- AADE 2026-H1: 112,320 declarations; EUR 12.0 bn; H1 2025: 108,228 declarations; avg value EUR 115k (H1 2025 110k); ~EUR 1.3 bn mortgage-funded; ~EUR 550m from foreign investors (https://www.powergame.gr/forologia/1385920/akinita-axias-12-dis-evro-allaxan-cheria-to-a-examino/, 2026-07-13).
- Transfer-values registry 2025: 41,743 properties, EUR 4.2 bn; 21,354 apartments (EUR 2.25 bn), 4,278 houses (EUR 451m); Athens city 5,816 sales (EUR 626m). Subset of the market (https://www.in.gr/2026/01/13/economy/allaksan-xeria-akinita-42-dis-eyro-2025/).
- Bank of Greece foreign direct investment into real estate (EUR m): 2019 1,449, 2021 1,176, 2022 1,975, 2023 2,130, 2024 2,750, 2025 2,050, 2026-Q1 511.6; 2019-2025 total 12,400 (2002-2018: 3,380).
- Foreign buyers' share: about 4.6% of transaction value in H1 2026 (EUR 550m of 12 bn, computed); property was 16.6% of all FDI in 2025. No official share by count is published.
- Attica and Thessaloniki: Israelis most active foreign buyers, then Turks, Lebanese, Chinese, Ukrainians; rest of Greece: Germans lead (RE/MAX Hellas, via alfavita.gr 2026-01-12). Turkish buyers: EUR 293m (2024), 214m (2025). Israel 2002-2022 cumulative: EUR 253m.
- Golden visa: initial applications 8,477 (2023), 9,411 (2024); 9,479 permits granted in 2025; Jan-Apr 2026 applications 1,677 vs 3,507 a year earlier; Israeli approvals 544 in 9M 2025 vs 296.

## Construction cost

- ELSTAT input-cost index for new homes, Q2 2026: +4.0% yoy (materials +4.3%, labour +3.6%), +1.7% on the quarter; Q1 2026 +2.8% (https://www.forin.gr/articles/article/91582/elstat-aukshsh-3-shmeiwse-o-genikos-deikths-timwn-ergwn-kataskeuhs-newn-katoikiwn-to-b-trimhno-efetos, 23.7.2026).
- ELSTAT output-price index for new residential construction, Q2 2026: +3.0% yoy.
- Euro per m² to build: press says "often 1,900 €/m² or more" depending on quality (newmoney.gr, 7.5.2026; no named industry body; low confidence).
- Building permits May 2026: 2,669 (-0.8%), 585,896 m² (+4.6%); rolling 12 months permits +9%, floor area +14%.
- Gap: No TEE or PEDMEDE 2026 EUR/m2 construction-cost figure found; ELSTAT Q3 2026 index not yet released.

## Luxury and prime

Prime/luxury EUR/m2. Broker ranges (Engel & Völkers) and listing medians (GEOAXIS) are NOT comparable with the all-stock averages in places[].

| Place | Low €/m² | High €/m² | What | Source date |
|---|---:|---:|---|---|
| Mykonos | 16,790 | 30,000 | GEOAXIS luxury median asking / top listing (+4.94% yoy); typical home median 2,969 | 2026-08-05 |
| Mykonos | 7,500 | 12,000 | Engel & Völkers 2026 holiday-home range | 2026-06-05 |
| Santorini | 13,943 | 25,000 | GEOAXIS luxury median asking / top listing (+4.90%); typical 2,363 | 2026-08-05 |
| Santorini | 4,500 | 8,000 | Engel & Völkers 2026 range; Oia and Imerovigli caldera named as premium (no figure) | 2026-07-17 |
| Paros | 10,026 | 20,000 | GEOAXIS luxury median asking / top listing (+5.55%); typical 2,384 | 2026-08-05 |
| Paros | 5,500 | 10,000 | Engel & Völkers 2026 range | 2026-06-05 |
| Antiparos | 6,800 | 10,200 | Engel & Völkers 2026 range | 2026-06-05 |
| Kea | 6,549 | 16,000 | GEOAXIS luxury median / top listing; E&V 3,500-7,000 | 2026-08-05 |
| Vouliagmeni (Athens Riviera) | 8,500 | 12,000 | Engel & Völkers 2026 average sale range; iconic seafront homes can exceed 20,000 | 2026-05-15 |
| Glyfada | 5,300 | 9,000 | Engel & Völkers 2026 range | 2026-05-15 |
| Kolonaki | 6,086 |  | Engel & Völkers 2026 average (Syntagma 5,638) | 2026-05-15 |
| Palaio Psychiko / Filothei |  | 10,000 | Engel & Völkers 2026: new-build up to 10,000 | 2026-05-15 |
| The Ellinikon - Riviera Tower | 14,036 |  | average pre-sale price, 171 units, EUR 626m (AXIA data on Lamda) | 2025-09-12 |
| The Ellinikon - Cove Residences / Cove Villas / Park Rise | 10,048 | 11,359 | average pre-sale prices (AXIA) | 2025-09-12 |
| The Ellinikon - Little Athens (Mainstream) | 7,575 | 8,873 | average pre-sale prices (AXIA); overall Ellinikon 7,500-14,000 | 2025-09-12 |
| Porto Heli / Kosta | 4,000 | 12,000 | Engel & Völkers 2026: 4,000-6,000, prime 12,000+ | 2026-06-05 |
| Messinia - Pylos / Gialova (Costa Navarino area) | 3,000 | 6,000 | Engel & Völkers 2026 range (no resort-specific figure) | 2026-06-05 |
| Halkidiki (beachfront) | 8,000 | 14,000 | Engel & Völkers 2026 range | 2026-06-05 |
| Corfu | 3,200 | 3,800 | Engel & Völkers 2026; seafront mansions sometimes above 8,500 | 2026-07-17 |
| Hydra | 5,000 | 7,500 | Engel & Völkers 2026 | 2026-07-17 |
| Paxoi | 4,200 | 9,500 | Engel & Völkers 2026: 4,200-5,000, top villas above 9,500 | 2026-07-17 |
| Lefkada | 3,800 | 7,500 | Engel & Völkers 2026: 3,800-3,900, luxury up to 7,500 | 2026-07-17 |
| Kefalonia | 3,000 | 7,500 | Engel & Völkers 2026: 3,000-3,600, up to 7,500 | 2026-07-17 |
| Elounda (Crete) |  |  | no published EUR/m2 found; Indomio Agios Nikolaos municipality (incl. Elounda) 3,901 (Sep 2026) |  |

Highest area averages in the list (Indomio Sep 2026): Vouliagmeni 7,710; Mykonos 7,633; Antiparos 7,420; Hydra 7,188; Meganisi 6,303; Voula 6,198; Plaka 6,116; Syntagma 6,067; Elliniko 5,745; Paros 5,656.

## Numbeo city centre vs outside (crowd-sourced, low confidence)

| City | Centre €/m² | Outside €/m² | 1-bed rent centre €/month | Yield centre | Yield outside |
|---|---:|---:|---:|---:|---:|
| Athens | 3,616 | 2,969 | 661 | 3.9% | 4.2% |
| Thessaloniki | 3,303 | 2,522 | 560 | 3.7% | 3.7% |
| Heraklion | 3,197 | 2,337 | 572 | 3.8% | 4.3% |
| Patras | 1,826 | 1,568 | 435 | 5.0% | 4.9% |
| Chania | 3,693 | 3,134 | 564 | 3.4% | 3.3% |

Numbeo has enough data only for these five Greek cities (last update 22.10.2026; Chania 17 and Patras 20 contributors).

## Conflicts between sources (difference above 15% for sale, 20% for rent)

Rule used: the map and tables use Indomio September 2026 everywhere it exists, so that places are compared on one method and one month. The second value is kept in the JSON and should be shown in the tooltip. A systematic pattern: Indomio is 15-30% above Spitogatos on the islands and in some regional units (different listing pools and averaging), close to Spitogatos in Athens and Thessaloniki.

| Place | Used | Other value | Why the difference / what to do |
|---|---|---|---|
| Ionian Islands (sale) | IND 3,083 | ISL 2,531 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Aegean islands (Indomio grouping) (sale) | IND 3,627 | ISL 2,941 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Aitoloakarnania (Agrinio, Mesolongi) (sale) | IND 1,228 | SPI 1,031 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Arkadia (Tripoli) (sale) | IND 1,477 | SPI 1,207 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Grevena (sale) | IND 730 | SPI 850 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Dodecanese (sale) | IND 2,696 | SPI 2,219 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Karditsa (sale) | IND 875 | SPI 741 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Kastoria (sale) | IND 690 | SQ3 577 (2026-Q3) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Kastoria (sale) | IND 690 | SPI 585 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Kastoria (rent) | IND 5 | SPI 6.25 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Corfu (regional unit, incl. Paxoi) (sale) | IND 3,032 | SPI 2,417 (2026-Q2) | Indomio 3,032 vs Spitogatos 2,417 (+25%). Different listing pools; show both, label Indomio as the map value. |
| Kozani (regional unit) (rent) | IND 4.59 | SPI 6 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Lakonia (Sparti, Monemvasia) (sale) | IND 1,623 | SPI 1,359 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Lasithi (Agios Nikolaos, Elounda) (sale) | IND 2,678 | SPI 1,944 (2026-Q2) | Indomio 2,678 vs Spitogatos 1,944: Indomio sample weighted to Agios Nikolaos/Elounda listings. Show both. |
| Lasithi (Agios Nikolaos, Elounda) (sale) | IND 2,678 | ISL 1,944 (2026-Q2) | Indomio 2,678 vs Spitogatos 1,944: Indomio sample weighted to Agios Nikolaos/Elounda listings. Show both. |
| Xanthi (regional unit) (rent) | IND 5.89 | SPI 8 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Rodopi (Komotini) (rent) | IND 5.77 | SPI 8 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Serres (regional unit) (rent) | IND 5.15 | SPI 6.73 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Florina (rent) | IND 5.34 | SPI 7.95 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Argosaronic islands (Aegina, Hydra, Spetses, Poros, Salamina) (sale) | IND 2,900 | SPI 2,366 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Athens Centre (Municipality of Athens) (sale) | IND 2,844 | NUM 3,616 (rolling 12 months to 2026-10-22) | Numbeo 3,616 is crowd-sourced "city centre" (a narrower, pricier zone); Spitogatos 2,500 (Q2) and xe 3,029 bracket Indomio 2,844. |
| Kolonaki - Lykavittos (rent) | IND 18.83 | RMX 14 (2026) | RE/MAX 14.0 is closed lettings; asking rents (Indomio 18.83, Spitogatos 18.0) are higher. Expected gap. |
| Koukaki - Makrygianni (rent) | IND 14.92 | RMX 9.7 (2026) | RE/MAX 9.7 closed lettings vs Indomio 14.92 asking: Koukaki asking rents reflect short-let style listings; show both. |
| Vari - Varkiza (rent) | IND 16.66 | RMX 13 (2026) | Closed lettings (RE/MAX) run below asking rents. |
| Kaisariani (rent) | IND 12.19 | SQ3 14.7 (2026-Q3) | Different provider / quarter; keep Indomio for the map. |
| Nea Ionia (sale) | IND 2,696 | XE 3,165 (2026-Q3) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Moschato (sale) | IND 3,107 | XE 3,739 (2026-Q3) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Thessaloniki (municipality) (sale) | IND 2,696 | NUM 3,303 (rolling 12 months to 2026-10-22) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Rest of Thessaloniki prefecture (rent) | IND 4.55 | SQ3 5.6 (2026-Q3) | Different provider / quarter; keep Indomio for the map. |
| 40 Ekklisies - Evangelistria (rent) | IND 9.28 | SQ3 11.4 (2026-Q3) | Different provider / quarter; keep Indomio for the map. |
| 40 Ekklisies - Evangelistria (rent) | IND 9.28 | SQ2 11.9 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Vardaris - Lachanokipoi (rent) | IND 9.74 | SQ3 12.5 (2026-Q3) | Different provider / quarter; keep Indomio for the map. |
| Vardaris - Lachanokipoi (rent) | IND 9.74 | SQ2 12 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Peraia (Thermaikos) (sale) | IND 2,352 | RMX 1,400 (2025) | RE/MAX 1,400 is completed sales of older homes in Peraia only; Indomio 2,352 is all asking listings in Thermaikos municipality. |
| Heraklion (city) (sale) | IND 2,351 | XE 2,813 (2026-Q3) | xe 2,813 is a listing-weighted mean of size bands; Numbeo 3,197 is crowd-sourced. Indomio 2,351 used. |
| Heraklion (city) (sale) | IND 2,351 | NUM 3,197 (rolling 12 months to 2026-10-22) | xe 2,813 is a listing-weighted mean of size bands; Numbeo 3,197 is crowd-sourced. Indomio 2,351 used. |
| Larissa (city) (rent) | IND 7.87 | STU 10 (2026-Q2) | Student-housing rents are small units (higher €/m²); not comparable. |
| Volos (rent) | IND 8.07 | STU 10 (2026-Q2) | Student-housing rents are small units (higher €/m²); not comparable. |
| Serres (city) (rent) | IND 5.25 | NG 6.6 (2026-Q1) | Different provider / quarter; keep Indomio for the map. |
| Chalkida (rent) | IND 8.8 | STU 10.7 (2026-Q2) | Student-housing rents are small units (higher €/m²); not comparable. |
| Rhodes (sale) | IND 2,612 | ISL 2,105 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Rhodes (rent) | IND 10.27 | STU 13.3 (2026-Q2) | Student-housing rents are small units (higher €/m²); not comparable. |
| Symi (sale) | IND 2,843 | ISL 2,157 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Amorgos (sale) | IND 2,578 | ISL 2,143 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Corfu (sale) | IND 2,993 | ISL 2,417 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Paxoi (sale) | IND 5,495 | ISL 3,846 (2026-Q2) | Indomio 5,495 vs Spitogatos 3,846: tiny island sample; treat as indicative. |
| Zakynthos (sale) | IND 2,895 | SPI 2,300 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Zakynthos (sale) | IND 2,895 | ISL 2,300 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Zakynthos (rent) | IND 7.93 | SPI 10 (2026-Q2) | Different provider / quarter; keep Indomio for the map. |
| Ithaca (sale) | IND 3,079 | ISL 2,455 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Spetses (sale) | IND 5,495 | HOL 4,615 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Methoni (sale) | IND 2,777 | HOL 2,273 (2026-Q2) | Different provider / listing pool; keep the Indomio value for the map and show the other in the tooltip. |
| Halkidiki (rent) | IND 12.38 | SPI 21.11 (Q2 2026; Q2 2025 32.14) | SPI value swings 34% in a year: small sample. Not used. |
| Spitogatos holiday homes text vs table | table yoy used | Porto Rafti +14.7% (text) vs +15.1% (table); Palaia Fokaia +14.3% vs +7.8%; Poros ">20%" vs +7.8%; Spetses "+10%" vs +15.1% | The blog text and its own table disagree; table values kept. |
| Lefkada (sale) | IND 3,816 | SQ3 3,500 (RU), SPI 3,302 (Q2) | Prices moved between Q2 and Q3; Spitogatos Q3 lists the regional unit at 3,500. |

## Could not find

- One published figure for six administrative regions: Central Macedonia, East Macedonia & Thrace, West Macedonia, Western Greece, North Aegean, South Aegean (providers publish regional units or their own groupings). Not computed, to avoid invented weights.
- Spitogatos Q3 2026 full tables per regional unit and per Athens/Thessaloniki sub-area: only top-5 / bottom-5 lists were released on 22.10.2026; the SPI page still shows Q2 2026.
- A year-by-year Spitogatos SPI €/m² series 2016-2025 by region (the official Bank of Greece index is used for history instead).
- Island rents for Kos, Milos, Sifnos, Serifos, Kythnos, Skiathos, Skopelos, Patmos, Antiparos, Ios, Folegandros, Amorgos, Paxoi, Ithaca, Meganisi, Hydra, Spetses, Symi, Karpathos, Astypalaia, Alonnisos, Skyros, Samothraki (no reliable long-let asking rent).
- Elounda-only, Oia-only, Ekali/Kifisia prime and north-east Corfu prime €/m²; Knight Frank / Savills / Sotheby's Greece price levels.
- Construction cost per m² from TEE or PEDMEDE for 2026 (only a press "1,900 €/m² or more" figure).
- Residential-only transaction counts for 2025 and a foreign-buyer share by number of deals; Bank of Greece FDI 2026 H1.
- Apartment vs detached-house €/m² per area; Bank of Greece and ELSTAT Q3 2026 releases (not yet published).
- Lagonisi asking price (only RE/MAX 2025 deals), Porto Rafti in Indomio (xe used), Komotini/Xanthi/Katerini/Veria/Drama/Kozani city-level Indomio figures (Spitogatos Q1 2026 used), Trikala city after Q3 2025.
- Golden-visa tags for small islands rely on approximate 2021 populations; Evia's treatment (island vs mainland) and whether Ioannina, Serres and Drama cities fall inside the partial border zone were not verified.

## Evidence files

- `raw/indomio/indomio_capture_2026-10-22.txt` and `raw/neighbourhoods/browser_capture_indomio_spitogatos_2026-10-22.txt` (Indomio pages read in the browser; the site blocks scripts).
- `raw/regions/spi_q2_2026_deiktis-timon.txt` (Spitogatos SPI table), `raw/xe_q3_2026.json` (xe.gr parsed by `parse_xe.py`), `raw/notes-1.md` (Spitogatos Q3/Q2/islands/holiday tables), `raw/types/age_*.png` (new vs old, energy class), `raw/market/` (ELSTAT, BoG, AADE, luxury), `raw/numbeo/`, `raw/agent_regions.json`, `raw/agent_neigh.json`.
