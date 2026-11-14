# MoonSight — Lunar Landing Site Navigator

**NASA Space Apps Challenge 2026**  
**Team:** #MoonSightExplorers  
**Challenge:** Lunar Landing Site Navigator

MoonSight is an educational prototype for exploring NASA lunar south-pole terrain products and apparent Sun/Earth directions. It is designed to help users compare source evidence—not to certify landing sites.

> **Safety and science boundary:** MoonSight is not a flight system. It does not determine landing safety, mission feasibility, terrain clearance, solar power availability, or operational communications capability.

## Current prototype

The Streamlit app provides four tabs:

1. **Terrain explorer:** select one of six NASA LOLA study-region product groups; download and inspect a GeoTIFF; view bounded sample statistics and a 2-D heatmap. Elevation products also have a 3-D sampled surface.
2. **Compare regions:** compare descriptive sample statistics for the same product across two regions and export the table as CSV.
3. **Sun & Earth geometry:** enter a lunar geodetic observer coordinate and request apparent azimuth/elevation for the Sun and Earth from JPL Horizons. Results can be exported as CSV.
4. **Data & limitations:** source descriptions, assumptions and scientific limitations.

The Horizons coordinates are explicitly user-entered. The app does not invent latitude/longitude for NASA's named LOLA tiles or imply that a default coordinate belongs to any particular region.

## Verification status

- Repository foundation, data modules, Streamlit UI, and tests are committed.
- Focused synthetic terrain tests and isolated raster-summary checks were previously recorded in `docs/PHASE3_CHECKLIST.md`.
- Horizons tests use synthetic API response fixtures and a fake HTTP session; they do not prove that a live Horizons request succeeds.
- The full repository test suite, Ruff, Streamlit launch, live NASA GeoTIFF retrieval, and live JPL Horizons requests still require verification in a clean environment.
- No real NASA raster has yet been validated in this development session.
- No terrain-aware horizon obstruction, site ranking, or landing-safety score is implemented.

## NASA Space Apps timing

The official 2026 event is November 14–15, 2026. The official site states that project submission opens November 14 at 9:00 AM and closes November 15 at 11:59 PM local time. Follow the event-specific Project Submission page and local-event instructions for final requirements.

Official event: https://www.spaceappschallenge.org/2026/

## Technology

Python 3.10+, Streamlit, NumPy, Pandas, Rasterio, Plotly, Requests, pytest and Ruff.

## Project layout

```text
app.py
src/moonsight/
  astronomy/horizons.py
  data/
  terrain/preview.py
tests/
docs/
.github/workflows/ci.yml
```

## Setup and run

1. Clone the repository and open a terminal in its directory.
2. Create and activate a virtual environment.

   **Windows PowerShell**
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the package and development dependencies.

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   ```

4. Launch the application.

   ```bash
   streamlit run app.py
   ```

5. Run quality checks.

   ```bash
   pytest
   ruff check .
   ```

These commands are setup instructions, not claims that the complete suite or app has already passed in a clean checkout. Rasterio installation may vary by operating system and Python environment.

## Data sources

- NASA LOLA product page: https://pgda.gsfc.nasa.gov/products/78
- NASA LOLA South Pole archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA/JPL Horizons API: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- NASA lunar polar illumination and Earth visibility resources: https://pgda.gsfc.nasa.gov/products/69
- NASA Lunar Surface Data Book: https://ntrs.nasa.gov/citations/20250002845

NASA describes the listed LOLA GeoTIFFs as 5 m/pixel south-polar stereographic X/Y grids in metres, MOON_ME reference frame, ephemeris DE421. MoonSight checks basic file properties but still needs a real file metadata comparison against the complete NASA reference definition.

## Development checklists

- [Phase 1 — Compliance and repository](docs/PHASE1_CHECKLIST.md)
- [Phase 2 — Architecture](docs/PHASE2_CHECKLIST.md)
- [Phase 3 — NASA data](docs/PHASE3_CHECKLIST.md)
- [Phase 4 — Scientific engine](docs/PHASE4_CHECKLIST.md)
- [Phase 5 — Interactive interface](docs/PHASE5_CHECKLIST.md)
- [User guide](docs/USER_GUIDE.md)
- [Data provenance and source register](docs/DATA_PROVENANCE.md)
- [Scientific validation plan](docs/SCIENTIFIC_VALIDATION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Scientific methodology](docs/SCIENTIFIC_METHODOLOGY.md)
- [AI assistance disclosure](AI_DISCLOSURE.md)

## Competition compliance and attribution

- Cite NASA datasets and all third-party materials used.
- Record AI assistance accurately in `AI_DISCLOSURE.md`.
- Credit contributors only for work they actually performed.
- Do not publish personal contact details, credentials, or private information.
- Do not imply NASA endorsement or affiliation.
- Review the current challenge-specific submission form, media requirements, and local-event instructions before submitting.

## License

The repository contains an MIT license for original project code. This does not automatically relicense NASA datasets, third-party packages, or external materials. Confirm that all contributors agree with the repository license before final submission.
