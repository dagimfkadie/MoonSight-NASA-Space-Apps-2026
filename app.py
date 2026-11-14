"""MoonSight Streamlit entry point.

This initial interface deliberately displays no fabricated measurements.
Scientific data workflows will be connected in later development phases.
"""

import streamlit as st

from moonsight.catalog import LOLA_STUDY_SITES

st.set_page_config(
    page_title="MoonSight | Lunar Landing Site Navigator",
    page_icon="🌕",
    layout="wide",
)

st.title("🌕 MoonSight")
st.subheader("Lunar Landing Site Navigator")
st.caption("NASA Space Apps Challenge 2026 · #MoonSightExplorers")

st.info(
    "Research prototype under development. No landing-safety determination is made "
    "by this application."
)

st.markdown(
    """
MoonSight is being developed to help users explore documented lunar south-pole
study regions using terrain evidence and Sun/Earth viewing geometry.

**The current build is the software foundation.** Live NASA data retrieval,
scientific calculations, and comparison results will appear only after they are
implemented and validated.
"""
)

left, middle, right = st.columns(3)
left.metric("Documented LOLA study regions", len(LOLA_STUDY_SITES))
middle.metric("Live data connections", "Not connected")
right.metric("Validated scientific outputs", "0")

st.divider()
st.header("Study regions listed in the NASA LOLA archive")

for site in LOLA_STUDY_SITES:
    with st.expander(f"{site.site_id} — {site.name}"):
        st.write(site.description)
        st.caption(f"Source: {site.source_url}")
        st.warning(
            "Region metadata only. Coordinates and measurements will be added "
            "after their reference definitions and source files are verified."
        )

st.divider()
st.header("Development roadmap")
st.markdown(
    """
- [x] Repository and Python package foundation
- [ ] NASA LOLA data retrieval and raster validation
- [ ] JPL Horizons request and response validation
- [ ] Sun/Earth geometry calculations
- [ ] Terrain-aware visibility analysis
- [ ] Evidence-based location comparison
- [ ] Automated tests and scientific review
"""
)

st.caption(
    "MoonSight is an independent educational project. It is not a NASA product "
    "or endorsement and is not intended for operational mission planning."
)
