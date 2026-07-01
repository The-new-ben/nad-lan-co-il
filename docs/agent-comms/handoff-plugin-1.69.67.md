# PLUGIN HANDOFF: uPress CSS Bypass (v1.69.67)

## What Was Done
Because uPress blocks Git synchronization for the active child theme (`themes/nadlan-platform-child`), layout fixes applied there were not reaching the live server. To bypass this host limitation, the emergency CSS fixes were extracted from the theme and injected directly into the core plugin architecture.

The plugin `nadlan-config` was bumped to version **1.69.67** and packaged into a deployment ZIP.

### Specific Layout Fixes Injected:
1. **Homepage Thumbnails:** Enforced a strict 4/3 aspect ratio and `object-fit: cover` on `.nlpc-home .nlux-showcase img` to prevent cut-off and staggered heights.
2. **Stage Blowout:** Added `max-height: 75vh` to `.nl-stagewrap` to prevent the 3D map from vertically stretching the layout.
3. **Floating Controls:** Re-docked the WhatsApp/Accessibility controls (`.nl-fly`) to `bottom: 85px` with a forced `z-index` so they float above the footer contact forms without overlapping them.

## Where is it Located?
- **Source Code:** The injection is located inside `plugins/nadlan-config/nadlan-config.php` via the `nadlan_config_emergency_css` function.
- **Deployment Package:** The installable ZIP file is located in this repository at: `plugin-dist/nadlan-config-1.69.67.zip`.

## Installation Instructions
Do **NOT** modify or unpack the ZIP file unless you are fundamentally restructuring how WordPress imports plugins. 

To deploy:
1. Download `plugin-dist/nadlan-config-1.69.67.zip` from this repository.
2. Go to your live WordPress Admin Panel -> **Plugins** -> **Add New** -> **Upload Plugin**.
3. Upload the ZIP. When prompted, select **Replace current with uploaded**.
4. **CRITICAL:** Purge your WordPress cache (uPress Cache / WP Rocket / LiteSpeed) to force browsers to fetch the newly injected CSS.
