from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from moonsight.data.summary import summarize_lola_raster


def create_test_raster(path: Path, values: np.ndarray, nodata: float = -9999.0):
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=values.shape[1],
        height=values.shape[0],
        count=1,
        dtype="float32",
        crs="EPSG:3031",
        transform=from_origin(0, 20, 5, 5),
        nodata=nodata,
    ) as dataset:
        dataset.write(values.astype("float32"), 1)


def test_summary_reports_sample_statistics_and_units(tmp_path: Path):
    path = tmp_path / "elevation.tif"
    values = np.array([[1, 2, 3], [4, -9999, 6]], dtype="float32")
    create_test_raster(path, values)

    result = summarize_lola_raster(path, "elevation", max_dimension=10)

    assert result.units == "metres"
    assert result.valid_sample_count == 5
    assert result.nodata_sample_count == 1
    assert result.minimum == 1.0
    assert result.maximum == 6.0
    assert result.median == 3.0
    assert result.sample_width == 3
    assert result.sample_height == 2
    assert "sample" in result.sampling


def test_summary_rejects_all_nodata_sample(tmp_path: Path):
    path = tmp_path / "empty.tif"
    values = np.full((2, 2), -9999.0, dtype="float32")
    create_test_raster(path, values)

    with pytest.raises(ValueError, match="no valid finite pixels"):
        summarize_lola_raster(path, "elevation")


def test_summary_rejects_invalid_sample_size(tmp_path: Path):
    path = tmp_path / "unused.tif"
    with pytest.raises(ValueError, match="at least 1"):
        summarize_lola_raster(path, "slope", max_dimension=0)
