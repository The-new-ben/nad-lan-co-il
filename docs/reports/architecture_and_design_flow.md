# Platform Architecture & Design Flow

## 1. Site Hierarchy & Ecosystem Pillars
This diagram shows the complete structure of the NadLan platform, from the homepage down to the deep e-commerce layers where users interact with 3D models and contact contractors.

```mermaid
graph TD
    %% Main Pillars
    Home[Homepage / Landing] --> Discover[Project Discovery & Map Search]
    Home --> Pros[Professionals Directory]
    Home --> Mag[Magazine / SEO Content]

    %% Project Discovery Flow
    Discover --> ProjList[Global Map & Listings]
    ProjList --> ProjPage[Project Page e.g. Ashira, Rainbow]
    
    %% Inside a Project Page (The E-Commerce Layer)
    ProjPage --> Hero[Hero / Context]
    ProjPage --> Showroom[Showroom Engine Layer]
    ProjPage --> Details[Neighborhood / Amenities]
    
    %% The Showroom Engine Depth
    Showroom --> Facade[Facade View / 2D Sketch]
    Showroom --> 3D[3D WebGL Building Model]
    
    %% Drill Down to Apartments
    Facade --> AptPicker[Apartment Selection Tool]
    3D --> AptPicker
    
    AptPicker --> FPS[First-Person Interior Walkthrough]
    AptPicker --> Floorplan[2D/3D Interactive Floorplan]
    
    %% Conversion / Monetization Layer
    FPS --> ActionRail[Mobile Action Rail]
    Floorplan --> ActionRail
    ActionRail --> WhatsApp[Instant WhatsApp Lead]
    ActionRail --> LOI[Submit Letter of Intent]
    ActionRail --> Call[Direct Call to Contractor]
```

## 2. The Design Flow (From Sketch to 3D)
This diagram illustrates how a raw 2D architectural sketch provided by a contractor is processed into the immersive "Creamy, Sketchy, Architectural" 3D experience on the platform.

```mermaid
graph LR
    subgraph Input
        Sketch[Contractor PDF/2D Sketch]
        CAD[BIM/CAD Files]
    end
    
    subgraph AI Processing Pipeline
        Sketch --> SpatialAI[Spatial AI Detection walls/doors]
        CAD --> MeshOptimizer[Decimation to <500k polygons]
        SpatialAI --> GenerativeDesign[Apply 'Creamy/Sketchy' Textures]
    end
    
    subgraph Outputs
        GenerativeDesign --> GLB[Lightweight GLB File]
        MeshOptimizer --> GLB
    end
    
    subgraph WordPress Implementation
        GLB --> WP[Upload to WP Media Library]
        WP --> MetaBox[Attach to Project MetaBox]
        MetaBox --> ModelViewer[Render in model-viewer engine.js]
    end
```

## 3. The Design Language Matrix
Every element on the site must adhere to this matrix. No exceptions.

| Element | Specification | Purpose |
| :--- | :--- | :--- |
| **Colors** | Warm Cream `#faf7f1`, Deep Charcoal `#1c1a15`, Terracotta `#c2563a` | Evoke Jerusalem stone, Mediterranean warmth, and high-fashion editorial clarity. |
| **Typography** | Sans-serif for UI (`Inter` or similar), Serif for headers. | Legibility for HNWIs; professional trust signals. |
| **Imagery** | 3D Renders blended with pencil-sketch edges. | Feels bespoke, architectural, and premium rather than mass-produced. |
| **Maps** | Custom Mapbox styles (light-v11) with 3D extrusions. | Contextualizes luxury assets within their geographic reality. |
