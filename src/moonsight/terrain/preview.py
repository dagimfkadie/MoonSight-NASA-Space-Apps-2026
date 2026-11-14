"""Bounded LOLA raster previews for interactive terrain exploration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import Affine


@dataclass(frozen=True, slots=True)
class TerrainPreview:
    """A small raster preview with map coordinates at pixel centres."""

    x_metres: np.ndarray
    y_metres: np.ndarray
    elevation_or_product_values: np.ndarray
    valid_pixel_count: int
    nodata_pixel_count: int
    source_width: int
    source_height: int
    sample_width: int
    sample_height: int
    units: str


def load_terrain_preview(
    path: str | Path,
    *,
    units: str,
    max_dimension: int = 512,
) -> TerrainPreview:
    """Read a bounded nearest-neighbour sample from a single-band raster.

    Rotated or sheared rasters are rejected because this 2-D heatmap preview
    uses one-dimensional projected X and Y axes. NoData and non-finite values
    become NaN and are not displayed as measured terrain.
    """
    if max_dimension < 1:
        raise ValueError("max_dimension must be at least 1.")

    with rasterio.open(path) as dataset:
        if dataset.count != 1:
            raise ValueError("Terrain preview currently requires a single-band raster.")
        if dataset.crs is None or not dataset.crs.is_projected:
            raise ValueError("Terrain preview requires a projected coordinate system.")
        if abs(dataset.transform.b) > 1e-10 or abs(dataset.transform.d) > 1e-10:
            raise ValueError("Rotated or sheared rasters are not supported by this preview.")

        sample_width = min(dataset.width, max_dimension)
        sample_height = min(dataset.height, max_dimension)
        sampled = dataset.read(
            1,
            out_shape=(sample_height, sample_width),
            masked=True,
            resampling=Resampling.nearest,
        )
        values = np.asarray(sampled.filled(np.nan), dtype=np.float64)
        values[~np.isfinite(values)] = np.nan

        # Scale the affine transform to the sampled grid and use pixel centres.
        sample_transform: Affine = dataset.transform * Affine.scale(
            dataset.width / sample_width,
            dataset.height / sample_height,
        )
        x_metres = sample_transform.c + (
            np.arange(sample_width, dtype=np.float64) + 0.5
        ) * sample_transform.a
        y_metres = sample_transform.f + (
            np.arange(sample_height, dtype=np.float64) + 0.5
        ) * sample_transform.e

        valid_count = int(np.count_nonzero(np.isfinite(values)))
        nodata_count = int(values.size - valid_count)

        return TerrainPreview(
            x_metres=x_metres,
            y_metres=y_metres,
            elevation_or_product_values=values,
            valid_pixel_count=valid_count,
            nodata_pixel_count=nodata_count,
            source_width=dataset.width,
            source_height=dataset.height,
            sample_width=sample_width,
            sample_height=sample_height,
            units=units,
        )


def build_terrain_heatmap(
    preview: TerrainPreview,
    *,
    title: str,
    colorbar_title: str,
) -> go.Figure:
    """Create a 2-D sampled-data heatmap; blank cells remain visibly missing."""
    figure = go.Figure(
        data=go.Heatmap(
            x=preview.x_metres,
            y=preview.y_metres,
            z=preview.elevation_or_product_values,
            colorbar={"title": {"text": colorbar_title}},
            hovertemplate=(
                "X: %{x:.1f} m<br>Y: %{y:.1f} m<br>"
                "Value: %{z:.3f}<extra></extra>"
            ),
            connectgaps=False,
        )
    )
    figure.update_layout(
        title=title,
        xaxis_title="Projected X (m)",
        yaxis_title="Projected Y (m)",
        template="plotly_white",
        height=600,
    )
    figure.update_yaxes(scaleanchor="x", scaleratio=1)
    return figure
