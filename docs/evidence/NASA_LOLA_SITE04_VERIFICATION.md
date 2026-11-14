# NASA LOLA Site04 live retrieval evidence

**Project:** MoonSight — Lunar Landing Site Navigator  
**Evidence date:** 2026-11-14  
**Workflow run:** https://github.com/dagimfkadie/MoonSight-NASA-Space-Apps-2026/actions/runs/43591846379  
**Artifact:** nasa-lola-site04-verification (ID 14113230067; expires 2026-11-28 11:50:06 UTC)

## Source

https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/Site04/Site04_final_adj_5mpp_surf.tif

## Observed results

- Download status: success
- File name: Site04_final_adj_5mpp_surf.tif
- File size: 40,980,806 bytes
- SHA-256: 38ff70dbdf2f066c2cfa94a646c3a59d653ce7f6b4528b15fc1b43ee397ce758
- Raster dimensions: 3,200 × 3,200 pixels
- Bands: 1
- Data type: Float32
- NoData: NaN
- Pixel spacing: 5 m × 5 m
- Bounds: X = -9,000 to 7,000 m; Y = -15,000 to 1,000 m
- Rasterio opened the downloaded file successfully.
- Reported CRS: unnamed polar stereographic; WKT includes a 1,737,400 m sphere and latitude of origin -90°.

## What this proves

A real file was downloaded from the NASA LOLA archive and successfully opened and inspected with Rasterio in a GitHub Actions runner. The workflow uploaded the TIFF and JSON metadata report as an artifact.

## What this does not prove

- Exact MOON_ME / DE421 reference-frame equivalence; the CRS is reported as unnamed.
- Product-specific scientific validation beyond the recorded raster metadata.
- Integration of this exact downloaded file into the Streamlit app or a successful interactive app session.
- Successful live JPL Horizons queries or independent ephemeris agreement.
- Landing safety, terrain-aware visibility, communications availability, or mission readiness.

Preserve the temporary workflow artifact before its expiration if long-term evidence is required.
