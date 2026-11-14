"""Download and validate NASA LOLA GeoTIFF products.

Downloads are cached locally and checked before being accepted. The module does
not interpret the raster as a landing-safety certification.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import os
import tempfile
from typing import Any

import rasterio
import requests

from moonsight.data.lola import LolaProduct, build_lola_product_url

DEFAULT_MAX_DOWNLOAD_BYTES = 512 * 1024 * 1024
TIFF_HEADERS = (b"II*\x00", b"MM\x00*")


@dataclass(frozen=True, slots=True)
class RasterMetadata:
    """Small, serializable summary of a validated raster file."""

    path: str
    width: int
    height: int
    band_count: int
    crs: str
    pixel_width: float
    pixel_height: float
    bounds: tuple[float, float, float, float]
    data_type: str
    nodata: float | int | None

    def to_dict(self) -> dict[str, Any]:
        """Return metadata suitable for display or JSON serialization."""
        return asdict(self)


def _has_tiff_header(header: bytes) -> bool:
    """Return whether the first four bytes match classic TIFF byte order/magic."""
    return any(header.startswith(signature) for signature in TIFF_HEADERS)


def inspect_lola_geotiff(path: str | Path) -> RasterMetadata:
    """Open a raster with Rasterio and verify basic LOLA archive expectations."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    with file_path.open("rb") as stream:
        header = stream.read(4)
    if not _has_tiff_header(header):
        raise ValueError("Downloaded file does not have a valid TIFF header.")

    try:
        with rasterio.open(file_path) as dataset:
            if dataset.width <= 0 or dataset.height <= 0 or dataset.count < 1:
                raise ValueError("Raster has invalid dimensions or no data bands.")
            if dataset.crs is None:
                raise ValueError("Raster is missing its coordinate reference system.")

            pixel_width = abs(float(dataset.transform.a))
            pixel_height = abs(float(dataset.transform.e))
            if not (4.0 <= pixel_width <= 6.0 and 4.0 <= pixel_height <= 6.0):
                raise ValueError(
                    "Unexpected pixel size: expected approximately 5 metres per pixel; "
                    f"received {pixel_width:g} x {pixel_height:g}."
                )

            return RasterMetadata(
                path=str(file_path),
                width=dataset.width,
                height=dataset.height,
                band_count=dataset.count,
                crs=dataset.crs.to_string(),
                pixel_width=pixel_width,
                pixel_height=pixel_height,
                bounds=(
                    float(dataset.bounds.left),
                    float(dataset.bounds.bottom),
                    float(dataset.bounds.right),
                    float(dataset.bounds.top),
                ),
                data_type=dataset.dtypes[0],
                nodata=dataset.nodata,
            )
    except rasterio.errors.RasterioError as exc:
        raise ValueError(f"Rasterio could not open the downloaded GeoTIFF: {exc}") from exc


def download_lola_geotiff(
    site_id: str,
    product: LolaProduct,
    cache_dir: str | Path = "data/cache/lola",
    *,
    max_bytes: int = DEFAULT_MAX_DOWNLOAD_BYTES,
    timeout: tuple[float, float] = (15.0, 120.0),
) -> RasterMetadata:
    """Download one NASA LOLA GeoTIFF, validate it, and cache it atomically.

    Existing cached files are revalidated before reuse. A partial or invalid
    download is never left at the final cache path.
    """
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive.")

    url = build_lola_product_url(site_id, product)
    filename = url.rsplit("/", 1)[-1]
    destination_dir = Path(cache_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / filename

    if destination.exists():
        try:
            return inspect_lola_geotiff(destination)
        except (OSError, ValueError):
            destination.unlink(missing_ok=True)

    temporary_path: Path | None = None
    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "").lower()
            if "text/html" in content_type:
                raise ValueError("NASA returned an HTML page instead of a GeoTIFF.")

            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise ValueError(
                    f"File is larger than the configured {max_bytes:,}-byte download limit."
                )

            file_descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{filename}.", suffix=".part", dir=destination_dir
            )
            temporary_path = Path(temporary_name)
            bytes_written = 0
            first_chunk = True

            with os.fdopen(file_descriptor, "wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    if first_chunk:
                        if not _has_tiff_header(chunk[:4]):
                            raise ValueError(
                                "NASA response did not begin with a valid TIFF header."
                            )
                        first_chunk = False
                    bytes_written += len(chunk)
                    if bytes_written > max_bytes:
                        raise ValueError(
                            f"Download exceeded the configured {max_bytes:,}-byte limit."
                        )
                    output.write(chunk)

                output.flush()
                os.fsync(output.fileno())

        if bytes_written == 0:
            raise ValueError("NASA returned an empty file.")

        metadata = inspect_lola_geotiff(temporary_path)
        temporary_path.replace(destination)
        return RasterMetadata(
            path=str(destination),
            width=metadata.width,
            height=metadata.height,
            band_count=metadata.band_count,
            crs=metadata.crs,
            pixel_width=metadata.pixel_width,
            pixel_height=metadata.pixel_height,
            bounds=metadata.bounds,
            data_type=metadata.data_type,
            nodata=metadata.nodata,
        )
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
