# Phase 3 — NASA LOLA data retrieval

## Implemented in the repository

| Item | Status | Evidence |
|---|---|---|
| NASA LOLA product URL registry | Implemented; URL naming verified against NASA archive listing | `src/moonsight/data/lola.py` |
| Bounded HTTP download | Implemented; not yet exercised against NASA from the app | `src/moonsight/data/downloader.py` |
| Temporary-file and atomic-cache workflow | Implemented; not yet tested in a clean repository environment | `src/moonsight/data/downloader.py` |
| TIFF header check | Implemented; covered by unit tests | `tests/test_downloader.py` |
| Rasterio metadata inspection | Implemented; synthetic GeoTIFF test added | `src/moonsight/data/downloader.py`, `tests/test_downloader.py` |
| Streamlit download controls | Implemented; app not yet launched | `app.py` |

## Local test note

A local scratch test harness assembled from the current committed catalog, URL-registry, downloader logic, and tests completed with **20 tests passed**. This was useful for checking the logic and synthetic GeoTIFF inspection, but it was not a clean install or test run of the GitHub checkout. The repository's own environment and app still need to be tested.

## NASA source facts

The NASA archive lists the six study regions and their elevation, spot-count, slope, total elevation uncertainty, and slope uncertainty products. It describes the GeoTIFFs as 5 m/pixel, with south-polar stereographic X/Y coordinates in metres and the MOON_ME reference frame tied to DE421.

Source: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

NASA product page: https://pgda.gsfc.nasa.gov/products/78

The current URL builder follows the filenames shown in NASA's archive. The URL pattern alone does not prove that a particular file has been downloaded or scientifically validated.

## Validation policy

- Reject non-TIFF responses, including HTML error pages.
- Enforce a configurable maximum download size (default 512 MiB).
- Download to a temporary file and move it into the cache only after validation.
- Require Rasterio to open the file.
- Require a coordinate reference system and positive raster dimensions.
- Check for approximately 5 m pixels before accepting the file.
- Record the file path, dimensions, band count, CRS, pixel size, bounds, data type, and NoData value.
- Do not interpret metadata validation as proof of terrain quality or landing suitability.

## Remaining work

- [ ] Install the package and dependencies in a clean environment.
- [ ] Run `pytest` from the GitHub checkout.
- [ ] Run `ruff check .` and fix any findings.
- [ ] Launch the Streamlit app.
- [ ] Download one real NASA product (start with Site04 elevation) and record its metadata.
- [ ] Confirm the file size, CRS, dimensions, transform, NoData value, and pixel scale against source documentation.
- [ ] Inspect a small raster window and verify values are finite and physically plausible before visualizing.
- [ ] Add a small data provenance record for the downloaded file.
- [ ] Only then expand testing to the remaining sites and product types.

## Current status

**Code committed; a local scratch test harness passed, but clean-checkout runtime and real-data validation remain pending.** No terrain measurements, site rankings, or landing-safety conclusions are currently produced by MoonSight.
