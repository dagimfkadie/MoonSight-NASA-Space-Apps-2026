# MoonSight user guide

MoonSight is an educational prototype for exploring NASA lunar south-pole LOLA terrain products and apparent Sun/Earth directions from JPL Horizons. This guide describes the current Streamlit interface in the repository.

> **Important:** MoonSight is not a flight system and does not certify landing safety, mission feasibility, terrain clearance, solar-power availability, or operational communications capability. Its comparisons are descriptive, not site rankings.

## 1. Requirements

- Python 3.10 or newer
- Internet access to retrieve NASA LOLA GeoTIFFs and query JPL Horizons
- A supported environment for Rasterio and its geospatial dependencies

## 2. Install and launch

Clone the repository:

```bash
git clone https://github.com/dagimfkadie/MoonSight-NASA-Space-Apps-2026.git
cd MoonSight-NASA-Space-Apps-2026
```

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package and development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Start the app:

```bash
streamlit run app.py
```

Streamlit prints a local address in the terminal. Open that address in a browser.

## 3. Terrain explorer

1. Open **Terrain explorer**.
2. Select one of the six NASA LOLA study-region product groups.
3. Select a product:
   - Elevation (metres)
   - Slope (degrees)
   - LOLA spot count
   - Elevation uncertainty (metres)
   - Slope uncertainty (degrees)
4. Select **Download and inspect NASA LOLA product**.
5. Review the raster metadata, sample statistics and 2-D heatmap. Elevation products also display a 3-D sampled surface.

The application caches downloaded files under `data/cache/lola`. The downloader checks the TIFF header, raster readability, projected CRS, metre units and an approximately 5 m pixel size. These checks are basic validation; they do not independently prove that the complete CRS definition matches NASA's MOON_ME / DE421 specification. After a successful download, the app displays the NASA source URL, file size, SHA-256 checksum, affine transform, CRS WKT and other raster metadata. Use **Download raster provenance JSON** to save this metadata record, or open the direct NASA GeoTIFF source link. A checksum identifies the downloaded bytes; it does not certify scientific correctness.

Statistics and previews use a bounded nearest-neighbour sample of at most 512 × 512 pixels. They are not calculations over every pixel in the original raster. NoData and non-finite sample values are excluded from the statistics. The terrain explorer also shows the sampled grid's projected coordinate-system name, effective pixel spacing, raster bounds and valid/missing pixel counts. These are map-grid descriptors, not a verification of the complete lunar reference frame.

## 4. Compare regions

1. Open **Compare regions**.
2. Select two different study regions.
3. Choose one LOLA product.
4. Select **Compare selected regions**.
5. Review the descriptive statistics table and choose a statistic for the bar chart.
6. Use **Download comparison CSV** to export the displayed comparison.

The comparison uses the same product type for both regions. It does not normalize different spatial footprints, assess landing hazards, calculate a weighted score, or rank sites. Missing-data patterns and raster characteristics can affect the results.

## 5. Sun & Earth geometry

1. Open **Sun & Earth geometry**.
2. Enter longitude in degrees, latitude in degrees, and altitude in kilometres above the reference ellipsoid used by Horizons for lunar geodetic coordinates. Positive longitude is east; negative longitude is west (for example, -90° is equivalent to 270° east). Altitude is not local terrain elevation.
3. Choose a UTC start date and a duration of one to three days.
4. Confirm the checkbox only after independently verifying the coordinate provenance and convention.
5. Select **Retrieve Sun and Earth ephemerides**.
6. Review the returned UTC timestamps, apparent azimuth and elevation, plot, and CSV export.

The observer coordinates are supplied by the user. MoonSight does not derive coordinates from a LOLA study-region name. Do not treat the displayed initial input values as the verified coordinates of a named region.

The client requests apparent azimuth/elevation (Horizons observer quantity 4) for the Sun and Earth. Positive elevation is a geometric direction indicator only. It does not account for nearby terrain obstruction. Earth elevation does not establish a radio link, and Sun elevation does not establish illumination duration or available electrical power.

## 6. Data & limitations

Open **Data & limitations** for the in-app source links, NASA study-region names, assumptions and scientific limitations.

Primary sources:

- NASA LOLA South Pole archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- NASA LOLA product page: https://pgda.gsfc.nasa.gov/products/78
- NASA/JPL Horizons API: https://ssd-api.jpl.nasa.gov/doc/horizons.html

## 7. Common issues

| Issue | What to check |
|---|---|
| Installation fails around Rasterio | Use a supported Python version and consult the Rasterio installation guidance for your operating system. |
| NASA download fails | Check the internet connection and whether the NASA archive is reachable. Retry later if the remote service is temporarily unavailable. |
| Download is rejected | The response may not be a TIFF, may exceed the configured size limit, may not open as a raster, or may fail the current CRS / units / pixel-size checks. |
| Horizons query fails | Check the internet connection, input ranges, selected dates and JPL Horizons service status. |
| No Horizons query starts | Confirm the observer-coordinate provenance checkbox after verifying the coordinates. |
| Values look unexpected | Check product units, NoData counts, sample dimensions, coordinate provenance and source metadata. Do not infer site suitability from a plot. |

## 8. Responsible interpretation

- Treat NASA archive files and JPL Horizons responses as source products; identify derived summaries as derived.
- Preserve source units, coordinate reference information and uncertainty descriptions.
- Do not describe RMS uncertainty as a confidence interval without a justified statistical model.
- Do not interpret a 3-D preview as a terrain hazard or landing-clearance model.
- Do not infer that a location is safe, optimal, or approved for landing.
- Do not equate geometric Earth visibility with communications feasibility.
- Do not equate geometric Sun elevation with illumination duration or solar-power availability.

## 9. Current verification status

GitHub Actions passed for the PR head commit `f317ccfba578fc1b847f224184ec4d89f068268b` before it was merged. CI installs the project in a clean Ubuntu/Python 3.11 environment, compiles the Python sources, runs Ruff, and executes pytest, including the Streamlit AppTest startup smoke test.

This confirms the automated software checks, not live scientific validation. Live NASA raster retrieval, exact MOON_ME / DE421 CRS verification, live JPL Horizons requests, independent ephemeris comparison, and full browser/mobile interaction still require separate testing. The presence of a feature in this guide describes the committed interface and code path; it is not proof that every live service has been successfully tested.
