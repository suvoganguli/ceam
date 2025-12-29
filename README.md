# CEAM — Critical Energy Access Mapping

CEAM is an exploratory project to map potential energy-access gaps using open geospatial data. The near-term focus is **data discovery and sanity-check analysis** (not modeling). The long-term goal is to evolve this into a reproducible ML pipeline for energy-access screening and prioritization.

## Project status
- **Phase 0 (current):** Prelim data exploration and visualization
- **Later:** Formal ML pipeline (data → EDA → feature engineering → modeling → evaluation)

## Repository structure

- `prelim_analysis/`  
  Early notebooks + notes to inspect and validate data sources and overlays.
  - `01_get_data.md` — download/extract runbook (VIIRS NTL via curl)
  - `02_admin_boundaries.ipynb` — political/admin boundaries + AOI context maps
  - `03_worldpop.ipynb` — population raster exploration (WorldPop or similar)
  - `04_openstreetmap.ipynb` — OSM features (roads/settlements/waterways) exploration
  - `05_nighttimelight.ipynb` — VIIRS nighttime lights (NTL) exploration and AOI clipping

## Data
Large datasets (GeoTIFFs, shapefiles, extracts) are intentionally kept **outside** the repo.  
Notebooks assume you have a local data directory and set a `DATA_ROOT` (or equivalent) near the top of each notebook.

## Current data sources (Phase 0)
- VIIRS DNB monthly composites (NTL radiance + cloud-free coverage proxy)
- OpenStreetMap (vector features)
- WorldPop (population raster)
- Admin boundaries / basemaps (vector)

## How to use
1. Start in `prelim_analysis/01_get_data.md` to download the VIIRS tile/months used for exploration.
2. Run notebooks in order (`02` → `05`) to validate AOI context, population, OSM features, and NTL overlays.

## Notes
This repo is intentionally lightweight while the data discovery phase is in progress. As the pipeline matures, this README and structure will be expanded (including environment setup, reproducibility, and formal ML workflow).

