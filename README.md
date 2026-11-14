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

## Planned technology

Python, Streamlit, NumPy, Pandas, Rasterio, Plotly, and Requests. Dependencies will be finalized when the data and calculation workflows are implemented.

## Planned project layout

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
assets/
```

The structure may be adjusted when implementation needs are established.

## Data sources under evaluation

- NASA LOLA product page: https://pgda.gsfc.nasa.gov/products/78
- NASA LOLA data archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA/JPL Horizons documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- NASA lunar polar illumination and Earth visibility resources: https://pgda.gsfc.nasa.gov/products/69
- NASA Lunar Surface Data Book: https://ntrs.nasa.gov/citations/20250002845

A source is not considered integrated merely because it is listed here. Product identifiers, coordinate conventions, resolution, units, access conditions, and challenge eligibility must be verified and documented before use.

## Development

Implementation and testing instructions will be added alongside the application code. Do not install dependencies or expect an application to run until those files are committed.

## Competition compliance

- Cite every source used, including datasets, software, and third-party materials.
- Document licenses for original and third-party materials.
- Record AI assistance accurately in `AI_DISCLOSURE.md`.
- Credit contributors truthfully.
- Do not include private personal information or credentials.
- Do not claim NASA endorsement or affiliation.
- Do not claim a calculation or feature is validated without evidence.

See [docs/PHASE1_CHECKLIST.md](docs/PHASE1_CHECKLIST.md) for the foundation checklist.

## License

A `LICENSE` file is present in this repository, but the team must review and agree on the license before treating it as the final project licensing decision. Third-party data and software may have separate terms; see the official NASA Space Apps participant terms and the project references before submission.
