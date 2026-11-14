"""MoonSight Streamlit entry point."""

import streamlit as st

from moonsight.terrain.preview import build_terrain_heatmap, load_terrain_preview

from moonsight.catalog import LOLA_STUDY_SITES
from moonsight.data.downloader import download_lola_geotiff
from moonsight.data.summary import summarize_lola_raster

st.set_page_config(
    page_title="MoonSight | Lunar Landing Site Navigator",
    page_icon="🌕",
    layout="wide",
)

st.title("🌕 MoonSight")
st.subheader("Lunar Landing Site Navigator")
st.caption("NASA Space Apps Challenge 2026 · #MoonSightExplorers")

st.info(
    "Research prototype under development. This application does not determine "
    "landing safety or certify mission suitability."
)

st.markdown(
    """
MoonSight helps users explore documented lunar south-pole study regions using
NASA terrain evidence and, in later phases, Sun/Earth viewing geometry.

The current workflow can retrieve a NASA LOLA GeoTIFF, inspect its metadata,
and calculate descriptive statistics from a bounded raster sample. It does not
yet calculate site suitability.
"""
)

left, middle, right = st.columns(3)
left.metric("Documented LOLA study regions", len(LOLA_STUDY_SITES))
middle.metric("Terrain products supported", "5")
right.metric("Validated site rankings", "0")

st.divider()
st.header("NASA LOLA terrain data")
st.write(
    "Choose a region and product. The first download may take time depending on "
    "the file size and network connection. Files are cached locally after validation."
)

site_options = {f"{site.site_id} — {site.name}": site.site_id for site in LOLA_STUDY_SITES}
selected_label = st.selectbox("Study region", list(site_options))
product_labels = {
    "Elevation (metres)": "elevation",
    "Slope (degrees)": "slope",
    "LOLA spot count": "spot_count",
    "Elevation uncertainty (metres)": "elevation_uncertainty",
    "Slope uncertainty (degrees)": "slope_uncertainty",
}
selected_product_label = st.selectbox("Terrain product", list(product_labels))

st.caption(
    "Downloads are limited to 512 MiB per file. A file is accepted only if it "
    "has a TIFF header and Rasterio confirms its CRS and approximately 5 m pixels."
)

if st.button("Download and inspect NASA data", type="primary"):
    with st.spinner("Retrieving and validating the NASA LOLA GeoTIFF..."):
        try:
            selected_site_id = site_options[selected_label]
            selected_product = product_labels[selected_product_label]
            metadata = download_lola_geotiff(selected_site_id, selected_product)
            sample_summary = summarize_lola_raster(metadata.path, selected_product)
            product_units = sample_summary.units
            preview = load_terrain_preview(metadata.path, units=product_units)
        except Exception as exc:
            st.error(f"Data retrieval or validation failed: {exc}")
        else:
            st.success("The GeoTIFF passed the current file and metadata checks.")
            st.subheader("Raster metadata")
            st.json(metadata.to_dict())
            st.subheader("Sampled pixel statistics")
            st.caption(
                "These statistics describe a bounded, nearest-neighbour sample "
                "of the raster—not every pixel in the complete study region."
            )
            st.json(sample_summary.to_dict())
            st.subheader("Sampled LOLA product heatmap")
            st.caption(
                f"Displaying {preview.sample_width} × {preview.sample_height} sampled pixels "
                f"from the source raster ({preview.source_width} × {preview.source_height}). "
                "Blank cells represent NoData or non-finite values. Coordinates are "
                "projected coordinates in metres, not latitude/longitude. The CRS shown in the metadata must be checked against NASA's stated lunar reference frame before interpreting these as verified lunar-grid coordinates."
            )
            figure = build_terrain_heatmap(
                preview,
                title=f"{selected_label} — {selected_product_label}",
                colorbar_title=product_units,
            )
            st.plotly_chart(figure, use_container_width=True)
            st.warning(
                "These are descriptive data checks, not a scientific quality "
                "assessment or a landing-safety conclusion."
            )

st.divider()
st.header("NASA LOLA study regions")
for site in LOLA_STUDY_SITES:
    with st.expander(f"{site.site_id} — {site.name}"):
        st.write(site.description)
        st.caption(f"Source: {site.source_url}")

st.divider()
st.header("Development roadmap")
st.markdown(
    """
- [x] Repository and Python package foundation
- [x] NASA LOLA product URL registry
- [x] Bounded GeoTIFF download and metadata validation workflow
- [x] Bounded raster sample statistics
- [ ] Run tests from the GitHub checkout and verify a real NASA download
- [ ] JPL Horizons request and response validation
- [ ] Sun/Earth geometry calculations
- [ ] Terrain-aware visibility analysis
- [ ] Evidence-based location comparison
- [ ] Scientific review and end-to-end testing
"""
)

st.caption(
    "MoonSight is an independent educational project. It is not a NASA product "
    "or endorsement and is not intended for operational mission planning."
)
