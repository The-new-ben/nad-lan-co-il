# Environmental hazards near a home: science, law and checks (research notes)

Research date: 3 November 2026. Companion data: `facts.json` in this folder, with 117 rows: 106 sourced facts plus 11 rows that record a gap ("NOT FOUND" or "NOT VERIFIED").

**How to read the sources.** gov.il pages (MoEP, Ministry of Health) returned HTTP 403 to scripted fetches. Primary texts were read where a file could be downloaded: the radiation law (Knesset PDF), an MoEP measurement letter, the IARC press release, a Knesset draft of the antenna regulations, and the MoEP pollutant-register report. Everything else came from secondary pages or from search summaries, and `source_name` and `source_date` say which. Before a number goes on the public page, check every row marked "secondary", "media" or "read via search summary".

**Privacy warning.** The MoEP magnetic-field letter used for several ELF facts contains a resident's name, phone and address. Use it as an internal citation only. Never link it on the public page. The same standard wording appears in other MoEP measurement letters, so look for one that has no personal details.

---

## 1. The Non-Ionizing Radiation Law (חוק הקרינה הבלתי מייננת, התשס"ו-2006)

Read in full from the official text (ספר החוקים התשס"ו, p.158, 1 January 2006).

- **Permits.** Building or operating any radiation source needs a permit from the Supervisor (ממונה), and so does giving a measurement service (s.3).
  - An operating permit lasts 5 years.
  - A construction permit lasts 3 months, extendable to 9 months in total (s.5).
  - Before construction: an exposure assessment by a licensed measurer (s.6).
  - Before operation: real measurements at several distances, showing levels below the maxima the Supervisor set (s.7).
- **Publication.** The Supervisor must publish (s.19):
  - permit holders and revoked permits;
  - the locations of permitted sources;
  - exposure assessments;
  - test and measurement results;
  - construction-permit applications.
- **Enforcement.**
  - Penalty: six months' prison or a fine, double for a corporation, plus 5% of the fine for each day an offence continues.
  - Anyone harmed by an order can ask a court to cancel it.
  - The Supervisor's decisions go to the administrative court.
- **Links to other laws.**
  - **Civil-claims law.** Non-ionizing radiation was added to the Prevention of Environmental Nuisances (Civil Claims) Law, 1992, so a resident can sue.
  - **Planning and Building Law.** A permit for a cellular facility now requires an indemnity letter (כתב שיפוי) against compensation claims. The 2018 regulations cite this as section 266ג.
  - **Electricity sector.** Until regulations are made, the Supervisor's decisions must follow the report of the Expert Committee on grid magnetic fields.

**Exposure thresholds for cellular sites.** MoEP applies stricter limits than ICNIRP:
- 10% of the ICNIRP level where people stay for long periods (homes, offices);
- 30% where people pass briefly (sidewalks, roads).

This comes from the Environmental Health in Israel 2020 report, and a municipal report repeats it. The MoEP page itself could not be read. Media turn the 10% into 40-100 µW/cm², depending on frequency; that conversion is not checked against MoEP. ICNIRP's 2020 update left the cellular limits unchanged. Whether Israel formally moved to ICNIRP 2020 is **not confirmed**.

**Safety distances.** No primary source gives one "safe distance" between an antenna and a home. Each site has a safety range (טווח בטיחות לבריאות הציבור) calculated for its permit under תמ"א 36/א, horizontal and vertical. The 2018 Knesset draft regulations exempt a rooftop facility from a building permit only if:
- the horizontal range is at most 4 m (6 m for shared or multi-technology sites);
- the range stays inside the plot;
- it is not on a preserved building, in a nature or antiquities site, or similar;
- the operator builds no more than 10 new exempt sites a year.

The often-quoted "300 m" appears in these regulations only as the radius within which the map must show other transmitters. It is not a safety distance. The final text of these regulations was not checked; only the committee draft of 8 May 2018 was read.

**Measurements on request.** An MoEP letter shows the ministry measured a home "following a public inquiry", including a week-long monitoring station. A resident can ask, but the request channel and any fee were not found on gov.il. Tel Aviv says a check at a private address is the resident's own responsibility, done through a licensed measurer.

**Monitoring scale.** These figures are from the 2020 report:
- MoEP monitors about 60,000 antennas.
- Active sites fell 20% from 2014 to 2020 through site sharing.
- Exposure around sites rose about 50% from 2013 to 2019, while mobile data grew 14.5-fold.

## 2. Power lines, transformers and substations (ELF)

- **The 4 mG figure.** It is real and official in wording, but its legal status is contested.
  - MoEP aims to minimise exposure above a **4 mG daily average on a peak-consumption day**, and states that this equals about **2 mG annual average**.
  - MoEP says the Ministry of Health determined that a prolonged exposure at or below 4 mG daily average is not a health risk.
  - More than 90% of Israeli homes are at or below 0.4 mG.
  - The 2020 report says the 2011 joint MoEP and MoH recommendation (2,000 mG momentary, 4 mG prolonged) was **never made a legally binding standard**. Yet the law makes the Expert Committee report the basis for the Supervisor's decisions in the electricity sector. Present both points.
- **Measurement method.**
  - MoEP's procedure (in force since 1 April 2017) normalises readings with the electricity company's current data for the line.
  - Example from an MoEP letter: a house 17.5 m from a 161 kV line read 6.6-15 mG after normalisation. MoEP found this did not meet its recommendation and passed it to the electricity company.
  - Distance alone does not settle the question.
- **Distances.**
  - **Planning clearances.** An electricity-company planning document published by Kfar Saba gives minimum horizontal distances from the line axis: 20 m for 161 kV, 35 m for 400 kV, 55 m for buildings with hazardous materials. These are planning clearances, not magnetic-field limits.
  - **The 50 m and 60 m claim.** "50 m from 161 kV, 60 m from 400 kV" comes from a commercial Q&A page and was **not found** in a primary source.
  - **Transformer rooms.** No official fixed distance was found; the practice is to measure.
- **Not verified.** Municipal reports cite a rule that school classrooms for young children should be planned at or below 4 mG at every seat. The age is given as under 15 in one version and under 10 in another. Only search snippets were seen, so this rule is not in `facts.json`.

## 3. Health science: what is established and what is not

**Radio frequency (antennas, phones)**
- **Classification.** IARC classified RF-EMF as Group 2B, possibly carcinogenic, on 31 May 2011 (Volume 102, 31 scientists). Its evidence ratings:
  - "limited" for glioma and acoustic neuroma in heavy phone users;
  - "inadequate" for exposure from radio, TV and telecom transmitters.
- **WHO.** No adverse health effects have been established from mobile phones. No short- or long-term effects have been shown from base-station signals.
- **WHO-commissioned systematic reviews, 2024-2025** (Environment International):
  - Phones and glioma, meningioma or acoustic neuroma: likely no increase, at **moderate** certainty.
  - Fixed transmitters and childhood leukaemia: likely no increase, at **moderate** certainty.
  - Fixed transmitters and children's brain tumours: may be no increase, at **low** certainty.
  - **No eligible studies at all** on fixed transmitters and the main adult tumours. That is the honest gap for adults living near antennas.
- **Animal review (Mevissen 2025).** The WHO-supported review found high-certainty evidence of increased heart schwannomas and gliomas in lab animals. The authors warned that this is hard to extrapolate to humans. The review is contested: regulators' commentaries list errors and note its heavy reliance on the NTP study.
- **Next step.** IARC's advisory group made RF a high priority for re-evaluation in 2025-2029, so the classification could change.

**ELF (power lines)**
- **The association.** IARC put ELF magnetic fields in Group 2B in 2001. The basis is pooled studies showing about **double the childhood-leukaemia rate above 0.3-0.4 µT (3-4 mG)** average at home.
- **Not shown to be causal.** WHO (EHC 238) judges the evidence not strong enough to be causal, citing problems such as selection bias. Only 1-4% of children live above 0.3 µT.
- **The EU view.** The EU's SCHEER (final opinion, 17 May 2024) also calls the evidence weak.
- **Other diseases.** WHO says the evidence suggests no causal link for heart disease or breast cancer.
- **A wording to avoid.** One MoEP letter paraphrases WHO with a "2 mG annual" figure. That wording is MoEP's, not WHO's, so do not print it as WHO's.

**Ministry of Health.** The guiding rule is the precautionary principle: simple, cheap steps to reduce exposure even without proof of harm. Practical advice from the MoH leaflet, as reproduced by a mobile operator:
- no phones for babies and toddlers;
- limit children's use;
- keep distance, cut time, and prefer good reception (TNUDA 2019).

A primary gov.il MoH page was **not read**.

## 4. Air quality

- **Law and regulations.**
  - Clean Air Law (חוק אוויר נקי, התשס"ח-2008), s.6.
  - Regulations: תקנות אוויר נקי (ערכי איכות אוויר) (הוראת שעה), התשע"א-2011, amended up to 2022 and listed as valid to 1 March 2027.
- **Three value types.** Target (policy goal), environmental (binding) and alert (immediate risk).
- **Israel against WHO 2021**, in µg/m³ (Israeli values from a Wikisource copy; verify on Nevo):

| Pollutant | Israeli target | Israeli binding (environmental) | WHO 2021 |
|---|---|---|---|
| PM2.5 annual | 5 | 25 | 5 |
| PM2.5 24 h | 15 | unclear in the copy (check) | 15 |
| NO2 annual | 10 | 40 | 10 |
| NO2 1 h | 200 | 200 (8 exceedances a year) | not used |

- **What the table shows.** Israel's target values copy WHO 2021. The binding limits are four to five times looser.
- **Gaps.** The size of the MoEP monitoring network and its live-data address were **not verified**. The complaint lines are *6911 (MoEP) and 1299.

## 5. Noise

- **The regulations.** תקנות למניעת מפגעים (רעש בלתי סביר), התש"ן-1990.
  - Day is 06:00-22:00; night is 22:00-06:00.
  - A home in a residential zone (type ב): 50 dB(A) for daytime noise lasting more than 9 hours, 40 dB(A) at night.
  - Schools and hospitals (type א): 45 dB(A) day, 35 dB(A) night.
  - Tonal or impulsive noise gets +5 dB.
  - Measured indoors with windows open.
  - The Table 1 columns were read from a scraped copy; verify them on Nevo.
- **What these rules do not cover.** Aircraft, trains, road vehicles and construction equipment have separate rules.
- **Airports.**
  - Ben Gurion has no take-offs 01:40-05:50 (closed 02:00-05:00 except Thursday nights and nights before holiday eves).
  - MoEP and the Airports Authority monitor noise continuously.
  - תמ"א 2/4 (1997) sets four noise zones (Ldn 60-65, 65-70 and higher), with insulation conditions for building.
  - The State Comptroller (2016) called the plan outdated.
  - A 2020 proposal to lower the insulation threshold from 65 to 60 dB and move to Lden was seen only in a search summary. Its status is **unknown**, so it is not in `facts.json`.
- **What a resident can do.**
  - Complain to the municipality, the MoEP district office or the Airports Authority's environmental centre.
  - Sue under the civil-claims law (1992).
- **Price gap.** No published Israeli price for an acoustic consultant was found.

## 6. Industry and fuel stations

- **Pollutant register (מפל"ס).** It is required by the 2012 PRTR law.
  - MoEP publishes it every year, with a map search by plant and pollutant.
  - The annual report goes to the Knesset committee.
  - It covers about 570 large plants (2016 figure).
  - The latest report PDF was downloaded, but its numbers did not extract.
- **Haifa Bay.** The State Comptroller calls it one of Israel's main pollution hotspots. The petrochemical relocation decision was **not verified**.
- **Fuel stations (תמ"א 18 amendment 4, 2016).** These distances come from media and a legal database; the plan text was **not read**.
  - 40 m from homes to a station with 4 fuelling positions.
  - Reducible to 20 m in urban renewal.
  - 80 m to public buildings, per a court-upheld decision.
  - The Ministry of Health objected because of benzene and was overruled.

## 7. Professionals and prices

All prices come from commercial pages; no company names are recorded.
- **Radiation survey.** Only a holder of an MoEP measurement-service permit may do measurements under the law. A standard apartment survey averages **500-650 NIS** and usually covers both RF and ELF (2026).
- **Home inspection (בדק בית).** Averages are 1,709 NIS (new apartment), 1,805 NIS (second-hand) and 1,788 NIS (pre-entry), with reported ranges of 1,320-2,750 NIS (2025 crowd data). Another list gives 1,300-1,500 NIS (3-4 rooms) up to 4,600-4,800 NIS (detached house), undated.
- **Not found:** published prices for acoustic consultants, environmental consultants, electricians doing magnetic shielding, or planning lawyers filing an objection to an antenna permit.

## 8. How a buyer or renter checks a property

1. **Look up the MoEP publication.** By law (s.19) it must show permitted radiation sources, their locations and measurement results.
2. **Ask the local planning committee for the antenna permit file.** It includes a 1:250 map with the safety ranges and all transmitters within 300 m.
3. **Order a survey from a licensed measurer** covering both RF and ELF, done on a weekday at peak hours. Ask that the ELF result be normalised to the line current, as MoEP does.
4. **Check the special cases.** Near a high-voltage line or a transformer room, ask MoEP or the electricity company for a measurement. MoEP has measured homes after public inquiries.
5. **Check noise and air.** Look at the airport noise zones (תמ"א 2/4) and the MoEP pollutant-register map for nearby plants.
6. **Check plans.** Mavat (mavat.iplan.gov.il) is the national plan search, but it was **not opened** in this session.

## 9. Rights

- **Objections.** Radiation is generally not a planning ground for an objection. Tel Aviv (2020) rejected a neighbour's objection on that basis, since radiation belongs to MoEP. The same decision conditioned the permit on an indemnity letter against section 197 compensation claims.
- **Permit history.** Between 2006 and 2009, 1,551 small facilities were added and only 444 had a building permit. The High Court then required permits until new regulations took effect.
- **Compensation.** Whether owners actually win section 197 compensation for loss of value from antennas, and how much, was **not established**.
- **Civil claims.** The civil-claims law covers non-ionizing radiation.

## Biggest honest gaps

1. No MoEP or MoH gov.il page could be read (HTTP 403). The 10%/30% ICNIRP rule rests on a well-sourced secondary report.
2. No primary source supports a single "safe distance" from an antenna or a power line. All commonly quoted metre figures are secondary or commercial.
3. The binding PM2.5 24-hour value and the noise Table 1 layout need checking against Nevo.
4. The fuel-station distances (תמ"א 18/4) and the airport-noise update were not read in the plan texts.
5. There are no published prices for acoustic or environmental consultants, shielding electricians or planning lawyers.
6. Section 197 compensation outcomes for antennas, the request channel for an MoEP measurement, the size of the air-monitoring network, and the Haifa Bay petrochemical decision were not verified.
