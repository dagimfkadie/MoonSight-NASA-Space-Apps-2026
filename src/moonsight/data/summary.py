"""Small, reproducible summaries of downloaded LOLA raster samples.

Statistics are computed from a bounded, regularly decimated sample, not every
pixel in the source raster. They are descriptive checks, not landing criteria.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import rasterio
from rasterio.enums import Resampling

from moonsight.data.lola import LolaProduct

_SAMPLE_MAX_DIMENSION = 512


@dataclass(frozen=True, slots=True)
class RasterSampleSummary:
    """Descriptive statistics from a bounded raster sample."""

    product: str
    units: str
    sampling: str
    sample_width: int
    sample_height: int
    valid_sample_count: int
    nodata_sample_count: int
    minimum: float
    maximum: float
    mean: float
    median: float
    percentile_95: float

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary."""
        return asdict(self)


_PRODUCT_UNITS: dict[LolaProduct, str] = {
    "elevation": "metres",
    "slope": "degrees",
    "spot_count": "LOLA returns per pixel",
    "elevation_uncertainty": "metres RMS error",
    "slope_uncertainty": "degrees RMS error",
}


def summarize_lola_raster(
    path: str | Path,
    product: LolaProduct,
    *,
    max_dimension: int = _SAMPLE_MAX_DIMENSION,
) -> RasterSampleSummary:
    """Summarize a bounded nearest-neighbour sample of a LOLA raster band.

    The source file is not modified. NoData cells and non-finite values are
    excluded from statistics. The output explicitly identifies itself as a
    sample so it cannot be mistaken for full-raster statistics.
    """
    if max_dimension < 1:
        raise ValueError("max_dimension must be at least 1.")

    with rasterio.open(path) as dataset:
        if dataset.count < 1:
            raise ValueError("Raster has no data bands.")

        sample_width = min(dataset.width, max_dimension)
        sample_height = min(dataset.height, max_dimension)
        sample = dataset.read(
            1,
            out_shape=(sample_height, sample_width),
            masked=True,
            resampling=Resampling.nearest,
        )

    values = np.asarray(sample.compressed(), dtype=np.float64)
    finite_values = values[np.isfinite(values)]
    total_sample_count = sample_width * sample_height
    valid_count = int(finite_values.size)
    nodata_count = total_sample_count - valid_count

    if valid_count == 0:
        raise ValueError("The sampled raster contains no valid finite pixels.")

    return RasterSampleSummary(
        product=product,
        units=_PRODUCT_UNITS[product],
        sampling=(
            f"nearest-neighbour sample decimated to at most "
            f"{max_dimension} x {max_dimension} pixels"
        ),
        sample_width=sample_width,
        sample_height=sample_height,
        valid_sample_count=valid_count,
        nodata_sample_count=nodata_count,
        minimum=float(np.min(finite_values)),
        maximum=float(np.max(finite_values)),
        mean=float(np.mean(finite_values)),
        median=float(np.median(finite_values)),
        percentile_95=float(np.percentile(finite_values, 95)),
    )
