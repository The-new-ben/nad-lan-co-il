# NadLan CMS content model

## Existing source of truth

The source of truth remains WordPress plus `nadlan-config`:

- `nadlan_project`
- `nadlan_property`
- `nadlan_professional`
- `nadlan_lead`
- calculators and guides
- billing and monetization modules
- lead handling and analytics

The platform package adds presentation and orchestration only.

## Project language architecture

Each language is a separate published `nadlan_project` URL:

- Hebrew: `ashira-sde-dov`
- English: `ashira-sde-dov-en`
- French: `ashira-sde-dov-fr`
- Russian: `ashira-sde-dov-ru`
- Arabic: `ashira-sde-dov-ar`

The language switch must navigate to the sibling post. It must not do a client-only text swap for SEO pages.

## Minimum content per project language

Each language page should include:

- H1 with project and area
- buyer intro
- building selector section
- apartments section
- price and comps section with range only
- surroundings section
- media and interior section
- styled SEO article, 1,200 words or more for production
- FAQ
- disclaimer
- inquiry with selected apartment context

## Required project meta fields

- `project_subtitle`
- `project_area`
- `project_floors`
- `project_model_glb`
- `project_model_poster`
- `project_3d_units`
- `project_3d_facade_images`
- `project_3d_tour_url`
- `project_interior_panoramas`
- `project_3d_avg_price_per_sqm`
- `lat`
- `lng`
- `project_featured`
- `project_tier`

## Interior fields

`project_interior_panoramas` should be JSON with room records:

```json
[
  {
    "id": "living",
    "title": "Living room",
    "image": "https://assets.example.com/projects/ashira/interior/living.jpg",
    "next": ["kitchen", "balcony"]
  }
]
```

When official content is missing, the public page should state that interior material will be added after approved materials arrive. Do not show fake interiors.
