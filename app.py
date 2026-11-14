"""MoonSight Streamlit entry point."""

import streamlit as st

from moonsight.catalog import LOLA_STUDY_SITES
from moonsight.data.downloader import download_lola_geotiff

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

The current data workflow can retrieve one NASA LOLA GeoTIFF and inspect its
metadata. It does not yet calculate site suitability.
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

if st.button("Download and validate NASA data", type="primary"):
    with st.spinner("Retrieving and validating the NASA LOLA GeoTIFF..."):
        try:
            metadata = download_lola_geotiff(
                site_options[selected_label],
                product_labels[selected_product_label],
            )
        except Exception as exc:
            st.error(f"Data retrieval or validation failed: {exc}")
        else:
            st.success("The GeoTIFF was downloaded and passed the current metadata checks.")
            st.subheader("Raster metadata")
            st.json(metadata.to_dict())
            st.warning(
                "Metadata validation is not a scientific quality assessment. "
                "No terrain interpretation or landing-safety conclusion is produced."
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
- [ ] Execute automated tests and verify a real NASA download
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
