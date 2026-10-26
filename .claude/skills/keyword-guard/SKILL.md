---
name: keyword-guard
description: MANDATORY before writing or changing any title, H1, meta title, slug or internal link text on nad-lan.co.il (owner order 26.10.2026). Protected high-volume keywords each have one owner page; no other page may lead with them. Run the guard, check Search Console and the live Google results first, and never trade a page that gets clicks for a guess.
---

# Keyword guard (Ben, 26.10.2026)

Ben's words: valuable, high-volume, competitive keywords like "דירות למכירה" are protected. Writing "דירות למכירה בשדה דב" at the head of another page's title, without thinking, can damage the page that should own "דירות למכירה", and you find out too late. Think like a careful SEO lead: data first, one owner per term, small steps, never harm a page that gets clicks.

## The list
`docs/seo/protected-keywords.md` (+ `.json`): 64 terms, tiers by monthly searches in Israel, owner page, our Search Console position. Rebuild it when a page changes owner or quarterly (DataForSEO keyword_overview + gsc_api.py).

## The rules
1. **One owner per protected term.** The owner is the only page that may lead its title, H1 or slug with the term, and the only target of an internal link whose text is the bare term.
2. **Other pages lead with their own topic.** A child page uses the term only qualified and after its topic: "שדה דב: דירות למכירה, מחירים ופרויקטים", not "דירות למכירה בשדה דב | ...". This is also the shape the strongest portals use (Madlan: "דירות ופרויקטים חדשים למכירה בשדה דב צפון").
3. **Hierarchy carries the long tail.** Child pages link up to the owner (breadcrumb + one contextual link "כל הדירות למכירה"), the owner links down to its children with qualified anchors.
4. **Data before any change:** monthly searches (DataForSEO), where we stand (Search Console, the URL and position per query), and the live Google top results (who ranks and the shape of their titles). Pick the target by volume and winnability, not by the words that sound right ("דירות למכירה בשדה דב" = 40 searches a month; "שדה דב" = 4,400).
5. **A page with clicks is protected too.** Do not change its title or H1 without a before snapshot, a reason from the data, and a check two to four weeks later in Search Console.
6. **Real cannibalization = two of our URLs getting impressions for the same query.** Fix it by re-targeting content and internal links. Never a redirect, never noindex (owner laws).
7. **No owner page yet** (for example "דירות להשכרה", 27,100 a month): do not let another page claim it by accident; propose an owner to Ben.

## The check (run it, paste the result in the plan)
```
python tools/seo/kw_guard.py --page /sde-dov/prices/ --kind title --text "שדה דב: דירות למכירה, מחירים ופרויקטים" --gsc <query,page CSV>
```
BLOCK stops the change. WARN needs the Search Console lines to show no second URL competing.

Related: URL word law (`tools/gsc/url_word_audit.py`), the no-redirect law, the page research law in CLAUDE.md.
