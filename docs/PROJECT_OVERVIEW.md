# MoonSight — Project Overview

## Project identity

- **Project:** MoonSight — Lunar Landing Site Navigator
- **Team:** #MoonSightExplorers
- **Challenge:** NASA Space Apps Challenge 2026 — Lunar Landing Site Navigator
- **Repository:** https://github.com/dagimfkadie/MoonSight-NASA-Space-Apps-2026
- **Application:** Python and Streamlit educational prototype

## The problem

Exploring candidate lunar south-pole regions requires understanding multiple kinds of evidence: surface elevation, slope, measurement coverage and uncertainty, along with the changing apparent directions of the Sun and Earth. These data are distributed across scientific archives and services, and interpreting them requires attention to units, coordinate frames, time and limitations.

A map or a single terrain statistic cannot establish whether a location is safe or suitable for a mission. A useful educational exploration tool should make source data easier to inspect while keeping the evidence and uncertainty visible.

## Our approach

MoonSight brings selected NASA Lunar Orbiter Laser Altimeter (LOLA) south-pole terrain products and JPL Horizons observer geometry into one interactive application.

The prototype currently supports:
1. Selecting one of six NASA LOLA study-region product groups.
2. Retrieving and inspecting available GeoTIFF terrain products.
3. Viewing bounded sample statistics and 2-D terrain heatmaps; elevation products can also be viewed as sampled 3-D surfaces.
4. Comparing descriptive statistics for the same product across two regions.
5. Entering a lunar geodetic observer coordinate and requesting apparent Sun/Earth azimuth and elevation from JPL Horizons.
6. Exporting supported comparison and ephemeris tables as CSV.

## Data and technical foundation

**NASA LOLA archive:** https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

The archive provides south-polar terrain products. Product families used by the application include elevation, slope, return count, elevation uncertainty and slope uncertainty. NASA's archive describes the GeoTIFF grids as 5 m/pixel south-polar stereographic data with X/Y in metres, MOON_ME reference frame and DE421 ephemeris. The implementation's current metadata checks are basic; exact lunar CRS verification remains a documented task.

**JPL Horizons API:** https://ssd-api.jpl.nasa.gov/doc/horizons.html

MoonSight requests apparent observer azimuth/elevation for the Sun and Earth from a user-entered lunar geodetic coordinate. Coordinates are not inferred from a LOLA tile identifier.

**Technology:** Python 3.10+, Streamlit, NumPy, Pandas, Rasterio, Plotly, Requests, pytest and Ruff.

## What is innovative about the prototype

MoonSight's contribution is the integration of terrain exploration, region-to-region descriptive comparison and time-dependent Sun/Earth observer geometry in a single, approachable workflow, with source provenance and limitations presented alongside the visualizations.

The prototype emphasizes transparency: it distinguishes archive products from calculated summaries, reports bounded sampling, asks users to supply observer coordinates, and avoids presenting a simplistic numerical score as a landing recommendation.

This is an integration and exploration prototype—not a claim that the underlying NASA data or JPL service is new.

## Intended users and potential value

- Students learning about lunar terrain data and planetary mapping.
- Educators demonstrating remote-sensing products and coordinate systems.
- Early-stage researchers exploring how terrain and illumination-related geometry datasets can be brought together.
- Challenge participants who need a transparent prototype for examining source evidence.

Potential value is educational and exploratory. Any use in mission planning would require substantially more engineering, validation and expert review.

## Current limitations

- The application does not calculate landing safety, site suitability, mission feasibility or an approved landing-site ranking.
- Raster statistics and visualizations use bounded nearest-neighbour samples, not full-resolution analysis.
- The downloader does not yet verify the exact complete MOON_ME / DE421 CRS definition against NASA's authoritative metadata.
- Live NASA data retrieval and live JPL Horizons calls require verification in the final deployment environment.
- Horizons azimuth/elevation does not account for local terrain obstruction.
- No illumination-duration model, surface-panel power estimate, terrain-aware communications model or radio link budget is implemented.
- Synthetic unit tests do not constitute independent scientific validation.

See [Scientific Methodology](SCIENTIFIC_METHODOLOGY.md), [Data Provenance](DATA_PROVENANCE.md), and [Scientific Validation](SCIENTIFIC_VALIDATION.md) for details.

## How to run

Follow the installation and launch instructions in the repository [README](../README.md) and the [User Guide](USER_GUIDE.md).

## Future development

Priorities for a responsible next version:
1. Verify exact source CRS and product metadata against downloaded NASA files.
2. Add saved, provenance-labelled live-data examples and reproducible validation records.
3. Add dedicated tests for terrain preview coordinates, masks and orientation.
4. Compare Horizons outputs against an independently configured JPL Horizons query.
5. Only then investigate terrain-aware horizon profiles and illumination analysis, with explicit assumptions and independent validation.

## Attribution and disclaimer

NASA and JPL data/services are credited to their respective providers. MoonSight is an independent educational prototype and is not endorsed by NASA or JPL. The project does not certify landing locations or replace expert scientific and engineering review.
