# Phase 5 — Interactive user interface

## Implemented

- [x] Streamlit interface organized into Terrain Explorer, Compare Regions, Sun & Earth Geometry, and Data & Limitations tabs.
- [x] NASA LOLA site and product selectors.
- [x] Raster metadata and bounded sample-statistics display.
- [x] 2-D Plotly product heatmap.
- [x] 3-D sampled surface for the elevation product only.
- [x] Two-region comparison using the same product and bounded sample statistics.
- [x] Comparison chart and CSV export.
- [x] User-entered lunar observer coordinates and UTC date selection.
- [x] Require explicit confirmation that observer-coordinate provenance has been checked before querying Horizons.
- [x] JPL Horizons Sun/Earth ephemeris table, elevation plot, and CSV export.
- [x] Visible explanations of assumptions and non-operational limitations.

## UI interpretation rules

- The 3-D preview is downsampled; visual perspective can mislead.
- The comparison view is descriptive, not a ranking or suitability score.
- Horizons coordinates are user-supplied and are not inferred from a LOLA tile name.
- Apparent elevation is not terrain-obstructed visibility.
- Earth geometric visibility is not communication feasibility.
- Sun elevation is not solar power or illumination duration.

## Automated verification

- [x] Streamlit AppTest startup smoke test is included in the automated suite.
- [x] Complete pytest suite passed: 46 tests.
- [x] Ruff passed.
- [x] Python source compilation passed.

**Evidence:** GitHub Actions workflow run [#125](https://github.com/dagimfkadie/MoonSight-NASA-Space-Apps-2026/actions/runs/43591255469), on merged `main` commit `b9e836cccc57888d206f9e2abe0040158f2eca52` (14 November 2026).

## Manual and live-data validation still required

- [ ] Test all four tabs in a browser.
- [ ] Test a real NASA raster download and 2-D/3-D rendering.
- [ ] Test the comparison CSV export in the browser.
- [ ] Run live Sun and Earth Horizons queries with a verified lunar observer coordinate.
- [ ] Test the Horizons CSV export in the browser.
- [ ] Check mobile layout and long-download feedback.
- [ ] Verify the downloaded raster's complete MOON_ME / DE421 CRS definition against NASA product metadata.

Passing automated checks does not complete these manual, live-data, or scientific-validation tasks.
