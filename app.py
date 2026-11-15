"""MoonSight Streamlit application: terrain evidence and lunar geometry."""

import json
from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import rasterio
import requests
import streamlit as st
from affine import Affine
from rasterio.io import MemoryFile

from moonsight.astronomy.horizons import fetch_lunar_observer_ephemeris
from moonsight.catalog import LOLA_STUDY_SITES
from moonsight.data.downloader import download_lola_geotiff
from moonsight.data.summary import summarize_lola_raster
from moonsight.terrain.preview import (
    build_terrain_heatmap,
    build_terrain_surface,
    load_terrain_preview,
)

st.set_page_config(
    page_title="MoonSight | Lunar Landing Site Navigator",
    page_icon="🌕",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
      --moon-bg: #080d1b;
      --moon-panel: rgba(19, 29, 53, .82);
      --moon-border: rgba(154, 178, 226, .18);
      --moon-cyan: #72e4f2;
      --moon-violet: #a99bff;
    }
    .stApp {
      background:
        radial-gradient(ellipse at 12% 0%, rgba(66, 91, 161, .24), transparent 34%),
        radial-gradient(ellipse at 92% 10%, rgba(91, 67, 150, .18), transparent 30%),
        linear-gradient(145deg, #080d1b 0%, #101a31 48%, #0b1020 100%);
      color: #edf3ff;
      font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3, [data-testid="stHeading"] {
      font-family: 'Space Grotesk', sans-serif !important;
      letter-spacing: -.035em;
      color: #f4f7ff;
    }
    h1 { font-size: clamp(2.3rem, 5vw, 3.8rem) !important; }
    h2 { color: #dce8ff !important; }
    [data-testid="stHeader"] { background: rgba(8, 13, 27, .72); }
    [data-testid="stTabs"] [role="tablist"] {
      gap: .45rem;
      border-bottom: 1px solid var(--moon-border);
    }
    [data-testid="stTabs"] button[role="tab"] {
      border-radius: 12px 12px 0 0;
      padding: .8rem 1rem;
      color: #b9c8e7;
      font-weight: 650;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
      color: var(--moon-cyan) !important;
      border-bottom: 3px solid var(--moon-cyan) !important;
      background: rgba(114, 228, 242, .08);
    }
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stExpander"],
    [data-testid="stMetric"] {
      border: 1px solid var(--moon-border);
      border-radius: 18px;
      background: var(--moon-panel);
      box-shadow: 0 12px 36px rgba(0,0,0,.16);
    }
    [data-testid="stMetric"] { padding: 1rem; }
    [data-testid="stMetricLabel"] { color: #aebfe0 !important; }
    [data-testid="stMetricValue"] { color: #f3f7ff !important; }
    .stButton > button, .stDownloadButton > button {
      border: 1px solid rgba(114, 228, 242, .45);
      border-radius: 12px;
      background: linear-gradient(110deg, #176d86, #514a9b);
      color: white;
      font-weight: 700;
      padding: .65rem 1.15rem;
      transition: transform .18s ease, box-shadow .18s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(66, 197, 222, .2);
      border-color: var(--moon-cyan);
      color: white;
    }
    [data-baseweb="select"] > div, [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div {
      background: rgba(17, 27, 49, .9);
      border-color: var(--moon-border);
      border-radius: 11px;
    }
    [data-testid="stAlert"] { border-radius: 14px; }
    [data-testid="stPlotlyChart"] {
      border: 1px solid var(--moon-border);
      border-radius: 18px;
      overflow: hidden;
      background: rgba(14, 23, 43, .7);
      padding: .25rem;
    }
    [data-testid="stCaptionContainer"] { color: #aebbd4; }
    a { color: #7de5f2 !important; }
    hr { border-color: var(--moon-border); }
    @media (max-width: 700px) {
      [data-testid="stTabs"] button[role="tab"] { padding: .55rem .45rem; font-size: .78rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PRODUCTS = {
    "Elevation (metres)": ("elevation", "metres"),
    "Slope (degrees)": ("slope", "degrees"),
    "LOLA spot count": ("spot_count", "LOLA returns per pixel"),
    "Elevation uncertainty (metres)": ("elevation_uncertainty", "metres RMS error"),
    "Slope uncertainty (degrees)": ("slope_uncertainty", "degrees RMS error"),
}

NASA_GLOBAL_DEM_URL = (
    "https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/ldem_4.tif"
)
MOON_REFERENCE_RADIUS_KM = 1737.4


@st.cache_data(ttl=86400, show_spinner=False)
def load_global_lunar_dem():
    """Load NASA's low-resolution global LOLA elevation grid for globe viewing."""
    response = requests.get(NASA_GLOBAL_DEM_URL, timeout=(15, 90))
    response.raise_for_status()
    with MemoryFile(response.content) as memory_file:
        with memory_file.open() as dataset:
            if dataset.count < 1:
                raise ValueError("NASA global lunar DEM contains no raster band.")
            width = min(360, dataset.width)
            height = min(180, dataset.height)
            sample = dataset.read(
                1, out_shape=(height, width), masked=True
            )
            elevation_km = np.asarray(sample.filled(np.nan), dtype=np.float64)
            transform = dataset.transform * Affine.scale(
                dataset.width / width, dataset.height / height
            )
            longitude = transform.c + (
                np.arange(width, dtype=np.float64) + 0.5
            ) * transform.a
            latitude = transform.f + (
                np.arange(height, dtype=np.float64) + 0.5
            ) * transform.e
    elevation_km[~np.isfinite(elevation_km)] = np.nan
    return longitude, latitude, elevation_km

st.title("🌕 MoonSight")
st.subheader("Lunar Landing Site Navigator")
st.caption("NASA Space Apps Challenge 2026 · #MoonSightExplorers")
st.warning(
    "Educational research prototype only. It does not certify landing safety, "
    "mission feasibility, terrain clearance, or operational communications."
)

st.markdown(
    """
Explore NASA's documented lunar south-pole LOLA products, inspect sampled terrain,
compare descriptive raster statistics, and request apparent Sun/Earth directions
from JPL Horizons for coordinates that you explicitly enter.
"""
)

globe_tab, terrain_tab, compare_tab, geometry_tab, sources_tab = st.tabs(
    [
        "🌕 3D lunar globe",
        "Terrain explorer",
        "Compare regions",
        "Sun & Earth geometry",
        "Data & limitations",
    ]
)

site_options = {f"{site.site_id} — {site.name}": site.site_id for site in LOLA_STUDY_SITES}

with globe_tab:
    st.header("Interactive global Moon — LOLA topography")
    st.write(
        "Rotate, zoom and inspect a three-dimensional model of the whole Moon. "
        "This global view provides geographic context; use the Terrain explorer "
        "for the much finer south-polar study tiles."
    )
    globe_col1, globe_col2 = st.columns([1, 2])
    with globe_col1:
        vertical_exaggeration = st.slider(
            "Terrain vertical exaggeration",
            min_value=1.0,
            max_value=8.0,
            value=2.0,
            step=0.5,
            help="Visual aid only. The default 1× uses the source elevation scale.",
        )
        globe_colors = st.selectbox(
            "Elevation colour palette",
            ["Earth", "Viridis", "Cividis", "Turbo", "Plasma"],
            index=0,
        )
        st.caption(
            "Global context grid: NASA LOLA 4 pixels per degree. This is a "
            "coarse global model, not the 5 m/pixel south-pole products."
        )
        st.markdown(
            "[NASA CGI Moon Kit — source data and credits]"
            "(https://svs.gsfc.nasa.gov/4720/)"
        )
        st.markdown(
            "[Open NASA Moon Trek for detailed map layers]"
            "(https://trek.nasa.gov/moon/)"
        )
    try:
        with st.spinner("Loading NASA's global LOLA elevation map..."):
            longitude, latitude, elevation_km = load_global_lunar_dem()
    except (requests.RequestException, rasterio.errors.RasterioError, ValueError) as exc:
        st.error(f"The global lunar DEM could not be loaded: {exc}")
        st.info(
            "You can still use the Terrain explorer to download the individual "
            "NASA south-pole LOLA GeoTIFF products."
        )
    else:
        lon_grid, lat_grid = np.meshgrid(longitude, latitude)
        radius_km = MOON_REFERENCE_RADIUS_KM + (
            elevation_km * vertical_exaggeration
        )
        lat_rad = np.radians(lat_grid)
        lon_rad = np.radians(lon_grid)
        x_globe = radius_km * np.cos(lat_rad) * np.cos(lon_rad)
        y_globe = radius_km * np.cos(lat_rad) * np.sin(lon_rad)
        z_globe = radius_km * np.sin(lat_rad)
        color_scales = {
            "Earth": [
                [0.0, "#243b6b"],
                [0.25, "#657b8e"],
                [0.5, "#a99c83"],
                [0.75, "#d4c9ad"],
                [1.0, "#f4eee0"],
            ],
            "Viridis": "Viridis",
            "Cividis": "Cividis",
            "Turbo": "Turbo",
            "Plasma": "Plasma",
        }
        globe = go.Figure(
            data=[
                go.Surface(
                    x=x_globe,
                    y=y_globe,
                    z=z_globe,
                    surfacecolor=elevation_km,
                    colorscale=color_scales[globe_colors],
                    colorbar={"title": "Elevation (km)"},
                    connectgaps=False,
                    lighting={
                        "ambient": 0.45,
                        "diffuse": 0.75,
                        "specular": 0.15,
                        "roughness": 0.85,
                        "fresnel": 0.1,
                    },
                    lightposition={"x": 1000, "y": 1500, "z": 2000},
                    hovertemplate=(
                        "Longitude: %{customdata[0]:.1f}°<br>"
                        "Latitude: %{customdata[1]:.1f}°<br>"
                        "Elevation: %{customdata[2]:.2f} km"
                        "<extra>NASA LOLA</extra>"
                    ),
                    customdata=np.dstack((lon_grid, lat_grid, elevation_km)),
                )
            ]
        )
        globe.update_layout(
            height=680,
            margin={"l": 0, "r": 0, "t": 35, "b": 0},
            title="Moon — global LOLA elevation model",
            scene={
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "zaxis": {"visible": False},
                "aspectmode": "data",
                "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.1}},
            },
        )
        st.plotly_chart(
            globe,
            use_container_width=True,
            key="global_lunar_globe",
            config={"scrollZoom": True, "displaylogo": False},
        )
        st.caption(
            f"Displayed grid: {len(latitude)} latitude rows × "
            f"{len(longitude)} longitude columns. Elevation source values are "
            "kilometres relative to NASA's 1,737.4 km reference sphere. "
            "Vertical exaggeration changes the displayed shape only."
        )
        st.info(
            "This is a global-scale context globe, not a 5 m/pixel terrain model. "
            "The named Site01–Site23 study-region products are not pinned to this "
            "globe because their exact coordinates have not been verified in the "
            "project catalog. No landing-safety judgement is made."
        )

with terrain_tab:
    st.header("NASA LOLA terrain explorer")
    col1, col2 = st.columns(2)
    with col1:
        selected_site_label = st.selectbox("Study region", list(site_options))
    with col2:
        selected_product_label = st.selectbox("LOLA product", list(PRODUCTS))
    control1, control2, control3 = st.columns(3)
    with control1:
        color_scale = st.selectbox(
            "Heatmap colour scale",
            ["Viridis", "Cividis", "Plasma", "Inferno", "Turbo"],
            help="Choose how raster values are represented by colour.",
        )
    with control2:
        preview_resolution = st.slider(
            "Preview resolution (maximum dimension)",
            min_value=128,
            max_value=512,
            value=384,
            step=64,
            help="Higher values show more sampled pixels but may take longer to render.",
        )
    with control3:
        show_3d_surface = st.checkbox(
            "Show 3D elevation surface",
            value=True,
            help="Available for elevation products only.",
        )
    st.caption(
        "NASA lists these products as 5 m/pixel south-polar stereographic GeoTIFFs "
        "in the MOON_ME reference frame tied to DE421. MoonSight still checks the "
        "actual file metadata; a generic projected-metre check alone is not proof "
        "that a downloaded file matches that complete reference definition."
    )
    if st.button("Download and inspect NASA LOLA product", type="primary"):
        site_id = site_options[selected_site_label]
        product, units = PRODUCTS[selected_product_label]
        with st.spinner("Downloading and validating the selected NASA raster..."):
            try:
                metadata = download_lola_geotiff(site_id, product)
                summary = summarize_lola_raster(metadata.path, product)
                preview = load_terrain_preview(
                    metadata.path, units=units, max_dimension=preview_resolution
                )
            except (OSError, ValueError, requests.RequestException, rasterio.errors.RasterioError) as exc:
                st.error(f"Download or raster processing failed: {exc}")
            else:
                st.success("The file passed MoonSight's current TIFF, projected-metre and approximate pixel-size checks.")
                st.markdown(f"[Open the original GeoTIFF at NASA]({metadata.source_url})")
                st.subheader("Raster metadata and provenance")
                st.caption(
                    "The checksum and source URL identify this local file. The CRS WKT is "
                    "provided for inspection; exact MOON_ME / DE421 equivalence is not yet "
                    "automatically certified by the downloader."
                )
                st.json(metadata.to_dict())
                st.download_button(
                    "Download raster provenance JSON",
                    data=json.dumps(metadata.to_dict(), indent=2),
                    file_name=f"{site_id}_{product}_provenance.json",
                    mime="application/json",
                )
                st.subheader("Sample statistics")
                st.caption(
                    "Nearest-neighbour sample only (maximum 512 × 512 pixels), "
                    "not a full-resolution statistical analysis."
                )
                st.json(summary.to_dict())
                st.subheader("Sampled map grid")
                st.caption(
                    "Coordinates are projected map coordinates at sampled pixel centres. "
                    "The displayed grid is downsampled; its spacing is larger than the "
                    "source raster's nominal 5 m pixels when the source exceeds 512 pixels."
                )
                st.json(
                    {
                        "coordinate_reference_name": preview.crs_name,
                        "sample_width_pixels": preview.sample_width,
                        "sample_height_pixels": preview.sample_height,
                        "sample_pixel_width_metres": preview.sample_pixel_width_m,
                        "sample_pixel_height_metres": preview.sample_pixel_height_m,
                        "raster_bounds_metres_left_bottom_right_top": preview.bounds_m,
                        "valid_sample_pixels": preview.valid_pixel_count,
                        "missing_sample_pixels": preview.nodata_pixel_count,
                    }
                )
                st.subheader("2D product heatmap")
                heatmap = build_terrain_heatmap(
                    preview,
                    title=f"{selected_site_label} — {selected_product_label}",
                    colorbar_title=units,
                )
                heatmap.update_traces(colorscale=color_scale)
                st.plotly_chart(
                    heatmap,
                    use_container_width=True,
                    key="terrain_heatmap",
                )
                if product == "elevation" and show_3d_surface:
                    st.subheader("3D sampled elevation surface")
                    surface = build_terrain_surface(
                        preview, title=f"{selected_site_label} — sampled elevation"
                    )
                    st.plotly_chart(
                        surface,
                        use_container_width=True,
                        key="terrain_surface",
                    )
                st.info(
                    "The 3D surface is a downsampled visualization. Vertical exaggeration "
                    "and viewing perspective can affect visual impression; it is not a "
                    "landing-hazard assessment."
                )

with compare_tab:
    st.header("Descriptive comparison of LOLA study regions")
    st.write(
        "Compare sample statistics for the same NASA product across two study regions. "
        "This is a data exploration aid, not a site ranking."
    )
    c1, c2 = st.columns(2)
    labels = list(site_options)
    with c1:
        first_label = st.selectbox("First region", labels, index=0, key="compare_first")
    with c2:
        second_label = st.selectbox(
            "Second region", labels, index=1, key="compare_second"
        )
    compare_product_label = st.selectbox(
        "Product to compare", list(PRODUCTS), key="compare_product"
    )
    metric = st.selectbox(
        "Chart statistic",
        ["Mean", "Median", "95th percentile", "Minimum", "Maximum"],
        key="compare_metric",
    )
    if st.button("Compare selected regions"):
        product, units = PRODUCTS[compare_product_label]
        if first_label == second_label:
            st.error("Choose two different study regions.")
        else:
            records = []
            comparison_previews = []
            try:
                with st.spinner("Retrieving both NASA products and preparing map previews..."):
                    for label in (first_label, second_label):
                        site_id = site_options[label]
                        metadata = download_lola_geotiff(site_id, product)
                        summary = summarize_lola_raster(metadata.path, product)
                        preview = load_terrain_preview(
                            metadata.path, units=units, max_dimension=384
                        )
                        comparison_previews.append((label, preview))
                        records.append(
                            {
                                "Region": label,
                                "Minimum": summary.minimum,
                                "Mean": summary.mean,
                                "Median": summary.median,
                                "95th percentile": summary.percentile_95,
                                "Maximum": summary.maximum,
                                "Valid sampled pixels": summary.valid_sample_count,
                                "NoData / non-finite sampled pixels": summary.nodata_sample_count,
                            }
                        )
            except (
                OSError,
                RuntimeError,
                ValueError,
                requests.RequestException,
                rasterio.errors.RasterioError,
            ) as exc:
                st.error(f"Comparison could not be completed: {exc}")
            else:
                frame = pd.DataFrame(records)
                st.subheader("Visual map comparison")
                st.caption(
                    "These are sampled 2D maps of the selected NASA raster product. "
                    "Hover over either map to inspect projected coordinates and values."
                )
                map_col1, map_col2 = st.columns(2)
                for map_col, (region_label, preview) in zip(
                    (map_col1, map_col2), comparison_previews
                ):
                    with map_col:
                        st.markdown(f"**{region_label}**")
                        map_figure = build_terrain_heatmap(
                            preview,
                            title=f"{region_label} — {compare_product_label}",
                            colorbar_title=units,
                        )
                        map_figure.update_layout(
                            height=430,
                            margin={"l": 10, "r": 10, "t": 55, "b": 10},
                            template="plotly_dark",
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(8,13,27,0.35)",
                            font={"color": "#eaf1ff"},
                        )
                        st.plotly_chart(
                            map_figure,
                            use_container_width=True,
                            key=f"compare_map_{site_options[region_label]}",
                        )
                        st.caption(
                            f"{preview.sample_width} × {preview.sample_height} sampled pixels · "
                            f"{preview.valid_pixel_count:,} valid values · {preview.crs_name}"
                        )
                st.subheader("Numerical comparison")
                st.dataframe(frame, use_container_width=True, hide_index=True)
                fig = px.bar(
                    frame,
                    x="Region",
                    y=metric,
                    title=f"{metric} of sampled {compare_product_label} ({units})",
                )
                st.plotly_chart(fig, use_container_width=True)
                st.caption(
                    "Sampling is bounded and nearest-neighbour. Different raster "
                    "footprints, missing-data patterns and interpolation characteristics "
                    "can affect these descriptive comparisons."
                )
                st.download_button(
                    "Download comparison CSV",
                    data=frame.to_csv(index=False).encode("utf-8"),
                    file_name="moonsight_lola_sample_comparison.csv",
                    mime="text/csv",
                )

with geometry_tab:
    st.header("JPL Horizons: apparent Sun and Earth directions")
    st.write(
        "Enter a lunar surface observer location. These coordinates are independent "
        "inputs; MoonSight does not assume that a named LOLA tile has these coordinates."
    )
    st.warning(
        "Horizons observer coordinates use east longitude (degrees), latitude "
        "(degrees), and altitude (kilometres) above the reference ellipsoid used "
        "for the Moon's geodetic coordinates. Positive longitude is east; negative "
        "longitude is west (for example, -90° is equivalent to 270° east). This is "
        "not local terrain elevation. Enter coordinates whose lunar geodetic "
        "definition you can document. Do not treat a zero or default coordinate "
        "as the location of a named landing-site study region."
    )
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        longitude = st.number_input(
            "East longitude (°)", min_value=-180.0, max_value=180.0, value=0.0
        )
    with g2:
        latitude = st.number_input(
            "Latitude (°)", min_value=-90.0, max_value=90.0, value=-89.0
        )
    with g3:
        altitude = st.number_input(
            "Altitude above reference ellipsoid (km)", min_value=-20.0, max_value=100.0, value=0.0
        )
    with g4:
        observation_date = st.date_input("Start date (UTC)", value=date.today())
    duration_days = st.selectbox("Duration", [1, 2, 3], index=0)
    coordinates_confirmed = st.checkbox(
        "I have independently verified these lunar geodetic coordinates and their source."
    )
    if st.button("Retrieve Sun and Earth ephemerides", type="primary"):
        if not coordinates_confirmed:
            st.error("Confirm the provenance of the lunar observer coordinates before querying Horizons.")
            st.stop()
        output = []
        try:
            with st.spinner("Querying NASA/JPL Horizons..."):
                for target in ("Sun", "Earth"):
                    positions = fetch_lunar_observer_ephemeris(
                        target,
                        longitude,
                        latitude,
                        altitude,
                        observation_date,
                        days=duration_days,
                    )
                    for position in positions:
                        output.append(
                            {
                                "Target": target,
                                "UTC": position.time_utc,
                                "Azimuth (°)": position.azimuth_deg,
                                "Elevation (°)": position.elevation_deg,
                            }
                        )
        except (RuntimeError, TypeError, ValueError) as exc:
            st.error(f"Horizons query failed: {exc}")
        else:
            ephemeris = pd.DataFrame(output)
            st.success(f"Retrieved {len(ephemeris)} observer records from Horizons.")
            st.dataframe(ephemeris, use_container_width=True, hide_index=True)
            fig = px.line(
                ephemeris,
                x="UTC",
                y="Elevation (°)",
                color="Target",
                markers=True,
                title="Apparent target elevation above the local geometric horizon",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.download_button(
                "Download ephemeris CSV",
                data=ephemeris.to_csv(index=False).encode("utf-8"),
                file_name="moonsight_horizons_ephemeris.csv",
                mime="text/csv",
            )
            st.info(
                "Positive elevation is a geometric direction indicator only. "
                "It does not account for nearby terrain blockage, antenna design, "
                "radio link budget, or verified communication availability."
            )

with sources_tab:
    st.header("Sources, assumptions and limitations")
    st.markdown(
        """
**NASA LOLA South Pole Landing Site DEM archive**

https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

The archive documents elevation, slope, LOLA return-count, elevation-uncertainty,
and slope-uncertainty products. It states 5 m/pixel, south-polar stereographic
X/Y coordinates in metres, MOON_ME reference frame, DE421 ephemeris.

**NASA/JPL Horizons API**

https://ssd-api.jpl.nasa.gov/doc/horizons.html

MoonSight requests observer-table quantity 4 (apparent azimuth and elevation)
for the Sun and Earth, with an explicitly entered lunar geodetic observer
coordinate and airless settings.

**Scientific limitations**

- A LOLA raster's slope layer is a terrain descriptor, not a complete landing hazard model.
- Elevation and slope uncertainty are reported as source RMS quantities; they are not automatically confidence intervals.
- Horizons geometric elevation does not include local terrain obstruction.
- Earth visibility is not a radio link budget or proof of communications.
- Solar elevation is not surface illumination duration or available solar electrical power.
- No site is declared safe, optimal, or approved for landing.
"""
    )
    st.subheader("NASA study regions")
    for site in LOLA_STUDY_SITES:
        st.write(f"**{site.site_id} — {site.name}.** {site.description}")
        st.caption(site.source_url)

st.divider()
st.caption(
    "MoonSight is an independent educational prototype. It is not a NASA product, "
    "is not endorsed by NASA, and is not intended for operational mission planning."
)
