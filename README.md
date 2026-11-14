# MoonSight — Lunar Landing Site Navigator

**NASA Space Apps Challenge 2026**  
**Team:** #MoonSightExplorers  
**Challenge:** Lunar Landing Site Navigator

MoonSight is a student-built research prototype intended to help users explore and compare lunar south-pole study locations using documented terrain data and Sun/Earth viewing geometry.

> **Scientific and safety note:** MoonSight is an educational decision-support prototype, not a flight system. It does not certify landing safety, mission feasibility, or operational communications capability.

## Project status

Development is being carried out during the official 2026 NASA Space Apps Challenge period. This repository is a fresh implementation. It does not import source code or pre-event implementation from the team's earlier prototype.

At this stage, the repository foundation is being prepared. Features must not be described as implemented or tested until the corresponding code and validation evidence exist.

## Planned capabilities

- Compare documented lunar south-pole study locations.
- Retrieve and visualize NASA LOLA terrain products.
- Examine elevation, slope, and available uncertainty information.
- Use NASA/JPL Horizons for date-specific apparent Sun and Earth directions.
- Distinguish geometric visibility from terrain-obstructed visibility and radio-link feasibility.
- Provide interactive plots and clearly labeled data exports.
- Document data provenance, assumptions, uncertainty, and limitations.

## Technology

Python, Streamlit, NumPy, Pandas, Rasterio, Plotly, and Requests. Development tools include pytest and Ruff.

## Project layout

```text
app.py
src/moonsight/
  data/
  terrain/
  astronomy/
  visibility/
  comparison/
  visualization/
tests/
docs/
```

## Setup and run

Use Python 3.10 or newer.

1. Clone this repository and open a terminal in the project folder.
2. Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project and development tools:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   ```

4. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

5. Run the automated checks:

   ```bash
   pytest
   ruff check .
   ```

These are setup instructions, not evidence that the commands have already been run successfully. Record actual results in the project checklist. Rasterio installation may depend on the Python version and operating-system environment.

## Data sources under evaluation

- NASA LOLA product page: https://pgda.gsfc.nasa.gov/products/78
- NASA LOLA data archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA/JPL Horizons documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- NASA lunar polar illumination and Earth visibility resources: https://pgda.gsfc.nasa.gov/products/69
- NASA Lunar Surface Data Book: https://ntrs.nasa.gov/citations/20250002845

NASA's LOLA south-pole archive documents elevation, slope, and uncertainty GeoTIFF products at 5 m/pixel for its listed study regions. Before using a file, verify its actual download, metadata, coordinate reference, units, and data quality. A source is not considered integrated merely because it is listed here.

## Competition compliance

- Cite every source used, including datasets, software, and third-party materials.
- Document licenses for original and third-party materials.
- Record AI assistance accurately in `AI_DISCLOSURE.md`.
- Credit contributors truthfully.
- Do not include private personal information or credentials.
- Do not claim NASA endorsement or affiliation.
- Do not claim a calculation or feature is validated without evidence.

See [docs/PHASE1_CHECKLIST.md](docs/PHASE1_CHECKLIST.md) and [docs/PHASE2_CHECKLIST.md](docs/PHASE2_CHECKLIST.md) for development status.

## License

The team has agreed to use the MIT License for original project code; see [LICENSE](LICENSE). NASA datasets, third-party software, and other external materials may have separate terms. The MIT license on this repository does not automatically relicense those materials.
