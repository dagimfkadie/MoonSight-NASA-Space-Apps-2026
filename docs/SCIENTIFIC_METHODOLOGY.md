# Scientific methodology and assumptions

This document is a framework for recording methods as they are implemented. It does not claim that the calculations below are already implemented.

## 1. Evidence categories

Every displayed result must be labeled as one of:

- **Source observation/product:** downloaded directly from an identified archive or API.
- **Derived quantity:** calculated from source values using a documented method.
- **Illustration:** a conceptual visual that is not a scientific measurement.

## 2. LOLA terrain products

NASA's South Pole Landing Site LOLA DEM archive lists these products:

| Product | Meaning | Units stated by source |
|---|---|---|
| LDEM / surface elevation | Surface-interpolated height | metres |
| Slope | Terrain slope | degrees |
| LDEC | LOLA return count per pixel | count |
| Total Z uncertainty | RMS elevation uncertainty | metres |
| Slope uncertainty | RMS slope uncertainty | degrees |

The listed GeoTIFF products are 5 m/pixel and use south-polar stereographic X/Y coordinates in metres, MOON_ME reference frame, ephemeris DE421.

Source: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

### Raster handling requirements

Before calculating statistics:
1. Read CRS, transform, pixel registration, nodata and raster dimensions.
2. Verify the product type and units against its metadata.
3. Mask nodata and all non-finite values.
4. Report valid-pixel count and fraction.
5. State the spatial footprint and whether values were resampled.
6. Do not interpret an interpolated elevation value as a direct laser return.

### Slope

For a raster elevation surface (z(x,y)), a common local slope expression is:

[
\theta = \arctan\left(\sqrt{
\left(\frac{\partial z}{\partial x}\right)^2+
\left(\frac{\partial z}{\partial y}\right)^2
}\right)
]

This formula is only a general definition. MoonSight should prefer the archived NASA slope product when its provenance and metadata match the selected elevation product. Any independently derived slope must document the algorithm, grid spacing, edge treatment, and uncertainty.

## 3. Sun and Earth geometry

JPL Horizons observer ephemerides can return apparent azimuth and elevation for a correctly defined topocentric observer. MoonSight requests observer-table quantity 4 for targets Sun (ID 10) and Earth (ID 399), with `CENTER=coord@301`, `COORD_TYPE=GEODETIC`, `SITE_COORD=east longitude,latitude,altitude in km`, `APPARENT=AIRLESS`, and UTC time tags. The app requires users to confirm that the coordinates are documented; it does not infer them from a LOLA tile ID. The client checks the API signature/version and parses the CSV ephemeris table.

- Azimuth is conventionally measured clockwise from north.
- Elevation is measured relative to the local plane perpendicular to the zenith direction.
- Geometric elevation above zero does not prove unobstructed visibility when nearby terrain is present.

Source: https://ssd-api.jpl.nasa.gov/doc/horizons.html

## 4. Illumination

A first geometric indicator is whether the apparent solar center is above the local geometric horizon. It is not the fraction of time a surface receives sunlight and is not available electrical power.

A physically meaningful local illumination analysis must account for terrain horizon obstruction, surface orientation, time sampling, and the chosen solar-disk convention. Any future calculation must document these inputs and validate against an authoritative reference.

No power-generation estimate should be made without additional engineering assumptions such as panel orientation, efficiency, temperature, degradation, and system losses.

## 5. Earth visibility and communications

Earth apparent elevation above a geometric horizon is only a geometric indicator. A terrain-aware line-of-sight analysis requires a suitable terrain horizon profile at the observer's position.

Even unobstructed geometric visibility does not establish a functioning radio link. Communication feasibility also depends on antenna patterns, frequency, link budget, transmit power, receiver sensitivity, pointing, interference, and spacecraft/system design.

## 6. Uncertainty and limitations

- Preserve NASA uncertainty layers rather than hiding them.
- Do not convert RMS uncertainty into a confidence interval without a justified statistical model.
- Do not compare values from different spatial footprints as though they were equivalent.
- Do not claim a site is safe, optimal, or approved for landing.
- Report missing data and assumptions visibly.

## 7. Validation record

For every implemented scientific calculation, record:
- Formula and units.
- Source inputs and retrieval timestamp.
- Coordinate frames and time scale.
- Assumptions and approximations.
- Numerical tests and independent comparison.
- Known limitations and uncertainty.
