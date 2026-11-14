# Phase 3 — NASA LOLA data retrieval and sampling

## Implemented in the repository

| Item | Status | Evidence |
|---|---|---|
| NASA LOLA product URL registry | Implemented; filenames confirmed against the official archive page | `src/moonsight/data/lola.py` |
| Bounded HTTP download | Implemented; live download from this environment remains unverified | `src/moonsight/data/downloader.py` |
| Temporary-file and atomic-cache workflow | Implemented; not yet tested in a clean repository environment | `src/moonsight/data/downloader.py` |
| TIFF header check | Implemented; unit tests written | `tests/test_downloader.py` |
| Rasterio metadata inspection | Implemented; requires projected metre-based CRS and approximately 5 m pixels | `src/moonsight/data/downloader.py` |
| Synthetic raster validation tests | Written; local focused CRS check passed | `tests/test_downloader.py` |
| Bounded raster sample statistics | Implemented; three isolated tests passed | `src/moonsight/data/summary.py`, `tests/test_summary.py` |
| Bounded terrain heatmap preview | Implemented; four focused isolated tests passed; full repository suite pending | `src/moonsight/terrain/preview.py`, `tests/test_terrain_preview.py` |
| Streamlit terrain heatmap display | Implemented; app launch pending | `app.py` |
| Streamlit download and sample-statistics interface | Implemented; app not yet launched | `app.py` |

## Test note

A focused local run of the terrain-preview logic completed with **4 tests passed** using synthetic GeoTIFFs. It covered NoData masking, pixel-centre coordinates, sample-size limits, and Plotly figure construction. The run used an isolated temporary test package mirroring the committed module; it is not a full clean-checkout test run.

A local isolated test run of the raster-summary module completed with **3 tests passed** using synthetic GeoTIFF files. A separate focused check confirmed that a projected metre-based test CRS is accepted and a geographic CRS is rejected. These are targeted checks, not a complete `pytest` run from a clean clone of this repository.

## NASA source facts

The official NASA archive lists Site01, Site04, Site07, Site11, Site20, and Site23, and provides the exact product filenames for elevation, spot count, slope, total elevation uncertainty, and slope uncertainty. It describes these GeoTIFFs as 5 m/pixel, with south-polar stereographic X/Y coordinates in metres and the MOON_ME reference frame tied to DE421.

Official archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

NASA product page: https://pgda.gsfc.nasa.gov/products/78

The Site04 elevation filename is `Site04_final_adj_5mpp_surf.tif`. The official archive links to it under the Site04 directory. The browser retrieval service used for this development session cannot download the TIFF media type, and a direct container download attempt also failed. Therefore no real raster has yet been retrieved or validated in this session.

## Validation policy

- Reject non-TIFF responses, including HTML error pages.
- Enforce a configurable maximum download size (default 512 MiB).
- Download to a temporary file and move it into the cache only after validation.
- Require Rasterio to open the file.
- Require a projected coordinate reference system with metre units. This generic check does not by itself verify the exact lunar projection or MOON_ME/DE421 reference frame; that must be checked against the real file metadata and NASA documentation.
- Require positive raster dimensions.
- Check for approximately 5 m pixels before accepting the file.
- Record file path, dimensions, band count, CRS, pixel size, bounds, data type, and NoData value.
- Calculate descriptive statistics from a bounded nearest-neighbour sample, not the entire raster.
- Exclude NoData and non-finite values from sample statistics.
- Label all sample statistics clearly; they are not full-raster summaries or landing criteria.
- Do not interpret metadata validation as proof of terrain quality or landing suitability.

## Coordinate-reference wording correction

The current downloader checks only that the raster CRS is projected and uses metres. It does **not** yet compare the CRS definition with the exact lunar south-polar stereographic / MOON_ME / DE421 reference information described by NASA. The app therefore labels map axes as projected coordinates and explicitly tells users to inspect the CRS metadata; it does not claim the frame has been independently verified. The synthetic tests use EPSG:3031 only as a generic projected-metre test CRS, not as a lunar CRS.

## Additional engineering correction

During code review, the TIFF byte-order/magic signatures were found to be represented incorrectly as escaped text in Python byte literals. They have been replaced with exact four-byte hexadecimal signatures, and the positive/negative header tests now use exact byte sequences. This fix is committed; the full test suite still needs to be run from a clean checkout.

## Remaining work

- [ ] Install the package and dependencies in a clean environment.
- [ ] Run the complete `pytest` suite from the GitHub checkout, including the new terrain-preview tests.
- [ ] Run `ruff check .` and fix any findings.
- [ ] Launch the Streamlit app.
- [ ] Download one real NASA product (start with Site04 elevation) from the app and record its metadata.
- [ ] Confirm file size, CRS, dimensions, transform, NoData value, and pixel scale against source documentation.
- [ ] Inspect sample values and confirm they are finite and physically plausible for the product.
- [ ] Add a data provenance record for the downloaded file.
- [ ] Only then expand testing to the remaining sites and product types.

## Current status

**Data retrieval and sample-statistics code committed; targeted synthetic tests passed.** A real NASA raster, the full GitHub checkout, and the Streamlit app remain unverified. MoonSight does not yet produce site rankings or landing-safety conclusions.
