from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from moonsight.data.downloader import download_lola_geotiff


class FakeResponse:
    def __init__(self, payload: bytes):
        self.payload = payload
        self.headers = {
            "Content-Type": "image/tiff",
            "Content-Length": str(len(payload)),
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size: int):
        yield self.payload


def make_geotiff_bytes(path: Path) -> bytes:
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        width=4,
        height=3,
        count=1,
        dtype="float32",
        crs="EPSG:3031",
        transform=from_origin(100, 200, 5, 5),
    ) as dataset:
        dataset.write(np.arange(12, dtype="float32").reshape(3, 4), 1)
    return path.read_bytes()


def test_download_saves_validated_file_and_provenance(tmp_path, monkeypatch):
    fixture_path = tmp_path / "fixture.tif"
    payload = make_geotiff_bytes(fixture_path)

    def fake_get(url, *, stream, timeout):
        assert url.endswith(
            "/Site04/Site04_final_adj_5mpp_surf.tif"
        )
        assert stream is True
        return FakeResponse(payload)

    monkeypatch.setattr("moonsight.data.downloader.requests.get", fake_get)

    metadata = download_lola_geotiff(
        "Site04",
        "elevation",
        cache_dir=tmp_path / "cache",
    )

    cached = Path(metadata.path)
    assert cached.is_file()
    assert cached.name == "Site04_final_adj_5mpp_surf.tif"
    assert metadata.source_url.endswith(cached.name)
    assert metadata.file_size_bytes == len(payload)
    assert len(metadata.sha256) == 64
    assert metadata.width == 4
    assert metadata.height == 3
    assert metadata.crs_wkt
    assert metadata.local_file_modified_at_utc.endswith("+00:00")


def test_download_reuses_valid_cached_file_without_network(tmp_path, monkeypatch):
    fixture_path = tmp_path / "fixture.tif"
    payload = make_geotiff_bytes(fixture_path)
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    cached_path = cache_dir / "Site04_final_adj_5mpp_surf.tif"
    cached_path.write_bytes(payload)

    def unexpected_get(*args, **kwargs):
        raise AssertionError("A valid cached raster should not be downloaded again.")

    monkeypatch.setattr("moonsight.data.downloader.requests.get", unexpected_get)

    metadata = download_lola_geotiff(
        "Site04",
        "elevation",
        cache_dir=cache_dir,
    )

    assert Path(metadata.path) == cached_path
    assert metadata.sha256
    assert metadata.source_url.endswith(cached_path.name)
