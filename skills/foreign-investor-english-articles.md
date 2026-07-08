# Skill: Foreign Investor English Articles (Formatting & UX)

> **Notice to all agents:** nad-lan.co.il is a Hebrew, RTL (Right-To-Left) website by default. When publishing English content for the Foreign Investor hub, you **must** apply strict LTR wrappers and follow specific UX guidelines to prevent structural breakage.

## 1. The RTL / LTR Collision Rule
Never push raw English markdown directly into the WordPress post body. The WordPress theme wrapper is `dir="rtl"`, which will push all English text, bullets, and tables to the right and break readability.

**Required HTML Wrapper:**
All English article content MUST be wrapped in:
```html
<div class="article-en-ltr" dir="ltr" lang="en">
   <!-- parsed markdown HTML goes here -->
</div>
```
*The `.article-en-ltr` class is styled in the `nadlan-config` plugin to enforce `text-align: left` and proper margins.*

## 2. No H1 Duplication
WordPress automatically outputs the post title as an `<h1>`. 
Do **NOT** include a `# Title` header inside the markdown body when publishing. If your markdown file has an H1, you must strip it via your publishing script before pushing to the REST API.

## 3. The "No Wall of Text" Rule
Foreign investors are scanning for numbers, safety, and process. Do not give them a legal contract layout.
- **Maximum 300 words** without a visual break.
- **Visual breaks include:** `<hr>`, `<blockquote>` (for callouts/quotes), or interactive CTA boxes.

## 4. Luxury Tables
Never use default browser tables. WordPress tables without classes look cheap.
When parsing markdown tables to HTML, you must inject the `nadlan-luxury-table` class:
```html
<table class="nadlan-luxury-table">
```

## 5. CTAs and Interactivity
Text links are not enough for conversion. When referencing a calculator (e.g., Purchase Tax, Mortgage), use the branded CTA class (or build a shortcode). For now, ensure links are bolded or wrapped in a button-like class if available.

## Open TODOs for next agent
- [ ] Develop a WordPress shortcode `[nadlan_cta type="mortgage"]` to render a polished CTA box inside English articles.
- [ ] Implement an automatic markdown linting step in the Github Actions CI that checks for `.article-en-ltr` wrappers on all `language: en` frontmatter files.

---
*Created 2026-07-01 to fix the catastrophic RTL layout breakage on the foreign investor hub.*
