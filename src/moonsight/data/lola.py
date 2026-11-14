"""URL registry for NASA's documented South Pole LOLA GeoTIFF products.

This module builds links only for known study sites and known product types.
It does not download files or treat a URL as proof that a product was retrieved.
"""

from typing import Literal
from urllib.parse import urljoin

from moonsight.catalog import get_site

LolaProduct = Literal[
    "elevation",
    "slope",
    "spot_count",
    "elevation_uncertainty",
    "slope_uncertainty",
]

_PRODUCT_SUFFIXES: dict[LolaProduct, str] = {
    "elevation": "surf",
    "slope": "slp",
    "spot_count": "ldec",
    "elevation_uncertainty": "toterr",
    "slope_uncertainty": "slperr",
}


def build_lola_product_url(site_id: str, product: LolaProduct) -> str:
    """Build the NASA archive URL for a known site's documented GeoTIFF product.

    Args:
        site_id: One of the study-region IDs in the NASA-backed site catalog.
        product: One of the supported LOLA GeoTIFF product types.

    Raises:
        ValueError: If the site ID or product type is not in the supported catalog.
    """
    site = get_site(site_id)
    try:
        suffix = _PRODUCT_SUFFIXES[product]
    except KeyError as exc:
        raise ValueError(f"Unsupported LOLA product type: {product}") from exc

    filename = f"{site.site_id}_final_adj_5mpp_{suffix}.tif"
    return urljoin(site.source_url, f"{site.site_id}/{filename}")
