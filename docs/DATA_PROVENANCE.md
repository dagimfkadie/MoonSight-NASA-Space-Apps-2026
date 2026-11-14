# Data provenance and source register

This document records the external datasets and services used by MoonSight, how the current code requests them, and what the application does (and does not) validate. It is intended to make the origin and interpretation of displayed information traceable.

**Status:** Repository-level documentation of implemented data-access paths. A documented source or code path is not proof that a live download/query has been completed successfully in the current environment.

## 1. Source register

| Source | Provider | MoonSight use | Primary reference |
|---|---|---|---|
| South Pole Landing Site LOLA DEM archive | NASA Planetary Geodesy and Cartography Working Group / Goddard Space Flight Center archive | Regional GeoTIFF terrain products | https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/ |
| LOLA product information | NASA archive | Context for the archive's gridded products | https://pgda.gsfc.nasa.gov/products/78 |
| Horizons API | NASA/JPL Solar System Dynamics | Apparent Sun/Earth observer directions for user-entered lunar coordinates | https://ssd-api.jpl.nasa.gov/doc/horizons.html |

Users should consult the provider documentation for authoritative metadata, updates, access conditions and interpretation. MoonSight is an independent educational prototype and is not a NASA product or endorsement.

## 2. NASA LOLA South Pole products

### 2.1 Study-region catalogue

The application catalogue contains these six archive region identifiers and names:

| Archive ID | Name shown in MoonSight |
|---|---|
| Site01 | Connecting ridge |
| Site04 | Shackleton rim |
| Site07 | Peak near Shackleton |
| Site11 | de Gerlache rim |
| Site20 | Leibnitz beta plateau |
| Site23 | Malapert massif |

These labels are transcribed into `src/moonsight/catalog.py` from the NASA archive listing. They identify archive product groups; they are not precise observer coordinates, polygon boundaries, or a statement that the entire named region has uniform terrain properties.

MoonSight intentionally does not assign latitude/longitude values to these labels. The Horizons tab requires a separately supplied lunar observer coordinate.

### 2.2 Product types and file naming

The URL registry in `src/moonsight/data/lola.py` supports five product types. For a known site, it constructs a filename in this pattern:

```text
{SITE_ID}_final_adj_5mpp_{SUFFIX}.tif
```

| MoonSight product key | File suffix | Meaning in the interface | Display units |
|---|---|---|---|
| `elevation` | `surf` | Surface elevation | metres |
| `slope` | `slp` | Terrain slope | degrees |
| `spot_count` | `ldec` | LOLA return count per pixel | LOLA returns per pixel |
| `elevation_uncertainty` | `toterr` | Total elevation uncertainty | metres RMS error |
| `slope_uncertainty` | `slperr` | Slope uncertainty | degrees RMS error |

The suffix mapping and names above describe the application's URL registry and labels. Always check the individual archive product's metadata and documentation before interpreting a downloaded file.

### 2.3 Archive-reported spatial reference and resolution

The NASA archive describes these products as 5 m/pixel GeoTIFFs with south-polar stereographic X/Y coordinates in metres, MOON_ME reference frame, and DE421 ephemeris.

The current downloader in `src/moonsight/data/downloader.py` checks that a raster:
- Has a classic TIFF header and can be opened by Rasterio.
- Has positive dimensions and at least one band.
- Has a projected coordinate reference system.
- Reports linear units in metres.
- Has pixel dimensions between 4 m and 6 m in each axis.

**Important validation gap:** these checks do not compare the complete CRS definition/WKT against the archive's exact lunar south-polar stereographic and MOON_ME / DE421 specification. A projected CRS measured in metres with approximately 5 m pixels is not, by itself, proof that the file has the correct lunar reference frame. The UI currently describes the checks as basic validation and explicitly notes this limitation.

## 3. Retrieval, caching and file handling

The data-access path is:

1. The user selects a catalogue site and one supported product.
2. `build_lola_product_url()` constructs the archive URL from the known site ID and product suffix.
3. `download_lola_geotiff()` checks the local cache at `data/cache/lola`.
4. An existing cached file is revalidated before reuse. An invalid cached file is removed.
5. A new response is streamed to a temporary file. The downloader checks the TIFF header, rejects HTML responses, enforces a configurable maximum size (512 MiB by default), and checks the raster before atomically moving it into the cache.
6. Raster metadata is returned to the application for display and subsequent processing.

The downloader uses a timeout and does not intentionally leave a partial download at the final cache path. The default maximum file size is a software safeguard, not a NASA archive limit.

### Metadata currently retained for display

The `RasterMetadata` record now includes:
- Local cached path and original NASA source URL
- File modification timestamp in UTC (not represented as an authoritative provider timestamp)
- File size and SHA-256 checksum, calculated incrementally without loading the full raster into memory
- Raster width and height and band count
- CRS identifier/string and full CRS WKT as reported by Rasterio
- Affine transform, pixel width/height and raster bounds
- Data type and NoData value

The application displays this metadata and offers a JSON provenance-manifest download. The NASA source GeoTIFF is also linked directly from the terrain result. The checksum identifies the local file contents; it does not independently prove the file's scientific correctness. The application still does not persist original HTTP ETag/Last-Modified headers or independently verify that the full CRS WKT is the expected MOON_ME / DE421 definition.

## 4. Raster sampling and derived summaries

The application does not load every pixel for its interactive summaries and previews.

### 4.1 Summary statistics

`summarize_lola_raster()` reads band 1 using nearest-neighbour resampling into a sample no larger than 512 × 512 pixels by default. It excludes masked NoData and non-finite values and reports:
- Sample dimensions
- Valid and NoData sample counts
- Minimum and maximum
- Mean and median
- 95th percentile
- Product name, units and sampling description

These are statistics of the sampled grid, not full-resolution statistics for the complete source raster. The sample count is not the total number of source pixels.

### 4.2 Visual previews

`load_terrain_preview()` also reads a bounded nearest-neighbour sample, masks NoData/non-finite values, and calculates projected X/Y pixel-centre coordinates for display. The application renders a 2-D heatmap and, for elevation, a 3-D surface.

The previews are visual aids. They are not a terrain-hazard model, a high-resolution landing simulation, or evidence of safe slopes/obstacles. Plot perspective and vertical scaling can affect visual interpretation.

## 5. NASA/JPL Horizons observer ephemerides

### 5.1 Endpoint and target identifiers

The client in `src/moonsight/astronomy/horizons.py` sends requests to:

```text
https://ssd.jpl.nasa.gov/api/horizons.api
```

It supports:
- Sun: target ID `10`
- Earth: target ID `399`
- Moon centre: ID `301`, used in `CENTER=coord@301`

### 5.2 Observer definition and request settings

The current request uses:
- `EPHEM_TYPE=OBSERVER`
- `COORD_TYPE=GEODETIC`
- `SITE_COORD=east longitude, latitude, altitude`
- Longitude and latitude in degrees; altitude in kilometres
- `QUANTITIES=4` for apparent azimuth/elevation
- `APPARENT=AIRLESS`
- `TIME_TYPE=UT`
- `STEP_SIZE=1h`
- A user-selected start date and duration of 1–3 days

The app validates the input ranges and requires the user to confirm that the coordinate source and geodetic definition have been independently verified. This confirmation is a user acknowledgement, not an automated validation of the coordinate's correctness.

The code does not infer an observer coordinate from Site01, Site04, Site07, Site11, Site20 or Site23. A query is only meaningful when the entered coordinates are appropriate for the intended lunar observer location and the Horizons coordinate convention.

### 5.3 Response parsing and checks

The client requests JSON, checks the returned API signature/version and source label, then parses the ephemeris text between the `$$SOE` and `$$EOE` delimiters. It extracts the timestamp, apparent azimuth and apparent elevation from the expected CSV columns.

The app displays the returned records and plots elevation over time. A successful response means the API returned parseable ephemeris data; it does not independently validate the user's observer coordinate or establish physical visibility at a real surface location.

## 6. Interpretation boundaries

| Displayed information | What it can support | What it cannot establish |
|---|---|---|
| LOLA elevation | Description of gridded surface height in the source reference frame | Landing clearance or hazard-free terrain |
| LOLA slope | Description of the source slope product | Complete landing safety or vehicle stability |
| LOLA return count | Context about source measurement density | Uniform accuracy or absence of hazards |
| LOLA uncertainty products | Source-provided RMS uncertainty context | Confidence intervals unless a justified statistical model is supplied |
| Sample statistics | Descriptive comparison of the sampled cells | Full-raster statistics or fair ranking across unequal footprints |
| Sun azimuth/elevation | Apparent geometric direction at the entered observer coordinate and times | Terrain-unobstructed sunlight, illumination duration, or electrical power |
| Earth azimuth/elevation | Apparent geometric direction at the entered observer coordinate and times | Terrain-unobstructed line of sight or a working radio link |

MoonSight currently does not implement:
- Terrain-aware horizon obstruction or ray tracing.
- A validated surface illumination-duration model.
- Solar-array power or energy estimation.
- A radio-frequency link budget or communications availability model.
- A landing hazard assessment, landing-safety score, or site approval model.

No MoonSight output should be described as certifying a site as safe, optimal, or approved for landing.

## 7. Reproducibility and recommended provenance improvements

For a future reproducible release, record the following for every retrieved source file or API request:

1. Provider and exact source URL/endpoint.
2. Retrieval timestamp in UTC.
3. Exact site ID, product identifier and target ID.
4. Original filename and file size.
5. Provider metadata, including full CRS WKT and NoData definition.
6. A cryptographic checksum (for example SHA-256) for downloaded files.
7. Request parameters and Horizons API signature/version, excluding secrets (none are expected for this public endpoint).
8. Software version / Git commit used to produce the derived output.
9. Sampling/resampling method, units, valid-data count and all transformations.
10. Validation result and any known warning or limitation.

These are recommended provenance enhancements, not claims that all fields are currently captured by MoonSight.

## 8. Verification status

The source URLs and implementation details in this document were checked against the repository code when this document was written. The following should be recorded as **pending until actually performed and evidenced**:

- Successful retrieval of each selected LOLA product from the live NASA archive.
- Verification of complete CRS WKT and lunar reference frame against the NASA product metadata.
- Independent confirmation of product suffixes, units and NoData conventions against the provider metadata.
- A live Horizons query with a documented lunar observer coordinate.
- Comparison of a Horizons result against an independently configured query or authoritative example.
- Recording of retrieval timestamps and checksums for submitted sample data.

Do not change a pending item to verified merely because the relevant code exists or a unit test passes.

## 9. References

- NASA LOLA South Pole Landing Site DEM archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA LOLA product information: https://pgda.gsfc.nasa.gov/products/78
- NASA/JPL Horizons API documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- Rasterio documentation: https://rasterio.readthedocs.io/
