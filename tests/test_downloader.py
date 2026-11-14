from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from moonsight.data.downloader import (
    _has_tiff_header,
    inspect_lola_geotiff,
)


@pytest.mark.parametrize("header", [bytes.fromhex("49492a00"), bytes.fromhex("4d4d002a")])
def test_accepts_classic_tiff_headers(header):
    assert _has_tiff_header(header)


@pytest.mark.parametrize("header", [b"", b"HTML", bytes.fromhex("504b0304"), bytes.fromhex("49492b00")])
def test_rejects_non_tiff_headers(header):
    assert not _has_tiff_header(header)


def test_inspector_rejects_html_error_page(tmp_path: Path):
    error_file = tmp_path / "not-a-raster.tif"
    error_file.write_text("<html>Not found</html>", encoding="utf-8")

    with pytest.raises(ValueError, match="valid TIFF header"):
        inspect_lola_geotiff(error_file)


def test_inspector_rejects_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        inspect_lola_geotiff(tmp_path / "missing.tif")


def test_inspector_reads_valid_five_metre_geotiff(tmp_path: Path):
    raster_path = tmp_path / "synthetic-test.tif"
    with rasterio.open(
        raster_path,
        "w",
        driver="GTiff",
        width=4,
        height=3,
        count=1,
        dtype="float32",
        crs="EPSG:3031",
        transform=from_origin(100.0, 200.0, 5.0, 5.0),
    ) as dataset:
        values = np.array(
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            dtype="float32",
        )
        dataset.write(values, 1)

    metadata = inspect_lola_geotiff(raster_path)

    assert metadata.width == 4
    assert metadata.height == 3
    assert metadata.band_count == 1
    assert metadata.pixel_width == 5.0
    assert metadata.pixel_height == 5.0
    assert metadata.crs == "EPSG:3031"
    assert metadata.data_type == "float32"


def test_inspector_rejects_geographic_coordinate_system(tmp_path: Path):
    raster_path = tmp_path / "geographic-test.tif"
    with rasterio.open(
        raster_path,
        "w",
        driver="GTiff",
        width=4,
        height=3,
        count=1,
        dtype="float32",
        crs="EPSG:4326",
        transform=from_origin(100.0, 200.0, 5.0, 5.0),
    ) as dataset:
        dataset.write(np.ones((3, 4), dtype="float32"), 1)

    with pytest.raises(ValueError, match="projected coordinate reference system"):
        inspect_lola_geotiff(raster_path)
