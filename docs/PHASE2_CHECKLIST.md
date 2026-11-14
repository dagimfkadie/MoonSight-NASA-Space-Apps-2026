# Phase 2 — Architecture and project structure

## Implemented architecture

| Layer | Implementation | Status |
|---|---|---|
| Presentation | Streamlit multi-tab app | Implemented; launch pending |
| Catalog | Six NASA LOLA study-region labels | Implemented; no invented coordinates |
| Data access | Product URL registry, bounded downloader, cache and raster metadata inspection | Implemented; real file validation pending |
| Terrain | Bounded sample statistics, heatmap and 3D elevation surface | Implemented; real NASA raster display pending |
| Astronomy | JPL Horizons observer API client | Implemented; live request pending |
| Comparison | Same-product, two-region descriptive comparison and CSV export | Implemented; end-to-end test pending |
| Testing | pytest tests and GitHub Actions workflow | Implemented; full suite/CI status pending |
| Documentation | Architecture, methodology and phase checklists | Implemented |

## Project structure

```text
app.py
src/moonsight/
  astronomy/horizons.py
  catalog.py
  data/
    downloader.py
    lola.py
    summary.py
  terrain/preview.py
tests/
docs/
.github/workflows/ci.yml
```

## Important design decisions

- Keep UI code separate from data and scientific modules.
- Treat LOLA study-region IDs as archive identifiers, not as latitude/longitude coordinates.
- Preserve NASA-provided slope and uncertainty products instead of substituting unsupported estimates.
- Keep raster sampling bounded for interactive performance and label it as sampling.
- Request apparent azimuth/elevation from JPL Horizons rather than relying on a simplified orbit approximation.
- Require explicit user-entered lunar observer coordinates for Horizons; do not assign arbitrary coordinates to a named LOLA region.
- Separate geometric visibility from terrain obstruction and radio communication feasibility.
- Avoid a composite site score or landing-safety recommendation.

## Phase 2 status

The package structure and modular design are implemented. Phase 2 is **not runtime-verified** until a clean environment can install the project, run pytest and Ruff, and launch Streamlit successfully.
