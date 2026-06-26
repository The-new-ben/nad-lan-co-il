# Ashira Showroom Layout Contract

Date: 2026-06-26

This diagram is the current build contract for the Ashira project page and the repeatable NadLan
project showroom factory.

```mermaid
flowchart TB
  A["Header / NadLan navigation"] --> B["Breadcrumbs: NadLan / Projects / Ashira Sde Dov"]
  B --> C["Hero media: sourced or original poster"]
  C --> D["Short buyer intro: project, Sde Dov, developer, non-binding estimate"]
  D --> E["Showroom shell"]

  subgraph E["Showroom shell"]
    E1["Legend: available / checking / unavailable"]
    E2["3D context model"]
    E3["Fixed facade apartment picker"]
    E4["Selected apartment card"]
    E5["Buyer contact form"]
    E1 --> E2
    E1 --> E3
    E2 --> E2a["Purpose: orientation, sea, sun, nearby buildings"]
    E2 --> E2b["Not used for exact apartment picking unless GLB has unit meshes"]
    E3 --> E3a["Apartment cells embedded on facade"]
    E3a --> E4
    E4 --> E4a["Plan"]
    E4 --> E4b["Interior tour"]
    E4 --> E4c["View from apartment"]
    E4 --> E5
  end

  E --> F["Project material modules"]
  F --> F1["Developer video slot"]
  F --> F2["Gallery / renders slot"]
  F --> F3["Matterport / Homes.com-style interior slot"]
  F --> F4["Plans and brochures"]

  F --> G["Neighborhood and investor content"]
  G --> G1["Sde Dov context"]
  G --> G2["Sea / Reading / Namal / parks / transit"]
  G --> G3["Price estimate table with source notes"]
  G --> G4["Foreign-buyer language cluster"]

  G --> H["Professionals and buyer support"]
  H --> I["FAQ / schema-aligned answers"]
  I --> J["Footer"]

  subgraph CMS["CMS / contractor-editable data"]
    C1["Project facts"]
    C2["GLB URL and poster URL"]
    C3["Facade image URL"]
    C4["Unit inventory JSON"]
    C5["Drawings JSON"]
    C6["Environment JSON"]
    C7["Video / gallery / tour URLs"]
  end

  CMS --> C
  CMS --> E2
  CMS --> E3
  CMS --> F
  CMS --> G
```

## Mobile Order

```mermaid
flowchart TB
  M1["Header"] --> M2["Hero media"]
  M2 --> M3["Short intro"]
  M3 --> M4["3D context model"]
  M4 --> M5["Facade picker"]
  M5 --> M6["Selected apartment card"]
  M6 --> M7["Contact action"]
  M7 --> M8["Material cards"]
  M8 --> M9["Neighborhood content"]
  M9 --> M10["Language links and footer"]
```

## Realism Rule

The context model must be project-relative:

- Sde Dov projects show land, sea to the west, and nearby references such as Reading / Namal.
- Ramat Aviv projects show Ramat Aviv parks, roads, schools and transit.
- No generic future city. No tower floating in water. No copied developer render without rights.
