# Where the raw files are

The raw captures behind `prices.json` were moved out of this public repo on 22.10.2026, at 22:40. They are third-party pages, PDFs and images. The folder they were in, `raw/`, is now at:

`C:/Users/777/nad-lan/_private-research/2026-10-22-greece-prices/raw/`

The Natural Earth file that `geo/build_map.py` reads, `countries-10m.json`, was moved to the `geo/` folder next to it. That file is public domain, from world-atlas@2.0.2.

**Before you re-run either script,** copy both folders back to where the script expects them:
- `build_prices.py` reads the `raw/` folder;
- `geo/build_map.py` reads `countries-10m.json`.

The outputs the site uses stay here, and these are what the site reads: `prices.json`, `prices.md`, `paid-dkg.json`, and the map data built into the plugin.
