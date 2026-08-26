# Automated recipe validation

Generated: 2026-08-25T14:57:23.285Z

Base checklist definitions: 138
Expanded matrix cases: 9098
Green: 22 · Yellow: 0 · Orange: 0 · Red: 0

| ID | Light | Check | Evidence |
|---|---|---|---|
| DATA-PROJECT-001 | green | Project identity is owned by Aurelia Sde Dov | aurelia-sde-dov · רובע שדה דב, תל אביב-יפו |
| DATA-UNITS-002 | green | Exactly 320 unit records are present | 320 units |
| DATA-UNITS-003 | green | Every unit ID is unique | 320/320 unique |
| DATA-UNITS-004 | green | Every unit has a positive price, area and floor | price/sqm/floor scan |
| DATA-PLAN-005 | green | Every unit plan_id resolves to a drawing | 6 drawing IDs checked against 320 units |
| DATA-FAC-006 | green | Twelve facilities have valid hotspot coordinates | 12 facilities |
| DATA-ENV-007 | green | Twelve environment points have valid coordinates | 12 environment points |
| DATA-LANG-008 | green | Five language dictionaries exist | he, en, fr, ru, ar |
| DATA-LANG-009 | green | Every language includes the primary CTA | selectUnit + getPlans |
| BOM-SYS-010 | green | Seventeen engineering systems exist | 17 systems |
| BOM-ASM-011 | green | Thirty-three assemblies exist | 33 assemblies |
| BOM-CMP-012 | green | Eighty BOM components exist | 80 components |
| BOM-CMP-013 | green | Every component has code, specification, unit, quantity basis, performance, inspection and maintenance | 80 component records scanned |
| RECIPE-SEQ-014 | green | The page recipe has twenty ordered sections | 20 ordered sections |
| RECIPE-SEQ-015 | green | Every page section explains desktop, mobile, placement and SEO role | placement fields scan |
| SEO-TITLE-016 | green | SEO title is within the target display range | 60 characters |
| SEO-META-017 | green | Meta description is within the target display range | 147 characters |
| SEO-H1-018 | green | H1 contains both project identities and Sde Dov | Aurelia Sde Dov — אורליה שדה דב |
| WP-TYPE-019 | green | WordPress contract targets nadlan_project | wordpress-contract.json |
| WP-RUNTIME-020 | green | WordPress contract references NADLAN_SHOWROOM | wordpress-contract.json |
| CHECK-DEF-021 | green | Every base check has evidence and WordPress hooks | 138 definitions |
| CHECK-MATRIX-022 | green | The checklist expands into thousands of explicit cases | 9098 matrix cases |

Browser, public View Source and live WordPress evidence are separate evidence classes. They are never reported as green merely because the data package is valid.
