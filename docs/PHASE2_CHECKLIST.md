# Phase 2 — Architecture and project structure

## Status

Phase 2 foundation files have been committed and retrieved from GitHub for verification. Runtime installation, Streamlit launch, and pytest execution have not yet been performed.

| Item | Status | Evidence |
|---|---|---|
| Python packaging configuration | Implemented, not runtime-tested | `pyproject.toml` |
| Dependency list | Implemented, not installed | `requirements.txt` |
| Streamlit application shell | Implemented, not launched | `app.py` |
| Modular package structure | Implemented, files verified | `src/moonsight/` |
| NASA LOLA study-region catalog | Implemented from NASA archive labels | `src/moonsight/catalog.py` |
| Catalog unit tests | Written, not executed | `tests/test_catalog.py` |
| Architecture documentation | Implemented | `docs/ARCHITECTURE.md` |
| Scientific methodology framework | Implemented | `docs/SCIENTIFIC_METHODOLOGY.md` |

## Important source-backed details

NASA's South Pole Landing Site LOLA DEM archive lists six study-region product groups: Site01, Site04, Site07, Site11, Site20, and Site23. It describes the associated GeoTIFF products as 5 m/pixel, with south-polar stereographic X/Y coordinates in metres and a MOON_ME reference frame tied to DE421.

Source: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

JPL Horizons documents observer ephemerides and apparent azimuth/elevation output. Lunar topocentric observer configuration must be explicitly validated before using returned values in MoonSight.

Source: https://ssd-api.jpl.nasa.gov/doc/horizons.html

## Remaining verification

- [ ] Install package in a clean Python environment using `pip install -e ".[dev]"`.
- [ ] Run `pytest`.
- [ ] Run `ruff check .`.
- [ ] Launch `streamlit run app.py`.
- [ ] Confirm the application loads and the six source-listed site names display.
- [ ] Confirm the README setup instructions match the actual environment.
- [ ] Fix any failures and record the results here.

## Exit criteria

Phase 2 is complete only after the package installs, tests pass, lint checks pass, and the Streamlit shell starts successfully. Source-backed labels are not equivalent to verified site coordinates or integrated terrain products.
