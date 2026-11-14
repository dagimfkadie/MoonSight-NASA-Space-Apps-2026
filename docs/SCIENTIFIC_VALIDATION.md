# Scientific validation plan and evidence record

This document defines how MoonSight's data handling and scientific outputs should be checked, what evidence the current repository tests provide, and which validation claims remain unverified. It distinguishes software correctness from scientific validity.

> **Scope:** MoonSight is an educational research prototype. It is not a landing-safety system, mission-design tool, or NASA-certified application. Passing unit tests does not establish landing suitability or operational mission readiness.

## 1. Validation principles

Every validation claim should identify:

1. **Claim:** What exactly is being asserted?
2. **Input:** Which source file, API response, coordinates, units and time are used?
3. **Method:** What calculation or comparison is performed?
4. **Expected result:** What independently established result or invariant is expected?
5. **Tolerance:** What numerical difference is acceptable, and why?
6. **Evidence:** Test output, source metadata, request parameters, comparison record or reproducible artifact.
7. **Limitations:** What the validation does not prove.

Use three distinct evidence categories:

- **Software verification:** Does the implementation behave as intended for controlled inputs?
- **Data validation:** Does retrieved data match provider metadata and expected structure?
- **Scientific validation:** Do calculated results agree with an independent authoritative method or reference within a justified tolerance?

Do not use one category as a substitute for another.

## 2. Current repository test coverage

The project configures pytest to discover tests under `tests/` and uses `src` as the Python import path. Development dependencies include pytest and Ruff.

The checked-in tests currently cover the following:

| Area | Existing test evidence | What it verifies | What it does not verify |
|---|---|---|---|
| LOLA catalogue | `tests/test_catalog.py` | Six configured site IDs, one displayed name, unknown-site rejection and common NASA archive URL | Geographic boundaries, exact coordinates or independent confirmation of all catalogue metadata |
| TIFF / raster inspection | `tests/test_downloader.py` | Classic TIFF header acceptance, invalid header rejection, missing file handling, synthetic projected raster metadata and rejection of a geographic CRS | Live NASA downloads, NASA-specific lunar CRS identity, all archive metadata or complete HTTP/cache behavior |
| Raster summaries | `tests/test_summary.py` | Synthetic raster statistics, NoData exclusion, all-NoData rejection and invalid sample-size rejection | Full-resolution statistics, live archive values or independent scientific accuracy of NASA source products |
| Horizons parser/client | `tests/test_horizons.py` | CSV parsing, unavailable angle handling, missing delimiter rejection, invalid input rejection and request construction using a fake session | Live Horizons service behavior, actual coordinate correctness or independent ephemeris agreement |
| Terrain preview | `tests/test_terrain_preview.py` | Pixel-centre coordinates, NoData masking, bounded sampling, heatmap axes and sampled surface values | Does not verify a live NASA raster's lunar CRS or scientific suitability |

The downloader test uses a synthetic raster with `EPSG:3031` and a 5 m pixel size. This is a test fixture for generic projected-metre validation; it is **not** a lunar CRS and must not be presented as evidence that MoonSight validates the NASA MOON_ME / DE421 reference definition.

These tests are controlled software tests. A fake Horizons session proves the request parameters and parser behavior under the supplied fixture; it does not prove that a live query returns correct results.

## 3. LOLA source-data validation

### 3.1 Provider metadata checks

For each selected NASA GeoTIFF, record and independently compare:

- Exact archive URL and product filename.
- Product identifier and intended meaning.
- Raster dimensions and band count.
- Full CRS WKT / authority information and coordinate axis definitions.
- Lunar reference frame and ephemeris realization, where stated by the source.
- Pixel size, transform, bounds and pixel registration.
- Data type, units, scale/offset, NoData value and mask behavior.
- Provider documentation and retrieval timestamp.

NASA's South Pole archive page was reviewed on 2026-11-14. It lists the six study regions used by MoonSight (Site01, Site04, Site07, Site11, Site20 and Site23), describes the available elevation, spot-count, slope and uncertainty products, and states that the GeoTIFFs are 5 m/pixel south-polar stereographic grids with X/Y in metres in the MOON_ME reference frame of ephemeris DE421. The archive page also identifies the product meanings and headline units: elevation in metres, spot counts, slope in degrees, and elevation/slope uncertainty as RMS quantities. This is a source-documentation check only; it does not establish the metadata tags or contents of a downloaded binary file.

The current code only checks projected CRS, metre units and pixel dimensions within 4–6 m. It does not yet verify the full lunar CRS definition. This remains a known validation gap. A real GeoTIFF still needs to be retrieved and inspected, and its full CRS WKT, pixel registration, transform, data type, scale/offset and NoData behavior compared with authoritative product documentation. The archive page does not, by itself, provide enough evidence to certify all of those file-level properties. The provenance timestamp is the local file modification time, not a NASA server-side modification timestamp; record the UTC retrieval time separately when collecting live evidence.

### 3.2 File integrity and retrieval

For a live retrieval evidence record, retain:
- Request URL and UTC retrieval time.
- HTTP status and relevant response headers, where available.
- File size and SHA-256 checksum.
- Rasterio-readable metadata.
- Any download or validation errors.

Test both successful and unsuccessful retrieval paths using controlled HTTP fixtures. Do not use a live network dependency as the only way to test downloader logic.

### 3.3 Product identity and units

For every product type, verify the filename suffix, semantic meaning, units and NoData convention against the provider's product-specific metadata. Do not infer that a filename alone proves the product's contents.

Preserve uncertainty products as source-provided RMS quantities. Do not relabel RMS error as a confidence interval without a statistical model that justifies that interpretation.

## 4. Raster calculation validation

### 4.1 Summary statistics

Use small synthetic rasters with known values to check:
- Minimum, maximum, mean, median and percentile calculations.
- NoData and non-finite value exclusion.
- Valid and invalid sample counts.
- Behavior when all sampled values are invalid.
- Sample dimensions and nearest-neighbour decimation.
- Correct product units and labels.

For a full-size source raster, independently calculate a reference result on the same explicitly defined sample grid. Compare results using exact equality for deterministic integer/count cases where appropriate, and justified floating-point tolerances for floating-point calculations.

The UI must continue to label these outputs as bounded sample statistics, not full-raster statistics.

### 4.2 Preview coordinates and masks

Add dedicated synthetic-raster tests for:
- Pixel-centre X/Y coordinates from the affine transform.
- Positive and negative Y pixel resolution.
- NoData and non-finite values represented as missing.
- Sample shape and valid/NoData counts.
- Rejection of rotated/sheared rasters if unsupported.
- Heatmap and surface axes corresponding to the sampled raster.

Where possible, construct a synthetic raster with a known affine transform and check each expected pixel-centre coordinate numerically.

### 4.3 Slope and terrain interpretation

MoonSight currently displays the archived slope product; it does not implement a complete landing-hazard assessment. If a derived slope calculation is introduced later, document the derivative algorithm, grid spacing, edge handling, units, nodata behavior and uncertainty propagation. Compare it against a controlled analytical surface and an independent implementation.

A slope value alone does not describe obstacle size, roughness at all scales, lander dynamics, or landing safety.

## 5. JPL Horizons request and ephemeris validation

### 5.1 Request construction

Check that every request explicitly records:
- Target ID (Sun 10 or Earth 399).
- Observer centre (`coord@301` in the current implementation).
- Geodetic coordinate type.
- East longitude, latitude and altitude order and units.
- Start/stop dates, time step and UTC time convention.
- Quantity 4 and apparent/airless settings.
- API signature/version returned by the service.

The current code checks coordinate ranges and confirms the Horizons response signature/source label. User confirmation of coordinate provenance is not a substitute for independently checking the coordinate itself.

### 5.2 Parser validation

Use saved, representative response fixtures to verify:
- Correct extraction between `$$SOE` and `$$EOE`.
- Correct timestamp, azimuth and elevation columns.
- Missing/unavailable values remain missing rather than becoming zero.
- Malformed and empty tables produce clear errors.
- Unexpected response structures and API error messages are handled.

Fixtures should be retained with their origin and date. Do not fabricate a fixture and describe it as a real NASA response.

### 5.3 Independent comparison

For a live validation, choose a documented lunar geodetic observer coordinate and UTC time. Submit the same target, observer, coordinate convention, time interval, time step and apparent settings to:
1. MoonSight's API client.
2. An independently configured JPL Horizons query or a provider-supplied reference example.

Compare timestamps and angular outputs after confirming that the settings and conventions are identical. Define a tolerance before reviewing the difference, explain the tolerance, and preserve the raw response and comparison record.

A plausible-looking plot is not validation. A fake-session unit test is not a live-service validation.

## 6. Geometry and interpretation checks

The current Horizons output is apparent azimuth and elevation at the user-entered observer location. It is a geometric direction indicator only.

Before claiming local visibility, a future terrain-aware model would need:
- Correct observer location and local coordinate frame.
- A verified terrain elevation model covering the relevant horizon.
- A documented horizon-profile or ray-intersection algorithm.
- Appropriate spatial resolution and treatment of missing terrain.
- Tests against synthetic terrain with known blocked and unblocked directions.

Before claiming solar illumination duration, a future model would additionally need a documented time sampling method, solar-disk convention, local terrain obstruction and surface orientation.

Before claiming communications availability, a future model would need a radio link budget and engineering assumptions. Earth elevation alone is not a communications model.

No current MoonSight feature validates landing safety, optimality or site approval.

## 7. Reproducible validation record template

Create one record per live source or independent comparison. Do not mark a record complete until the evidence is saved.

| Field | Record |
|---|---|
| Validation ID | Unique identifier |
| Date/time (UTC) | When validation was performed |
| Git commit | Exact code revision |
| Claim under test | One precise claim |
| Source / endpoint | Provider and exact URL |
| Input identifiers | Site, product, target, coordinate, time |
| Input metadata | CRS, units, NoData, parameters |
| Method | Steps and calculation |
| Expected reference | Independent source or known synthetic answer |
| Tolerance | Numerical tolerance and rationale |
| Observed result | Actual output and difference |
| Evidence files | Raw metadata, response, checksum, logs or comparison |
| Status | Not started / In progress / Passed / Failed |
| Limitations | What remains unverified |

## 8. Current validation status

The following status distinguishes automated software checks from live data and scientific validation. GitHub Actions passed on current merged `main` commit `2f7974e807f7ba1ad9293f11a3e18e2469fba251` (workflow run [#131](https://github.com/dagimfkadie/MoonSight-NASA-Space-Apps-2026/actions/runs/43591451169)). The clean Ubuntu/Python 3.11 workflow compiled sources, ran Ruff and completed the full pytest suite: 46 tests passed, including the Streamlit AppTest startup smoke test. The NASA archive catalogue/specification page was also reviewed on 2026-11-14; this confirms the provider's published product description, not a live file download or file-level CRS validation.

| Validation item | Status |
|---|---|
| Synthetic TIFF inspection tests | Implemented and included in the passing CI run; does not validate lunar CRS |
| Synthetic raster summary tests | Implemented and included in the passing CI run |
| Horizons parser and fake-session request tests | Implemented and included in the passing CI run; no live-service proof |
| Dedicated terrain preview tests | Implemented in `tests/test_terrain_preview.py` and included in the passing CI run |
| NASA archive catalogue and published product-specification review | Completed on 2026-11-14; confirms listed sites, product families, 5 m/pixel south-polar stereographic grids, metre X/Y coordinates and MOON_ME / DE421 description only |
| Live NASA LOLA GeoTIFF retrieval and file-integrity evidence | Pending |
| Exact file-level MOON_ME / DE421 CRS WKT verification | Pending |
| Per-file scale/offset and NoData metadata audit | Pending |
| Live JPL Horizons request with documented coordinates | Pending |
| Independent Horizons result comparison | Pending |
| Terrain-aware horizon / illumination validation | Not implemented |
| Communications link-budget validation | Not implemented |
| Landing hazard or safety validation | Not implemented |

## 9. References

- NASA LOLA South Pole Landing Site DEM archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA LOLA product information: https://pgda.gsfc.nasa.gov/products/78
- NASA/JPL Horizons API documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- Rasterio documentation: https://rasterio.readthedocs.io/
- pytest documentation: https://docs.pytest.org/
