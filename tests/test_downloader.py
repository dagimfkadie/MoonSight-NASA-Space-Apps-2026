from pathlib import Path

import pytest

from moonsight.data.downloader import (
    _has_tiff_header,
    inspect_lola_geotiff,
)


@pytest.mark.parametrize("header", [b"II*\x00", b"MM\x00*"])
def test_accepts_classic_tiff_headers(header):
    assert _has_tiff_header(header)


@pytest.mark.parametrize("header", [b"", b"HTML", b"PK\x03\x04", b"II+\x00"])
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
