from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from moonsight.terrain.preview import build_terrain_heatmap, load_terrain_preview


def write_raster(path: Path, values: np.ndarray, nodata: float = -9999.0):
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=values.shape[1],
        height=values.shape[0],
        count=1,
        dtype="float32",
        crs="EPSG:3031",
        transform=from_origin(100.0, 200.0, 5.0, 5.0),
        nodata=nodata,
    ) as dataset:
        dataset.write(values.astype("float32"), 1)


def test_preview_masks_nodata_and_uses_pixel_centres(tmp_path: Path):
    path = tmp_path / "terrain.tif"
    write_raster(path, np.array([[1, 2], [3, -9999]], dtype="float32"))

    preview = load_terrain_preview(path, units="metres")

    assert preview.valid_pixel_count == 3
    assert preview.nodata_pixel_count == 1
    assert preview.x_metres.tolist() == [102.5, 107.5]
    assert preview.y_metres.tolist() == [197.5, 192.5]
    assert np.isnan(preview.elevation_or_product_values[1, 1])


def test_preview_respects_maximum_dimension(tmp_path: Path):
    path = tmp_path / "large.tif"
    write_raster(path, np.arange(10000, dtype="float32").reshape(100, 100))

    preview = load_terrain_preview(path, units="metres", max_dimension=16)

    assert preview.sample_width == 16
    assert preview.sample_height == 16
    assert preview.source_width == 100
    assert preview.source_height == 100


def test_preview_rejects_invalid_sample_size(tmp_path: Path):
    with pytest.raises(ValueError, match="at least 1"):
        load_terrain_preview(tmp_path / "missing.tif", units="metres", max_dimension=0)


def test_heatmap_uses_projected_axes_and_title(tmp_path: Path):
    path = tmp_path / "terrain.tif"
    write_raster(path, np.array([[1, 2], [3, 4]], dtype="float32"))
    preview = load_terrain_preview(path, units="metres")

    figure = build_terrain_heatmap(
        preview,
        title="Sampled elevation",
        colorbar_title="Elevation (m)",
    )

    assert figure.layout.title.text == "Sampled elevation"
    assert list(figure.data[0].x) == [102.5, 107.5]
    assert list(figure.data[0].y) == [197.5, 192.5]
