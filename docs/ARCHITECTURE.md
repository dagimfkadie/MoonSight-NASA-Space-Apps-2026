# MoonSight software architecture

## Architectural goals

- Keep the user interface separate from scientific calculations.
- Keep source data provenance attached to every data workflow.
- Reject malformed inputs and invalid measurements rather than inventing defaults.
- Make numerical functions independently testable.
- Clearly distinguish measured/source data, derived values, and illustrative graphics.

## Application layers

### Presentation: `app.py`

Streamlit entry point. It displays the application status and calls package services. It must not contain scientific formulas or silently fabricate data.

### Domain catalog: `moonsight.catalog`

Contains source-verified study-region identifiers and labels. Coordinates are deliberately excluded until their definitions and coordinate frames are verified from authoritative metadata.

### Data access: `moonsight.data`

Future responsibilities:
- Construct and validate source URLs.
- Retrieve NASA/JPL responses with timeouts and clear error handling.
- Cache successful responses using source URL and request parameters as cache keys.
- Record retrieval time, source, product identifier, units, coordinate reference, and version where available.

### Terrain: `moonsight.terrain`

Future responsibilities:
- Open LOLA GeoTIFF products with Rasterio.
- Read CRS, transform, dimensions, pixel registration, nodata and units.
- Mask nodata and non-finite pixels.
- Report valid-pixel coverage and descriptive statistics.
- Keep source resolution separate from any downsampled display resolution.

### Astronomy: `moonsight.astronomy`

Future responsibilities:
- Build documented JPL Horizons observer requests.
- Parse API version, error messages, time tags, azimuth and elevation.
- Validate the observer location and coordinate conventions.
- Preserve the exact query settings with returned data.

### Visibility: `moonsight.visibility`

Future responsibilities:
- Determine geometric visibility relative to a defined local horizon.
- Add terrain obstruction only when a suitable, correctly registered terrain profile is available.
- Keep geometric line-of-sight separate from radio-frequency link feasibility.

### Comparison: `moonsight.comparison`

Future responsibilities:
- Compare like-for-like products, dates, units, resolutions and spatial footprints.
- Display evidence and limitations side by side.
- Avoid unsupported weighted scores or claims of landing safety.

### Visualization: `moonsight.visualization`

Future responsibilities:
- Render maps and plots with units, legends, source attribution and clear missing-data handling.
- Make clear whether a view is full resolution, resampled, or illustrative.

## Data flow

1. User selects a documented study region, product, and date.
2. Input validation checks supported choices and coordinate definitions.
3. Data service retrieves the original NASA/JPL response.
4. Domain modules validate source metadata and calculate derived quantities.
5. Tests and quality checks run before results are exposed.
6. Presentation displays results with provenance and limitations.

## Current implementation boundary

The initial foundation contains the Streamlit shell, a source-cited list of six NASA LOLA study-region labels, package directories, and catalog tests. It does not yet retrieve NASA data or calculate astronomy, terrain, or visibility results.

## NASA LOLA source characteristics

NASA's South Pole Landing Site LOLA DEM archive describes 5 m/pixel GeoTIFF products, with south-polar stereographic X/Y coordinates in metres and a MOON_ME reference frame tied to ephemeris DE421. Product groups include elevation, slope, return counts, and uncertainty layers. The exact metadata of each downloaded file must still be inspected before processing.

Source: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

## JPL Horizons integration

Horizons observer ephemerides can provide apparent azimuth and elevation when configured for a topocentric observer. The implementation must verify the observer-center and coordinate options supported for a lunar surface site. Earth-based defaults must not be reused for lunar observers.

API documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html

## Error handling

- Network timeout: show source and retry guidance; do not show stale values as current.
- API error response: surface the returned error safely.
- Missing raster: identify the requested product and source URL.
- Invalid raster metadata: stop analysis and report the mismatch.
- Missing pixels: mask and report coverage; never replace missing values with zero.
- Unsupported coordinate system: stop rather than guessing a transformation.
