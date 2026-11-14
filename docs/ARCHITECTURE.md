# MoonSight software architecture

## Architectural goals

- Separate the interface from data retrieval and scientific calculations.
- Preserve source provenance and coordinate/time metadata.
- Reject malformed inputs and invalid measurements rather than inventing defaults.
- Keep numerical functions independently testable.
- Distinguish source observations/products, derived values and illustrative visualizations.

## Layers

### Presentation — `app.py`

Streamlit interface with four tabs: Terrain Explorer, Compare Regions, Sun & Earth Geometry, and Data & Limitations. The interface orchestrates service calls and displays assumptions and caveats; calculations belong in package modules.

### Catalog — `moonsight.catalog`

Contains six source-listed NASA LOLA study-region identifiers and names. It deliberately does not invent geographic coordinates for these regions.

### Data access — `moonsight.data`

- `lola.py`: builds URLs for known NASA LOLA product types.
- `downloader.py`: bounded HTTP download, temporary-file handling, caching and basic GeoTIFF validation.
- `summary.py`: bounded nearest-neighbour raster sample statistics.

### Terrain — `moonsight.terrain`

- `preview.py`: bounded single-band raster preview, NoData masking, projected coordinate axes, 2-D heatmap and 3-D surface rendering.
- The 3-D surface is intended for elevation products only. It is a downsampled visualization, not a terrain hazard model.

### Astronomy — `moonsight.astronomy`

- `horizons.py`: constructs JPL Horizons observer requests for the Sun and Earth from a user-entered lunar geodetic coordinate; validates inputs and API signature; parses apparent azimuth/elevation output.
- Coordinates are not inferred from LOLA tile IDs.
- Live request verification and independent comparison against the Horizons interface remain outstanding.

### Comparison

The UI compares bounded descriptive statistics for the same LOLA product across two selected regions. It does not calculate a weighted score, infer suitability or rank sites.

### Visibility and communications

No terrain-aware horizon ray tracing or radio link-budget model is implemented. Horizons elevation is only a geometric direction indicator. These future modules must not be presented as complete.

## Data flow

1. User selects a LOLA archive region and product, or enters a lunar observer coordinate and date.
2. Input validation checks allowed product IDs, coordinate ranges and request duration.
3. Data service retrieves NASA LOLA GeoTIFFs or JPL Horizons JSON.
4. Domain modules validate metadata and calculate bounded summaries or parse apparent observer directions.
5. Tests and quality checks are run before release.
6. UI presents values with units, provenance, assumptions and limitations.

## Coordinate and data integrity

NASA describes the South Pole Landing Site LOLA GeoTIFFs as 5 m/pixel, south-polar stereographic X/Y coordinates in metres, MOON_ME reference frame, ephemeris DE421. The current downloader only checks projected CRS, metre units and approximately 5 m pixels. It does not yet verify that the exact CRS WKT and lunar frame match NASA's complete specification.

NASA archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

## JPL Horizons

Horizons API: https://ssd-api.jpl.nasa.gov/doc/horizons.html

The client requests observer-table quantity 4 (apparent azimuth/elevation) using a lunar surface observer coordinate with `CENTER=coord@301`, geodetic coordinate order east longitude, latitude, altitude in kilometres, and airless output. The user must provide a documented lunar coordinate. The app must not treat a default input as a known study-region coordinate.

## Known limitations

- Live NASA GeoTIFF download and exact lunar CRS metadata verification remain pending.
- Live JPL Horizons requests and comparison against an independently configured Horizons query remain pending.
- The 2-D/3-D views use bounded samples, not full-resolution display.
- No terrain obstruction, illumination duration, available solar power, radio link budget, or landing-safety model is implemented.
- A successful API request or attractive plot is not independent scientific validation.
