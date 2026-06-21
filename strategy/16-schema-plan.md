# Schema Plan

Schema goals:
- Help search engines understand pages without fabricating facts.
- Keep schema aligned with visible content.

Candidate schema:
- Organization.
- WebSite.
- BreadcrumbList.
- Article.
- FAQPage.
- ItemList.
- RealEstateListing where appropriate.
- Product/Offer only when commercial facts are real and visible.
- LocalBusiness/ProfessionalService where legally and factually appropriate. `LEGAL_REVIEW`

Rules:
- No fake prices.
- No fake availability.
- No fake reviews.
- No official-project claims without source.
- No duplicate/conflicting schema from multiple systems.

Required audit:
- Existing schema by page type. `NEEDS_VERIFICATION`
- Yoast overlap/conflict check. `NEEDS_VERIFICATION`

