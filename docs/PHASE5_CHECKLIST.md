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

## Validation still required

- [x] Add a Streamlit AppTest startup smoke test to the automated suite.
- [ ] Run the complete automated test suite and Ruff.
- [ ] Test all four tabs in a browser.
- [ ] Test a real NASA raster download and 2-D/3-D rendering.
- [ ] Test the comparison CSV export.
- [ ] Run live Sun and Earth Horizons queries with a verified lunar observer coordinate.
- [ ] Test the Horizons CSV export.
- [ ] Check mobile layout and long-download feedback.
- [ ] Run the complete automated test suite and Ruff.
