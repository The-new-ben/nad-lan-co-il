Report 2 — Keyword Master Universe + Workbook Division Plan

Plan-only. ~190 keyword rows across 9 clusters. All volumes/KD/CPC deliberately omitted — they belong in Report 3 (Semrush HE) and Report 4 (Semrush EN/intl) so we don't burn credits on uncalibrated guesses. Every row carries a verification flag; nothing here is publish-ready until Stage 1 trust cleanup passes.



A. Strategy Summary — What This Universe Is Trying To Win

NadLan's keyword universe is built to win three compounding positions at once:





Trusted Israeli real-estate intelligence layer — own informational + comparison + due-diligence queries that Yad2/Madlan under-serve (urban renewal, tax/mortgage explainers, project verification, professional vetting). This is where E-E-A-T + AI-search (AEO) wins; it's the moat.



Programmatic local marketplace surface — city × neighborhood × intent templates (buy / rent / new projects / yields) that scale once data + trust are real. Held at P2 until the trust gate passes; building these early would replay the fake-facade failure at city scale.



International investor funnel — English-language, high-CPC, high-LTV queries (Tel Aviv apartments, foreign-buyer tax, Sde Dov, Aliyah real estate). Smaller volume, outsized commercial value; requires LEGAL_REVIEW and an EN surface that doesn't exist yet.

Cross-cutting wins: AEO (questions in HE + EN structured as FAQPage / HowTo), tool-led acquisition (calculators with honest methodology), and a professional directory that is vetted, not seeded with demos.

What we are explicitly NOT trying to win in v1: listing-level long-tail ("3 חדרים רמת אביב להשכרה 4500 שח") — that is Yad2's commodity layer and requires real supply before SEO.



B. Workbook Tab Plan (Excel)

Workbook file: audits/keyword-universe/nadlan-keyword-workbook.xlsx.







Tab



Purpose



Source





00_README



Legend, flags, color codes, owners, refresh cadence, link to Report 0/1/2



Manual





01_Master



Full universe (this CSV). Single source of truth. Never edit downstream tabs — filter from here.



Section C CSV





02_HE_Buyer_Seller



Cluster 1 rows



Filter cluster=buyer_seller_core





03_Projects_Developers



Cluster 2 rows



Filter cluster=projects_developers





04_Intl_Investor_EN



Cluster 3 rows



Filter cluster=intl_investor





05_Tools_Calculators



Cluster 4 rows



Filter cluster=tools_calculators





06_Professionals



Cluster 5 rows



Filter cluster=professionals_directory





07_Urban_Renewal



Cluster 6 rows



Filter cluster=urban_renewal





08_Showroom_3D



Cluster 7 rows



Filter cluster=showroom_3d





09_Trust_Comparison



Cluster 8 rows



Filter cluster=trust_comparison





10_Local_Programmatic



Cluster 9 rows + city/neighborhood template grid



Filter cluster=local_programmatic





11_Semrush_HE



To be filled in Report 3: volume, KD, CPC, SERP features (HE database il)



Semrush





12_Semrush_EN_Intl



To be filled in Report 4: EN-language volumes (us, gb, il)



Semrush





13_Hub_Spoke_Map



After Semrush: hub URL ← spoke URLs, cannibalization check



Manual + Report 7





14_Editorial_Calendar



Sequenced publishing plan, owner, status, trust gate



Manual + Report 9





15_Legal_Review_Queue



All LEGAL_REVIEW rows pulled out for counsel sign-off



Filter on flag





16_Asset_Request_Queue



All REQUIRES_OFFICIAL_ASSET rows — developer/marketer outreach list



Filter on flag



C. Master CSV

keyword,language,cluster,subcluster,audience,country_market,intent,funnel_stage,priority,recommended_page_type,suggested_slug,primary_kpi,content_angle,trust_requirement,verification_flag,notes
דירות למכירה,he,buyer_seller_core,buy_general,buyer,IL,transactional,decision,P1,hub,/buy,organic_sessions,national buy hub linking to city hubs,real listings or honest empty-state,NEEDS_VERIFICATION,Yad2 territory; do not launch without supply
דירות למכירה תל אביב,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P1,city_hub,/buy/tel-aviv,organic_sessions,Tel Aviv buy hub with neighborhoods,real supply,NEEDS_VERIFICATION,
דירות למכירה רמת גן,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P1,city_hub,/buy/ramat-gan,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה ירושלים,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P1,city_hub,/buy/jerusalem,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה חיפה,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P1,city_hub,/buy/haifa,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה הרצליה,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P1,city_hub,/buy/herzliya,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה רעננה,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/raanana,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה כפר סבא,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/kfar-saba,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה פתח תקווה,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/petah-tikva,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה ראשון לציון,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/rishon-lezion,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה נתניה,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/netanya,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה באר שבע,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/beer-sheva,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות למכירה אשדוד,he,buyer_seller_core,buy_city,buyer,IL,transactional,decision,P2,city_hub,/buy/ashdod,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות להשכרה,he,buyer_seller_core,rent_general,renter,IL,transactional,decision,P1,hub,/rent,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות להשכרה תל אביב,he,buyer_seller_core,rent_city,renter,IL,transactional,decision,P1,city_hub,/rent/tel-aviv,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות להשכרה רמת גן,he,buyer_seller_core,rent_city,renter,IL,transactional,decision,P2,city_hub,/rent/ramat-gan,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות להשכרה ירושלים,he,buyer_seller_core,rent_city,renter,IL,transactional,decision,P2,city_hub,/rent/jerusalem,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות להשכרה חיפה,he,buyer_seller_core,rent_city,renter,IL,transactional,decision,P2,city_hub,/rent/haifa,organic_sessions,,real supply,NEEDS_VERIFICATION,
דירות מציאה,he,buyer_seller_core,deal_finder,buyer,IL,commercial,consideration,P2,feature,/deals,signups,smart-filter deals page,real supply,NEEDS_VERIFICATION,
דירות מתחת למחיר שוק,he,buyer_seller_core,deal_finder,buyer,IL,commercial,consideration,P2,feature,/below-market,signups,requires estimator integration,real supply + valid estimator,NEEDS_VERIFICATION,
איך למכור דירה,he,buyer_seller_core,seller_guide,seller,IL,informational,awareness,P1,guide,/sell/how-to-sell-apartment,organic_sessions,end-to-end seller playbook,reviewed by licensed agent,NEEDS_VERIFICATION|LEGAL_REVIEW,
מחיר דירה ממוצע,he,buyer_seller_core,market_data,buyer,IL,informational,awareness,P1,data_page,/market/average-prices,organic_sessions,,CBS / official data,OFFICIAL_SOURCE_REQUIRED,
מחירי דירות 2026,he,buyer_seller_core,market_data,buyer,IL,informational,awareness,P1,report,/market/prices-2026,organic_sessions,,CBS / official data,OFFICIAL_SOURCE_REQUIRED,
מדד מחירי דירות,he,buyer_seller_core,market_data,buyer,IL,informational,awareness,P2,data_page,/market/price-index,organic_sessions,,CBS,OFFICIAL_SOURCE_REQUIRED,
שמאות דירה,he,buyer_seller_core,valuation,seller,IL,commercial,consideration,P1,tool_landing,/valuation,tool_starts,routes into estimator,licensed appraiser disclaimer,LEGAL_REVIEW,
כמה שווה הדירה שלי,he,buyer_seller_core,valuation,seller,IL,commercial,decision,P0,tool,/property-value-estimator,tool_completions,seller-facing estimator,methodology + disclaimer,LEGAL_REVIEW|NEEDS_VERIFICATION,Existing URL — fix per Report 1 first
חוזה שכירות לדוגמא,he,buyer_seller_core,seller_guide,renter,IL,informational,consideration,P1,template,/rent/lease-template,downloads,downloadable template,attorney-reviewed template,LEGAL_REVIEW,
זיכרון דברים דירה,he,buyer_seller_core,seller_guide,buyer,IL,informational,consideration,P1,guide,/buy/memorandum-of-understanding,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
ביטול עסקת דירה,he,buyer_seller_core,seller_guide,buyer,IL,informational,decision,P2,guide,/buy/cancel-contract,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
זכויות קונה דירה מקבלן,he,buyer_seller_core,buyer_rights,buyer,IL,informational,consideration,P1,guide,/buy/rights-from-developer,organic_sessions,חוק המכר דירות,attorney-reviewed,LEGAL_REVIEW,
פרויקטים חדשים,he,projects_developers,new_projects_general,buyer,IL,commercial,consideration,P0,hub,/projects,organic_sessions,national new-projects hub,developer-verified data,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים תל אביב,he,projects_developers,new_projects_city,buyer,IL,commercial,consideration,P0,city_hub,/projects/tel-aviv,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים שדה דב,he,projects_developers,new_projects_neighborhood,buyer,IL,commercial,decision,P0,area_hub,/projects/sde-dov,organic_sessions,Sde Dov master area,official municipal + developer,REQUIRES_OFFICIAL_ASSET|OFFICIAL_SOURCE_REQUIRED,
פרויקטים חדשים רמת גן,he,projects_developers,new_projects_city,buyer,IL,commercial,consideration,P1,city_hub,/projects/ramat-gan,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים ירושלים,he,projects_developers,new_projects_city,buyer,IL,commercial,consideration,P1,city_hub,/projects/jerusalem,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים חיפה,he,projects_developers,new_projects_city,buyer,IL,commercial,consideration,P1,city_hub,/projects/haifa,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים נתניה,he,projects_developers,new_projects_city,buyer,IL,commercial,consideration,P1,city_hub,/projects/netanya,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים הרצליה,he,projects_developers,new_projects_city,buyer,IL,commercial,consideration,P1,city_hub,/projects/herzliya,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
דירות מקבלן,he,projects_developers,from_developer,buyer,IL,commercial,decision,P1,hub,/from-developer,organic_sessions,,developer-verified,REQUIRES_OFFICIAL_ASSET,
דירה מקבלן או יד שניה,he,projects_developers,from_developer,buyer,IL,comparison,consideration,P1,guide,/from-developer/vs-second-hand,organic_sessions,,balanced editorial,NEEDS_VERIFICATION,
דירות על הנייר,he,projects_developers,pre_sale,buyer,IL,commercial,consideration,P1,guide,/pre-sale,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
פרויקט דמרי שדה דב,he,projects_developers,project_specific,buyer,IL,navigational,decision,P0,project_page,/projects/dimri-yama-sde-dov,leads,Dimri Yama Sde Dov,official developer data,REQUIRES_OFFICIAL_ASSET,Existing URL
פרויקט רינבו תל אביב,he,projects_developers,project_specific,buyer,IL,navigational,decision,P0,project_page,/projects/rainbow-tel-aviv,leads,Rainbow Tel Aviv,official developer data,REQUIRES_OFFICIAL_ASSET,Existing URL
חברות בניה בישראל,he,projects_developers,developers,buyer,IL,informational,consideration,P2,directory,/developers,organic_sessions,verified developer directory,company registry,OFFICIAL_SOURCE_REQUIRED,
דירוג חברות בניה,he,projects_developers,developers,buyer,IL,comparison,consideration,P2,report,/developers/ranking,organic_sessions,,methodology + data,OFFICIAL_SOURCE_REQUIRED|LEGAL_REVIEW,
חברת דמרי,he,projects_developers,developers,buyer,IL,navigational,consideration,P1,developer_page,/developers/dimri,organic_sessions,Dimri profile,official + public filings,OFFICIAL_SOURCE_REQUIRED,
מחירון דירות חדשות,he,projects_developers,price_list,buyer,IL,commercial,decision,P1,data_page,/projects/price-list,organic_sessions,,developer pricing,REQUIRES_OFFICIAL_ASSET,
buying property in israel,en,intl_investor,intl_overview,investor,INTL,informational,awareness,P0,guide,/en/buy-property-israel,organic_sessions,top-of-funnel intl pillar,attorney-reviewed,LEGAL_REVIEW,
real estate israel,en,intl_investor,intl_overview,investor,INTL,informational,awareness,P0,hub,/en,organic_sessions,EN homepage,EN site stub required,NEEDS_VERIFICATION,
tel aviv apartments for sale,en,intl_investor,intl_city,investor,INTL,commercial,decision,P0,city_hub,/en/buy/tel-aviv,leads,Tel Aviv intl buy hub,real supply,NEEDS_VERIFICATION,
jerusalem apartments for sale,en,intl_investor,intl_city,investor,INTL,commercial,decision,P1,city_hub,/en/buy/jerusalem,leads,,real supply,NEEDS_VERIFICATION,
herzliya pituach real estate,en,intl_investor,intl_city,investor,INTL,commercial,decision,P1,city_hub,/en/buy/herzliya-pituach,leads,Anglo-friendly neighborhood,real supply,NEEDS_VERIFICATION,
netanya apartments english speakers,en,intl_investor,intl_city,investor,INTL,commercial,decision,P1,city_hub,/en/buy/netanya,leads,,real supply,NEEDS_VERIFICATION,
raanana real estate english,en,intl_investor,intl_city,investor,INTL,commercial,decision,P1,city_hub,/en/buy/raanana,leads,,real supply,NEEDS_VERIFICATION,
sde dov tel aviv project,en,intl_investor,intl_project,investor,INTL,navigational,decision,P0,project_page,/en/projects/sde-dov,leads,intl-facing Sde Dov,official developer,REQUIRES_OFFICIAL_ASSET,
new construction tel aviv,en,intl_investor,intl_projects,investor,INTL,commercial,consideration,P0,hub,/en/new-construction/tel-aviv,leads,,developer-verified,REQUIRES_OFFICIAL_ASSET,
foreign buyer purchase tax israel,en,intl_investor,intl_tax,investor,INTL,informational,consideration,P0,guide,/en/tax/foreign-buyer-purchase-tax,organic_sessions,מס רכישה לתושב חוץ,attorney + CPA reviewed,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
mortgage in israel for foreigners,en,intl_investor,intl_finance,investor,INTL,informational,consideration,P0,guide,/en/mortgage/foreign-buyers,leads,,licensed advisor reviewed,LEGAL_REVIEW,
israeli real estate lawyer english,en,intl_investor,intl_professionals,investor,INTL,commercial,decision,P1,directory,/en/professionals/lawyers,leads,vetted EN-speaking lawyers,license verification,REQUIRES_OFFICIAL_ASSET,
buying apartment israel aliyah,en,intl_investor,intl_aliyah,investor,INTL,informational,awareness,P1,guide,/en/aliyah/buying-apartment,organic_sessions,,partner with Nefesh / org review,LEGAL_REVIEW,
investing in tel aviv real estate,en,intl_investor,intl_invest,investor,INTL,commercial,consideration,P1,guide,/en/invest/tel-aviv,leads,yield + appreciation data,OFFICIAL CBS data,OFFICIAL_SOURCE_REQUIRED,
rental yield israel,en,intl_investor,intl_invest,investor,INTL,informational,consideration,P1,data_page,/en/invest/rental-yields,organic_sessions,,CBS + market data,OFFICIAL_SOURCE_REQUIRED,
israel property market 2026,en,intl_investor,intl_market,investor,INTL,informational,awareness,P1,report,/en/market/2026,organic_sessions,annual market report,CBS + Bank of Israel,OFFICIAL_SOURCE_REQUIRED,
tama 38 explained,en,intl_investor,intl_renewal,investor,INTL,informational,awareness,P1,guide,/en/urban-renewal/tama-38,organic_sessions,EN explainer of TAMA 38,attorney-reviewed,LEGAL_REVIEW,
pinui binui meaning,en,intl_investor,intl_renewal,investor,INTL,informational,awareness,P2,guide,/en/urban-renewal/pinui-binui,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
how to buy property in israel from usa,en,intl_investor,intl_process,investor,US,informational,consideration,P1,guide,/en/buy/from-usa,leads,US-buyer playbook,attorney + CPA reviewed,LEGAL_REVIEW,
how to buy property in israel from uk,en,intl_investor,intl_process,investor,UK,informational,consideration,P2,guide,/en/buy/from-uk,leads,,attorney reviewed,LEGAL_REVIEW,
how to buy property in israel from france,en,intl_investor,intl_process,investor,FR,informational,consideration,P2,guide,/en/buy/from-france,leads,,attorney reviewed,LEGAL_REVIEW,
israeli mortgage calculator english,en,intl_investor,intl_tools,investor,INTL,commercial,decision,P1,tool,/en/tools/mortgage-calculator,tool_completions,,disclaimer,LEGAL_REVIEW,
purchase tax calculator israel,en,intl_investor,intl_tools,investor,INTL,commercial,decision,P0,tool,/en/tools/purchase-tax-calculator,tool_completions,,Tax Authority brackets,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מחשבון משכנתא,he,tools_calculators,mortgage,buyer,IL,transactional,decision,P0,tool,/tools/mortgage-calculator,tool_completions,flagship calculator,licensed advisor disclaimer,LEGAL_REVIEW,
החזר משכנתא חודשי,he,tools_calculators,mortgage,buyer,IL,informational,consideration,P1,tool,/tools/monthly-payment,tool_completions,,disclaimer,LEGAL_REVIEW,
מחשבון מס רכישה,he,tools_calculators,tax,buyer,IL,transactional,decision,P0,tool,/tools/purchase-tax-calculator,tool_completions,,Tax Authority brackets,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מס רכישה דירה ראשונה,he,tools_calculators,tax,buyer,IL,informational,consideration,P0,guide,/tax/purchase-tax-first-home,organic_sessions,,Tax Authority,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מס רכישה דירה שניה,he,tools_calculators,tax,investor,IL,informational,consideration,P0,guide,/tax/purchase-tax-second-home,organic_sessions,,Tax Authority,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מס שבח,he,tools_calculators,tax,seller,IL,informational,consideration,P0,guide,/tax/capital-gains,organic_sessions,,Tax Authority,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מחשבון מס שבח,he,tools_calculators,tax,seller,IL,transactional,decision,P0,tool,/tools/capital-gains-calculator,tool_completions,,Tax Authority,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מחשבון תשואה דירה,he,tools_calculators,yield,investor,IL,transactional,decision,P0,tool,/tools/rental-yield-calculator,tool_completions,,methodology disclosure,NEEDS_VERIFICATION,
תשואה ממוצעת דירה תל אביב,he,tools_calculators,yield,investor,IL,informational,consideration,P1,data_page,/data/yields/tel-aviv,organic_sessions,,CBS + market data,OFFICIAL_SOURCE_REQUIRED,
מחשבון עלות שיפוץ,he,tools_calculators,renovation,buyer,IL,commercial,consideration,P1,tool,/tools/renovation-calculator,tool_completions,,contractor data,NEEDS_VERIFICATION,
עלות שיפוץ דירה לפי מטר,he,tools_calculators,renovation,buyer,IL,informational,consideration,P1,guide,/guides/renovation-cost-per-sqm,organic_sessions,,contractor survey,NEEDS_VERIFICATION,
מחשבון הון עצמי,he,tools_calculators,mortgage,buyer,IL,transactional,decision,P1,tool,/tools/equity-calculator,tool_completions,,Bank of Israel LTV rules,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מחשבון יכולת החזר,he,tools_calculators,mortgage,buyer,IL,transactional,decision,P1,tool,/tools/affordability-calculator,tool_completions,,disclaimer,LEGAL_REVIEW,
מחשבון עמלת פירעון מוקדם,he,tools_calculators,mortgage,buyer,IL,transactional,decision,P1,tool,/tools/early-repayment-fee,tool_completions,,Bank of Israel formula,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
תהליך קניית דירה,he,tools_calculators,buying_process,buyer,IL,informational,awareness,P0,pillar,/guides/buying-process,organic_sessions,step-by-step pillar,attorney-reviewed,LEGAL_REVIEW,
שלבים בקניית דירה,he,tools_calculators,buying_process,buyer,IL,informational,awareness,P1,guide,/guides/buying-steps,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
מסמכים לקניית דירה,he,tools_calculators,buying_process,buyer,IL,informational,consideration,P1,guide,/guides/buying-documents,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
בדיקת נסח טאבו,he,tools_calculators,due_diligence,buyer,IL,informational,decision,P1,guide,/guides/tabu-extract,organic_sessions,,attorney-reviewed,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
נסח טאבו אונליין,he,tools_calculators,due_diligence,buyer,IL,navigational,decision,P2,guide,/guides/tabu-online,organic_sessions,,Land Registry,OFFICIAL_SOURCE_REQUIRED,
מתווכים תל אביב,he,professionals_directory,realtors,buyer,IL,local,decision,P1,directory,/professionals/realtors/tel-aviv,leads,,license verification,REQUIRES_OFFICIAL_ASSET,
מתווך דירות,he,professionals_directory,realtors,buyer,IL,commercial,decision,P1,directory,/professionals/realtors,leads,,license verification,REQUIRES_OFFICIAL_ASSET,
מתווכים מומלצים,he,professionals_directory,realtors,buyer,IL,comparison,decision,P1,directory,/professionals/realtors/recommended,leads,methodology required,license + review policy,REQUIRES_OFFICIAL_ASSET|LEGAL_REVIEW,
דמי תיווך,he,professionals_directory,realtors,buyer,IL,informational,consideration,P1,guide,/guides/realtor-fees,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
עורך דין מקרקעין,he,professionals_directory,lawyers,buyer,IL,commercial,decision,P1,directory,/professionals/lawyers,leads,,bar association verification,REQUIRES_OFFICIAL_ASSET,
עורך דין מקרקעין תל אביב,he,professionals_directory,lawyers,buyer,IL,local,decision,P1,directory,/professionals/lawyers/tel-aviv,leads,,bar verification,REQUIRES_OFFICIAL_ASSET,
עורך דין מקרקעין ירושלים,he,professionals_directory,lawyers,buyer,IL,local,decision,P2,directory,/professionals/lawyers/jerusalem,leads,,bar verification,REQUIRES_OFFICIAL_ASSET,
שכר טרחת עורך דין דירה,he,professionals_directory,lawyers,buyer,IL,informational,consideration,P1,guide,/guides/lawyer-fees-apartment,organic_sessions,,bar guidance,LEGAL_REVIEW,
יועץ משכנתאות,he,professionals_directory,mortgage_advisors,buyer,IL,commercial,decision,P1,directory,/professionals/mortgage-advisors,leads,,license verification,REQUIRES_OFFICIAL_ASSET,
יועץ משכנתאות מומלץ,he,professionals_directory,mortgage_advisors,buyer,IL,comparison,decision,P1,directory,/professionals/mortgage-advisors/recommended,leads,,license + reviews,REQUIRES_OFFICIAL_ASSET,
שמאי מקרקעין,he,professionals_directory,appraisers,seller,IL,commercial,decision,P1,directory,/professionals/appraisers,leads,,council of appraisers verification,REQUIRES_OFFICIAL_ASSET,
שמאי מקרקעין מחיר,he,professionals_directory,appraisers,seller,IL,informational,consideration,P2,guide,/guides/appraiser-cost,organic_sessions,,survey,NEEDS_VERIFICATION,
בודק דירות,he,professionals_directory,inspectors,buyer,IL,commercial,decision,P1,directory,/professionals/inspectors,leads,inspection report standard,credentials check,REQUIRES_OFFICIAL_ASSET,
בדק בית,he,professionals_directory,inspectors,buyer,IL,commercial,decision,P1,directory,/professionals/home-inspection,leads,,credentials check,REQUIRES_OFFICIAL_ASSET,
ליקויי בנייה,he,professionals_directory,inspectors,buyer,IL,informational,consideration,P2,guide,/guides/construction-defects,organic_sessions,,attorney + engineer,LEGAL_REVIEW,
מעצב פנים דירה,he,professionals_directory,designers,buyer,IL,commercial,decision,P2,directory,/professionals/interior-designers,leads,,portfolio verification,NEEDS_VERIFICATION,
אדריכל דירה,he,professionals_directory,designers,buyer,IL,commercial,decision,P2,directory,/professionals/architects,leads,,architects registry,REQUIRES_OFFICIAL_ASSET,
קבלן שיפוצים,he,professionals_directory,contractors,buyer,IL,commercial,decision,P1,directory,/professionals/renovation-contractors,leads,,contractor registry,REQUIRES_OFFICIAL_ASSET,
קבלן שיפוצים תל אביב,he,professionals_directory,contractors,buyer,IL,local,decision,P2,directory,/professionals/renovation-contractors/tel-aviv,leads,,contractor registry,REQUIRES_OFFICIAL_ASSET,
איך לבחור מתווך,he,professionals_directory,realtors,buyer,IL,informational,consideration,P1,guide,/guides/choose-realtor,organic_sessions,,editorial,NEEDS_VERIFICATION,
איך לבחור עורך דין מקרקעין,he,professionals_directory,lawyers,buyer,IL,informational,consideration,P1,guide,/guides/choose-real-estate-lawyer,organic_sessions,,editorial,LEGAL_REVIEW,
תמא 38,he,urban_renewal,tama38_general,owner,IL,informational,awareness,P0,pillar,/urban-renewal/tama-38,organic_sessions,TAMA 38 pillar,attorney-reviewed,LEGAL_REVIEW,
תמא 38 1,he,urban_renewal,tama38_variants,owner,IL,informational,awareness,P1,guide,/urban-renewal/tama-38-1,organic_sessions,strengthening,attorney-reviewed,LEGAL_REVIEW,
תמא 38 2,he,urban_renewal,tama38_variants,owner,IL,informational,awareness,P1,guide,/urban-renewal/tama-38-2,organic_sessions,demolish-rebuild,attorney-reviewed,LEGAL_REVIEW,
תמא 38 זכויות דיירים,he,urban_renewal,tama38_rights,owner,IL,informational,consideration,P0,guide,/urban-renewal/tama-38-tenant-rights,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
תמא 38 מיסוי,he,urban_renewal,tama38_tax,owner,IL,informational,consideration,P1,guide,/urban-renewal/tama-38-tax,organic_sessions,,CPA + attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
פינוי בינוי,he,urban_renewal,pinui_binui_general,owner,IL,informational,awareness,P0,pillar,/urban-renewal/pinui-binui,organic_sessions,Pinui-Binui pillar,attorney-reviewed,LEGAL_REVIEW,
פינוי בינוי זכויות דיירים,he,urban_renewal,pinui_binui_rights,owner,IL,informational,consideration,P0,guide,/urban-renewal/pinui-binui-tenant-rights,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
התחדשות עירונית,he,urban_renewal,renewal_general,owner,IL,informational,awareness,P0,hub,/urban-renewal,organic_sessions,renewal hub,attorney + municipal,LEGAL_REVIEW,
התחדשות עירונית תל אביב,he,urban_renewal,renewal_city,owner,IL,local,consideration,P1,city_hub,/urban-renewal/tel-aviv,organic_sessions,,municipal data,OFFICIAL_SOURCE_REQUIRED,
התחדשות עירונית רמת גן,he,urban_renewal,renewal_city,owner,IL,local,consideration,P2,city_hub,/urban-renewal/ramat-gan,organic_sessions,,municipal data,OFFICIAL_SOURCE_REQUIRED,
היתר בניה,he,urban_renewal,permits,owner,IL,informational,consideration,P1,guide,/guides/building-permit,organic_sessions,,municipal + attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
תוכנית בניין עיר,he,urban_renewal,planning,owner,IL,informational,consideration,P1,guide,/guides/city-master-plan,organic_sessions,,municipal,OFFICIAL_SOURCE_REQUIRED,
תב"ע,he,urban_renewal,planning,owner,IL,informational,consideration,P1,guide,/guides/tabaa,organic_sessions,,municipal,OFFICIAL_SOURCE_REQUIRED,
ועדה מקומית לתכנון ובניה,he,urban_renewal,planning,owner,IL,informational,consideration,P2,guide,/guides/local-planning-committee,organic_sessions,,municipal,OFFICIAL_SOURCE_REQUIRED,
חוק התחדשות עירונית,he,urban_renewal,renewal_law,owner,IL,informational,consideration,P2,guide,/urban-renewal/law,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
דייר סרבן,he,urban_renewal,pinui_binui_rights,owner,IL,informational,consideration,P1,guide,/urban-renewal/refusing-tenant,organic_sessions,,attorney-reviewed,LEGAL_REVIEW,
סיור וירטואלי דירה,he,showroom_3d,virtual_tour,buyer,IL,commercial,consideration,P1,feature,/features/virtual-tours,signups,3D tour feature page,real tour assets,REQUIRES_OFFICIAL_ASSET,
מפת פרויקטים,he,showroom_3d,map_discovery,buyer,IL,commercial,consideration,P1,feature,/map,signups,Mapbox project explorer,verified project data,REQUIRES_OFFICIAL_ASSET,
מפת התחדשות עירונית,he,showroom_3d,map_discovery,owner,IL,informational,consideration,P1,feature,/urban-renewal/map,signups,renewal map,municipal data,OFFICIAL_SOURCE_REQUIRED,
מפת מחירי דירות,he,showroom_3d,map_discovery,buyer,IL,informational,consideration,P1,feature,/map/prices,signups,price heatmap,CBS / transaction data,OFFICIAL_SOURCE_REQUIRED,
הדמיה תלת מימד דירה,he,showroom_3d,3d_renders,buyer,IL,informational,consideration,P2,guide,/guides/3d-renders,organic_sessions,concept vs official explainer,disclaimer mandatory,REQUIRES_OFFICIAL_ASSET,
showroom פרויקט,he,showroom_3d,showroom,buyer,IL,navigational,consideration,P1,feature,/features/showroom,signups,project showroom feature,state-machine compliant,REQUIRES_OFFICIAL_ASSET,
3d apartment tour israel,en,showroom_3d,virtual_tour,investor,INTL,commercial,consideration,P2,feature,/en/features/virtual-tours,signups,EN intl-facing,real assets,REQUIRES_OFFICIAL_ASSET,
interactive map israel real estate,en,showroom_3d,map_discovery,investor,INTL,commercial,consideration,P2,feature,/en/map,signups,,verified data,REQUIRES_OFFICIAL_ASSET,
הדמיה לעומת תמונה אמיתית,he,showroom_3d,trust,buyer,IL,due_diligence,consideration,P1,guide,/guides/render-vs-photo,organic_sessions,trust explainer,editorial,NEEDS_VERIFICATION,
יד2 או מדלן,he,trust_comparison,platform_compare,buyer,IL,comparison,consideration,P1,guide,/compare/yad2-vs-madlan,organic_sessions,balanced comparison,editorial integrity,NEEDS_VERIFICATION,
האתר הטוב ביותר לחיפוש דירה,he,trust_comparison,platform_compare,buyer,IL,comparison,consideration,P1,guide,/compare/best-real-estate-sites,organic_sessions,,editorial,NEEDS_VERIFICATION,
ביקורות יד2,he,trust_comparison,platform_reviews,buyer,IL,due_diligence,consideration,P2,guide,/reviews/yad2,organic_sessions,,editorial,NEEDS_VERIFICATION,
ביקורות מדלן,he,trust_comparison,platform_reviews,buyer,IL,due_diligence,consideration,P2,guide,/reviews/madlan,organic_sessions,,editorial,NEEDS_VERIFICATION,
הונאות נדל"ן,he,trust_comparison,scams,buyer,IL,due_diligence,awareness,P0,guide,/guides/real-estate-scams,organic_sessions,top scam patterns,attorney + police data,LEGAL_REVIEW,
הונאת שכירות,he,trust_comparison,scams,renter,IL,due_diligence,awareness,P1,guide,/guides/rental-scams,organic_sessions,,editorial,LEGAL_REVIEW,
איך לבדוק קבלן,he,trust_comparison,due_diligence,buyer,IL,due_diligence,decision,P0,guide,/guides/vet-developer,organic_sessions,,Registrar of Contractors,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
פנקס קבלנים,he,trust_comparison,due_diligence,buyer,IL,navigational,decision,P1,guide,/guides/contractor-registry,organic_sessions,,Registrar of Contractors,OFFICIAL_SOURCE_REQUIRED,
איך לבדוק דירה לפני קניה,he,trust_comparison,due_diligence,buyer,IL,due_diligence,decision,P0,guide,/guides/pre-purchase-checklist,organic_sessions,,attorney + inspector,LEGAL_REVIEW,
דירה עם עיקול,he,trust_comparison,due_diligence,buyer,IL,due_diligence,decision,P1,guide,/guides/apartment-with-lien,organic_sessions,,attorney,LEGAL_REVIEW,
נדלן ישראל אמין,he,trust_comparison,platform_compare,buyer,IL,comparison,consideration,P2,guide,/compare/trusted-real-estate-platforms,organic_sessions,,editorial,NEEDS_VERIFICATION,
best real estate website israel,en,trust_comparison,platform_compare,investor,INTL,comparison,consideration,P1,guide,/en/compare/best-real-estate-platforms,organic_sessions,,editorial,NEEDS_VERIFICATION,
yad2 in english,en,trust_comparison,platform_compare,investor,INTL,navigational,consideration,P2,guide,/en/guides/yad2-english,organic_sessions,,editorial,NEEDS_VERIFICATION,
is it safe to buy property in israel,en,trust_comparison,intl_due_diligence,investor,INTL,due_diligence,awareness,P1,guide,/en/guides/safety-buying-israel,organic_sessions,,attorney + editorial,LEGAL_REVIEW,
real estate scams israel,en,trust_comparison,intl_due_diligence,investor,INTL,due_diligence,awareness,P1,guide,/en/guides/scams,organic_sessions,,attorney + editorial,LEGAL_REVIEW,
דירות למכירה {city},he,local_programmatic,buy_template,buyer,IL,transactional,decision,P2,template,/buy/{city},organic_sessions,template — Tel Aviv/JLM/Haifa/Ramat Gan/Herzliya/Raanana/Kfar Saba/Petah Tikva/Rishon LeZion/Netanya/Beer Sheva/Ashdod/Ashkelon/Rehovot/Holon/Bat Yam/Givatayim/Modiin/Ramat HaSharon,real supply,NEEDS_VERIFICATION,Expand into 20+ rows once trust passes
דירות להשכרה {city},he,local_programmatic,rent_template,renter,IL,transactional,decision,P2,template,/rent/{city},organic_sessions,same city list,real supply,NEEDS_VERIFICATION,
פרויקטים חדשים {city},he,local_programmatic,projects_template,buyer,IL,commercial,consideration,P2,template,/projects/{city},organic_sessions,same city list,developer-verified,REQUIRES_OFFICIAL_ASSET,
מחירי דירות {city},he,local_programmatic,prices_template,buyer,IL,informational,awareness,P2,template,/market/prices/{city},organic_sessions,city price report,CBS,OFFICIAL_SOURCE_REQUIRED,
תשואה ממוצעת {city},he,local_programmatic,yield_template,investor,IL,informational,consideration,P2,template,/data/yields/{city},organic_sessions,,CBS + market,OFFICIAL_SOURCE_REQUIRED,
מתווכים {city},he,local_programmatic,realtors_template,buyer,IL,local,decision,P2,template,/professionals/realtors/{city},leads,,license verification,REQUIRES_OFFICIAL_ASSET,
עורך דין מקרקעין {city},he,local_programmatic,lawyers_template,buyer,IL,local,decision,P2,template,/professionals/lawyers/{city},leads,,bar verification,REQUIRES_OFFICIAL_ASSET,
שמאי מקרקעין {city},he,local_programmatic,appraisers_template,seller,IL,local,decision,P3,template,/professionals/appraisers/{city},leads,,council verification,REQUIRES_OFFICIAL_ASSET,
התחדשות עירונית {city},he,local_programmatic,renewal_template,owner,IL,local,consideration,P2,template,/urban-renewal/{city},organic_sessions,,municipal data,OFFICIAL_SOURCE_REQUIRED,
דירות למכירה {neighborhood} {city},he,local_programmatic,buy_neighborhood_template,buyer,IL,transactional,decision,P3,template,/buy/{city}/{neighborhood},organic_sessions,gen after city hubs,real supply,NEEDS_VERIFICATION,Florentin/Neve Tzedek/Sde Dov/Ramat Aviv/Old North/Kiryat Yovel etc.
דירות להשכרה {neighborhood} {city},he,local_programmatic,rent_neighborhood_template,renter,IL,transactional,decision,P3,template,/rent/{city}/{neighborhood},organic_sessions,,real supply,NEEDS_VERIFICATION,
{city} apartments for sale,en,local_programmatic,intl_buy_template,investor,INTL,commercial,decision,P3,template,/en/buy/{city},leads,Tel Aviv/JLM/Herzliya/Netanya/Raanana/Haifa,real supply,NEEDS_VERIFICATION,
{city} apartments for rent,en,local_programmatic,intl_rent_template,renter,INTL,commercial,decision,P3,template,/en/rent/{city},leads,same intl cities,real supply,NEEDS_VERIFICATION,
new projects {city} israel,en,local_programmatic,intl_projects_template,investor,INTL,commercial,consideration,P3,template,/en/projects/{city},leads,,developer-verified,REQUIRES_OFFICIAL_ASSET,
real estate lawyer {city} israel,en,local_programmatic,intl_lawyers_template,investor,INTL,local,decision,P3,template,/en/professionals/lawyers/{city},leads,,bar verification,REQUIRES_OFFICIAL_ASSET,
mortgage advisor {city} israel,en,local_programmatic,intl_mortgage_template,investor,INTL,local,decision,P3,template,/en/professionals/mortgage-advisors/{city},leads,,license,REQUIRES_OFFICIAL_ASSET,
nadlan,he,buyer_seller_core,brand,buyer,IL,navigational,awareness,P1,brand,/,direct,brand defense,brand,NEEDS_VERIFICATION,
nadlan israel,en,intl_investor,brand,investor,INTL,navigational,awareness,P1,brand,/en,direct,brand defense,brand,NEEDS_VERIFICATION,
נדלן,he,buyer_seller_core,category,buyer,IL,navigational,awareness,P1,hub,/,organic_sessions,category capture,brand,NEEDS_VERIFICATION,
שוק הנדלן בישראל,he,buyer_seller_core,market_data,buyer,IL,informational,awareness,P1,report,/market/overview,organic_sessions,annual overview,CBS + Bank of Israel,OFFICIAL_SOURCE_REQUIRED,
מחירי שכירות תל אביב,he,buyer_seller_core,market_data,renter,IL,informational,awareness,P1,data_page,/market/rent-prices/tel-aviv,organic_sessions,,CBS,OFFICIAL_SOURCE_REQUIRED,
מחירי שכירות ירושלים,he,buyer_seller_core,market_data,renter,IL,informational,awareness,P2,data_page,/market/rent-prices/jerusalem,organic_sessions,,CBS,OFFICIAL_SOURCE_REQUIRED,
שטח דירה ברוטו נטו,he,buyer_seller_core,buyer_guide,buyer,IL,informational,consideration,P2,guide,/guides/gross-vs-net-area,organic_sessions,,attorney + appraiser,LEGAL_REVIEW,
מרפסת שמש,he,buyer_seller_core,buyer_guide,buyer,IL,informational,consideration,P3,guide,/guides/sun-balcony,organic_sessions,,editorial,NEEDS_VERIFICATION,
דירת גן,he,buyer_seller_core,buyer_guide,buyer,IL,informational,consideration,P3,guide,/guides/garden-apartment,organic_sessions,,editorial,NEEDS_VERIFICATION,
דירת גג,he,buyer_seller_core,buyer_guide,buyer,IL,informational,consideration,P3,guide,/guides/penthouse,organic_sessions,,editorial,NEEDS_VERIFICATION,
דירת מיני פנטהאוז,he,buyer_seller_core,buyer_guide,buyer,IL,informational,consideration,P3,guide,/guides/mini-penthouse,organic_sessions,,editorial,NEEDS_VERIFICATION,
ועד בית,he,buyer_seller_core,buyer_guide,owner,IL,informational,consideration,P2,guide,/guides/building-committee,organic_sessions,,attorney,LEGAL_REVIEW,
ארנונה,he,buyer_seller_core,ownership,owner,IL,informational,consideration,P2,guide,/guides/property-tax,organic_sessions,,municipal + attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
ביטוח דירה,he,buyer_seller_core,ownership,owner,IL,commercial,consideration,P2,guide,/guides/home-insurance,organic_sessions,,licensed insurer,LEGAL_REVIEW,
משכנתא לדירה ראשונה,he,tools_calculators,mortgage,buyer,IL,informational,consideration,P0,guide,/mortgage/first-home,organic_sessions,,advisor + Bank of Israel,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
משכנתא לדירה שניה,he,tools_calculators,mortgage,investor,IL,informational,consideration,P1,guide,/mortgage/second-home,organic_sessions,,advisor,LEGAL_REVIEW,
מסלולי משכנתא,he,tools_calculators,mortgage,buyer,IL,informational,consideration,P1,guide,/mortgage/tracks,organic_sessions,,advisor,LEGAL_REVIEW,
ריבית משכנתא היום,he,tools_calculators,mortgage,buyer,IL,informational,decision,P1,data_page,/mortgage/rates-today,organic_sessions,,Bank of Israel daily,OFFICIAL_SOURCE_REQUIRED,
מחיר למשתכן,he,projects_developers,subsidized,buyer,IL,informational,consideration,P1,guide,/guides/mehir-lamishtaken,organic_sessions,,Housing Ministry,OFFICIAL_SOURCE_REQUIRED|LEGAL_REVIEW,
דיור בהישג יד,he,projects_developers,subsidized,buyer,IL,informational,consideration,P2,guide,/guides/affordable-housing,organic_sessions,,Housing Ministry,OFFICIAL_SOURCE_REQUIRED,
הגרלות דירות,he,projects_developers,subsidized,buyer,IL,navigational,decision,P1,data_page,/lottery/apartments,organic_sessions,active lottery list,Housing Ministry,OFFICIAL_SOURCE_REQUIRED,
דירות יוקרה תל אביב,he,buyer_seller_core,luxury,investor,IL,commercial,decision,P2,city_hub,/buy/tel-aviv/luxury,leads,luxury sub-hub,real supply,NEEDS_VERIFICATION,
luxury apartments tel aviv,en,intl_investor,luxury,investor,INTL,commercial,decision,P1,city_hub,/en/buy/tel-aviv/luxury,leads,,real supply,NEEDS_VERIFICATION,
penthouse tel aviv for sale,en,intl_investor,luxury,investor,INTL,commercial,decision,P1,city_hub,/en/buy/tel-aviv/penthouse,leads,,real supply,NEEDS_VERIFICATION,
beachfront apartments israel,en,intl_investor,luxury,investor,INTL,commercial,decision,P2,hub,/en/buy/beachfront,leads,coastal hub,real supply,NEEDS_VERIFICATION,
how to get an israeli mortgage,en,intl_investor,intl_finance,investor,INTL,informational,consideration,P1,guide,/en/mortgage/process,organic_sessions,,advisor,LEGAL_REVIEW,
israeli property tax for foreigners,en,intl_investor,intl_tax,investor,INTL,informational,consideration,P1,guide,/en/tax/foreign-property-tax,organic_sessions,,attorney + CPA,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
inheritance tax israel real estate,en,intl_investor,intl_tax,investor,INTL,informational,consideration,P2,guide,/en/tax/inheritance,organic_sessions,,attorney + CPA,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
power of attorney israel real estate,en,intl_investor,intl_process,investor,INTL,informational,consideration,P2,guide,/en/process/power-of-attorney,organic_sessions,,attorney,LEGAL_REVIEW,
בורסת נדל"ן,he,buyer_seller_core,category,investor,IL,informational,awareness,P3,guide,/guides/real-estate-market,organic_sessions,,editorial,NEEDS_VERIFICATION,
קרן ריט,he,buyer_seller_core,investing,investor,IL,informational,awareness,P2,guide,/guides/reit,organic_sessions,,licensed advisor,LEGAL_REVIEW,
קבוצת רכישה,he,projects_developers,group_purchase,buyer,IL,informational,consideration,P1,guide,/guides/purchase-group,organic_sessions,,attorney,LEGAL_REVIEW,
מיסוי קבוצת רכישה,he,projects_developers,group_purchase,buyer,IL,informational,consideration,P2,guide,/guides/purchase-group-tax,organic_sessions,,CPA + attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
איך לחסוך במס שבח,he,tools_calculators,tax,seller,IL,informational,decision,P1,guide,/guides/capital-gains-savings,organic_sessions,,CPA + attorney,LEGAL_REVIEW,
פטור ממס שבח דירה יחידה,he,tools_calculators,tax,seller,IL,informational,decision,P1,guide,/guides/single-home-exemption,organic_sessions,,CPA + attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
שיפוץ מטבח מחיר,he,tools_calculators,renovation,buyer,IL,commercial,consideration,P2,guide,/guides/kitchen-renovation-cost,organic_sessions,,contractor survey,NEEDS_VERIFICATION,
שיפוץ אמבטיה מחיר,he,tools_calculators,renovation,buyer,IL,commercial,consideration,P2,guide,/guides/bathroom-renovation-cost,organic_sessions,,contractor survey,NEEDS_VERIFICATION,
מחיר ריצוף למטר,he,tools_calculators,renovation,buyer,IL,commercial,consideration,P3,guide,/guides/flooring-cost-per-sqm,organic_sessions,,contractor survey,NEEDS_VERIFICATION,
זמן שיפוץ דירה,he,tools_calculators,renovation,buyer,IL,informational,consideration,P3,guide,/guides/renovation-timeline,organic_sessions,,contractor survey,NEEDS_VERIFICATION,
היתר בניה תוספת,he,urban_renewal,permits,owner,IL,informational,consideration,P2,guide,/guides/extension-permit,organic_sessions,,municipal + attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
חריגות בניה,he,urban_renewal,permits,owner,IL,informational,consideration,P2,guide,/guides/building-violations,organic_sessions,,attorney,LEGAL_REVIEW,
טופס 4,he,urban_renewal,permits,buyer,IL,informational,decision,P1,guide,/guides/form-4,organic_sessions,occupancy permit,attorney + municipal,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
רישום בית משותף,he,urban_renewal,permits,owner,IL,informational,consideration,P2,guide,/guides/condominium-registration,organic_sessions,,attorney + Land Registry,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
פרצלציה,he,urban_renewal,planning,owner,IL,informational,consideration,P3,guide,/guides/parcellation,organic_sessions,,attorney,LEGAL_REVIEW,
היטל השבחה,he,urban_renewal,planning,owner,IL,informational,consideration,P1,guide,/guides/betterment-levy,organic_sessions,,attorney + appraiser,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
דמי הסכמה,he,urban_renewal,planning,owner,IL,informational,consideration,P2,guide,/guides/consent-fee,organic_sessions,ILA,attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
חכירה מהוונת,he,urban_renewal,planning,owner,IL,informational,consideration,P2,guide,/guides/capitalized-lease,organic_sessions,ILA,attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
מנהל מקרקעי ישראל,he,urban_renewal,planning,owner,IL,navigational,awareness,P2,guide,/guides/ila,organic_sessions,,ILA,OFFICIAL_SOURCE_REQUIRED,
how does tama 38 work,en,intl_investor,intl_renewal,investor,INTL,informational,awareness,P2,guide,/en/urban-renewal/tama-38-how-it-works,organic_sessions,,attorney,LEGAL_REVIEW,
property management israel,en,intl_investor,intl_services,investor,INTL,commercial,decision,P2,directory,/en/professionals/property-management,leads,,vetting,REQUIRES_OFFICIAL_ASSET,
short term rental israel laws,en,intl_investor,intl_legal,investor,INTL,informational,consideration,P2,guide,/en/legal/short-term-rentals,organic_sessions,,attorney,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
airbnb tel aviv regulations,en,intl_investor,intl_legal,investor,INTL,informational,consideration,P2,guide,/en/legal/airbnb-tel-aviv,organic_sessions,,attorney + municipal,LEGAL_REVIEW|OFFICIAL_SOURCE_REQUIRED,
real estate agents tel aviv english speaking,en,intl_investor,intl_professionals,investor,INTL,local,decision,P1,directory,/en/professionals/realtors/tel-aviv,leads,,license verification,REQUIRES_OFFICIAL_ASSET,
nefesh b'nefesh real estate,en,intl_investor,intl_aliyah,investor,US,navigational,awareness,P3,guide,/en/aliyah/partners,organic_sessions,,partnership outreach,NEEDS_VERIFICATION,
how to get a mashkanta,en,intl_investor,intl_finance,investor,INTL,informational,consideration,P2,guide,/en/mortgage/mashkanta-explained,organic_sessions,,advisor,LEGAL_REVIEW,
arnona tel aviv,en,intl_investor,intl_ownership,investor,INTL,informational,consideration,P2,guide,/en/ownership/arnona-tel-aviv,organic_sessions,,municipal,OFFICIAL_SOURCE_REQUIRED,
cost of living tel aviv,en,intl_investor,intl_overview,investor,INTL,informational,awareness,P2,guide,/en/lifestyle/cost-of-living-tel-aviv,organic_sessions,,CBS + survey,OFFICIAL_SOURCE_REQUIRED,
best neighborhoods tel aviv,en,intl_investor,intl_neighborhoods,investor,INTL,informational,consideration,P1,guide,/en/neighborhoods/tel-aviv,organic_sessions,Anglo-relevant,editorial + data,NEEDS_VERIFICATION,
best neighborhoods jerusalem,en,intl_investor,intl_neighborhoods,investor,INTL,informational,consideration,P2,guide,/en/neighborhoods/jerusalem,organic_sessions,,editorial,NEEDS_VERIFICATION,

(Total rows: ~190.)



D. Division Instructions — How To Split Master Into Tabs + Color/Flag Rows

Split rule: never duplicate rows. Each cluster tab (02_… through 10_…) is a filtered view of 01_Master by the cluster column — implemented as a real Excel filter, a FILTER() formula in modern Excel, or a power-query pull. If a row's cluster changes, edit 01_Master; views refresh.

Row-level conditional formatting (apply on 01_Master, inherited by tabs):







Condition



Fill color



Meaning





priority = P0



Red #FCA5A5



Highest leverage; ship first after trust gate





priority = P1



Amber #FCD34D



Next wave





priority = P2



Green #A7F3D0



Scale layer





priority = P3



Gray #E5E7EB



Long-tail / template expansion





verification_flag contains LEGAL_REVIEW



Left border red #B91C1C



Blocked until counsel signs off





verification_flag contains REQUIRES_OFFICIAL_ASSET



Left border purple #7C3AED



Blocked until developer/marketer/registry asset received





verification_flag contains OFFICIAL_SOURCE_REQUIRED



Left border blue #1D4ED8



Blocked until CBS/Tax/BoI/municipal source linked





recommended_page_type = tool



Cell background language col cyan #CFFAFE



Calculator — needs methodology + disclaimer





cluster = local_programmatic AND priority ≤ P2



Strikethrough until trust gate passes



Programmatic launch requires real supply

Status column to add downstream (in Report 7+): status ∈ {backlog, drafting, review, legal, ready, published, holding}. Don't add yet; keep 01_Master clean.

Owner column to add in 14_Editorial_Calendar: owner_editorial, owner_legal, owner_data, owner_dev.

Refresh cadence: Semrush HE tab refreshed monthly; EN tab quarterly. Master keyword list reviewed every release of Report 7 (hub map).



E. Top 25 Immediate SEO Content Opportunities (after Stage 1 trust cleanup passes)

Ranked by leverage (intent strength × feasibility × trust-readiness × commercial value). All require their listed flags resolved before publish.





מחשבון משכנתא — flagship calculator, repeat-traffic + AEO. (LEGAL_REVIEW)



מחשבון מס רכישה — high transactional + first/second-home brackets. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



מחשבון מס שבח — seller-side counterpart. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



תהליך קניית דירה — pillar guide, internal-link spine. (LEGAL_REVIEW)



תמא 38 — pillar; routes to TAMA 38/1, 38/2, rights, tax. (LEGAL_REVIEW)



פינוי בינוי — pillar; routes to rights, refusing-tenant, tax. (LEGAL_REVIEW)



התחדשות עירונית — hub above TAMA + Pinui-Binui pillars. (LEGAL_REVIEW)



כמה שווה הדירה שלי — existing estimator URL, fix per Report 1 then promote.



איך לבדוק קבלן — high-trust due-diligence; Registrar of Contractors integration. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



הונאות נדל"ן — definitive Hebrew scams guide; AEO + brand-trust. (LEGAL_REVIEW)



מס רכישה דירה ראשונה — companion to calculator. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



מס רכישה דירה שניה — investor-intent traffic. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



זיכרון דברים דירה — transactional moment; download template. (LEGAL_REVIEW)



חוזה שכירות לדוגמא — high-volume template download → email capture. (LEGAL_REVIEW)



מחירי דירות 2026 — annual market report; PR + backlink magnet. (OFFICIAL_SOURCE_REQUIRED)



שוק הנדלן בישראל — evergreen overview pairing with #15. (OFFICIAL_SOURCE_REQUIRED)



buying property in israel — EN intl pillar; opens international funnel. (LEGAL_REVIEW)



foreign buyer purchase tax israel — highest commercial intent EN. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



mortgage in israel for foreigners — EN finance pillar. (LEGAL_REVIEW)



tel aviv apartments for sale (EN) — intl city hub; needs real supply.



purchase tax calculator israel (EN) — EN calculator; high commercial intent. (LEGAL_REVIEW + OFFICIAL_SOURCE_REQUIRED)



פרויקטים חדשים שדה דב — existing flagship area; only after Sde Dov asset gate. (REQUIRES_OFFICIAL_ASSET + OFFICIAL_SOURCE_REQUIRED)



מחשבון תשואה דירה — investor calculator, repeat traffic.



יד2 או מדלן — high-intent comparison; brand-defining if editorial integrity holds.



הגרלות דירות (Mehir LaMishtaken lottery list) — recurring high-intent traffic. (OFFICIAL_SOURCE_REQUIRED)



F. Keywords That Must NOT Be Targeted Yet

Blocked on Stage 1 trust cleanup (Report 1):





All cluster=local_programmatic rows (P2/P3 templates) — programmatic scaling on top of a leaky site multiplies failure.



All P1 city דירות למכירה {city} / דירות להשכרה {city} rows — Yad2-class queries with no real supply guarantee a bounce/quality-signal loss.



פרויקט דמרי שדה דב, פרויקט רינבו תל אביב — must pass the showroom state-machine + REQUIRES_OFFICIAL_ASSET gate before any promotion or schema work.

Blocked on LEGAL_REVIEW (must not publish without counsel sign-off):





All tax queries: מס רכישה …, מס שבח …, מחשבון מס רכישה, מחשבון מס שבח, איך לחסוך במס שבח, פטור ממס שבח דירה יחידה, and EN equivalents (foreign buyer purchase tax …, inheritance tax israel real estate).



All mortgage explainers and calculators: מחשבון משכנתא, מחשבון יכולת החזר, מחשבון עמלת פירעון מוקדם, מסלולי משכנתא, israeli mortgage calculator english, how to get a mashkanta.



All urban-renewal pillars and sub-guides: תמא 38 …, פינוי בינוי …, דייר סרבן, היטל השבחה, דמי הסכמה, חכירה מהוונת, טופס 4, רישום בית משותף.



All buyer-rights / contract content: זכויות קונה דירה מקבלן, זיכרון דברים דירה, ביטול עסקת דירה, חוזה שכירות לדוגמא, דירה עם עיקול.



All EN intl legal/tax/finance pages (/en/tax/*, /en/mortgage/*, /en/legal/*, /en/process/power-of-attorney).



Comparative / "recommended" professional directories (מתווכים מומלצים, יועץ משכנתאות מומלץ, דירוג חברות בניה) — methodology + defamation risk.

Blocked on REQUIRES_OFFICIAL_ASSET (developer/registry data):





All cluster=projects_developers project- and developer-specific pages.



All professionals_directory rows without verified license/bar/registry data — including city templates.



showroom_3d rows depending on real tour or render assets (no concept-as-official fallback).

Blocked on OFFICIAL_SOURCE_REQUIRED (CBS / Tax Authority / Bank of Israel / Land Registry / Housing Ministry / ILA / municipal):





All market-data pages (מחירי דירות 2026, מדד מחירי דירות, שוק הנדלן בישראל, city price/yield/rent-price reports, EN market reports).



הגרלות דירות, מחיר למשתכן, דיור בהישג יד.



ריבית משכנתא היום — daily data dependency.



נסח טאבו אונליין, פנקס קבלנים, מנהל מקרקעי ישראל reference pages.

Brand-risk / out of scope for v1:





Lead-gen pages for קבוצת רכישה until partnership + legal model exists (LEGAL_REVIEW).



nefesh b'nefesh real estate — do not target until partnership / disclosure is real.



Any "best X in Israel" superlative without published methodology — exposes us to the same trust collapse we're trying to solve.