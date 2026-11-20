# Rentals world: levels (free first, then paid) and what breaks at scale (HAD-795)

Written 20.11.2026 after Ben's voice note of that morning: "I want people to use it. Usage first and then upgrade to premium, levels" and "it can become a much more serious product, maintenance of buildings, companies with thousands of assets; be ready for that. Right now I do not want to change it."
This is a PROPOSAL for the coordinator and Ben. Nothing here is built, no price is set, and version 2 stays closed to the public until the coordinator's word.

## 0. What already exists in the code (found 20.11.2026, inc/rentals/billing.php, written 3.10.2026 under HAD-383)
Three plans are already built and switched off: free (3 apartments, 200 MB of documents), pro (50 apartments) and business (2,000 apartments). The landlord would pay through the site's own shop (WooCommerce with Morning: card, Bit, Google Pay, Apple Pay, with a tax invoice); the rent itself never passes through the site. Above the free limit nothing is deleted, the landlord only cannot add. The switch `nlrm_billing` is 'off' (no offer, no limit), the shop products are drafts, and the prices were never approved. So the levels below are a proposal on how to USE what exists, not a new build.

## 1. Three levels (the three plans that exist: free, pro, business)

| | Private landlord | Manager of dozens | Company with thousands |
|---|---|---|---|
| Who | one to a few apartments, his own | a manager or a family office, 10 to 200 apartments, often for several owners | a company, whole buildings, many employees |
| Pays | nothing | a monthly fee | by agreement |
| Gets | everything one person needs to run a rented home: the map of his properties, the building and the apartment in 3D, the day screen, the tenancy line, repairs with photos, documents, the index calculation, the example portfolio | the same, plus what only a manager needs: several owners under one account, a report per owner, team members with roles, import from a spreadsheet, a queue of repairs across all buildings, export for the accountant | the same, plus: an organisation with permissions per building and per portfolio, bulk import and sync, portfolio views (city, building, manager), service-time targets for repairs, a full log of who did what, an interface for their systems |
| Why this line | a private landlord must never hit a wall: Dira360 in Israel is free with no limit on properties, Stessa and Avail are free abroad. The code's free limit today is 3 apartments; the proposal is to raise it (10) or drop it, Ben decides | what is paid is the work of managing OTHER people's assets and a team, never the basics | sold in a conversation, not by a button |

What stays free at every level: the example portfolio, the 3D views, the first apartment and everything in it. The 3D is the entrance, so it is never behind a payment.

## 2. Where the money comes from (in the order it can start)
1. The paid manager level (above).
2. Paid one-time services inside the free level, each stated with its price before the press: for example a signed lease file, a 3D scan of the apartment by a photographer, a printed evidence file. (Reference: LeaseLink in Israel charges 79 shekels one-time for a protected contract.)
3. Professionals: a repair opened in the product can be sent to a professional from the site's own directory; the professional pays for the place in the directory, the landlord pays nothing. The site never presents itself as a broker and takes no part in the deal.
4. The developers' 3D product that already exists on the site: an apartment bought in a project page continues into the rentals world ("ten years after"), which gives developers a reason to pay for the project page.

## 3. Reference prices seen on the vendors' own pages (docs/rentals/bom/compare/products.csv, read 20.11.2026)
- Israel: MyHome free for 2 properties, then 23 and 45 shekels a month, companies from 280; LeaseLink 149 shekels a month for independent management; Dira360 free, a paid level announced without a price.
- Abroad, small landlords: Landlord Studio free for 3 units then about 15 pounds a month; Rentila free for 1 unit then 5.90 and 11.90 euros; RentRedi 12 to 30 dollars a month; Stessa free then 12 and 28 dollars.
- Abroad, managers: DoorLoop 2.50 to 5 dollars per unit per month; AppFolio from 1.49 dollars per unit with a 50-unit minimum; Buildium from 65 dollars a month.
The price itself is Ben's decision.

## 4. What breaks at 5,000 properties and many users per company (read in the code, no build)
The product was built for one person. Every row belongs to one WordPress user (`owner_id`, inc/rentals/store.php), and a team member simply acts as that owner with one role for everything (table `members`), so there is no organisation, no permission per building and no way to hold several owners' assets apart inside one account. On opening, the app loads ALL of the owner's rows into the browser, each table cut at 5,000 rows with no paging (`LIMIT 5000`, store.php): with one rent line a month per lease the money table passes that line at about 400 leases in their first year, and from there the books on screen are silently incomplete; this is the first thing to break, long before 5,000 properties. The monthly rent lines are created when the app opens, the plan and the appliances of an apartment live inside one text field of the apartment (so "every water heater older than ten years in the portfolio" cannot be asked), the import that exists is rows pasted from a spreadsheet and created one by one (fine for twenty apartments, not for a company's file that must be matched and updated), the map draws one marker per property with no grouping, the largest plan in the code stops at 2,000 apartments, and the journal records who acted in a short text with no view across people. None of this blocks the free level for private landlords; all of it must change before the first company: an organisation above the owner, permissions per building, lists that load by page and by search, parts of a home as rows of their own, a file import that matches and updates, and a real log. Ben asked not to change the model now, so this stays a list.

## 5. Before the door opens to the public (the coordinator's switch)
- The opening board approved by Ben (the example portfolio in 3D first).
- The seven legal sentences answered by a lawyer, or left out.
- The notice on what is kept about tenants, in plain words (a landlord enters other people's details).
- A decision on the free level's limit (3 apartments in the code today, the proposal is 10 or none), on the prices of the two paid plans (drafts in the shop), and on who answers a landlord who writes for help.
