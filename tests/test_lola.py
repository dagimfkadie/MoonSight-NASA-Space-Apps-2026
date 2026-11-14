from moonsight.data.lola import build_lola_product_url

import pytest


NASA_ARCHIVE = "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/"


def test_builds_documented_site01_elevation_url():
    assert build_lola_product_url("Site01", "elevation") == (
        f"{NASA_ARCHIVE}Site01/Site01_final_adj_5mpp_surf.tif"
    )


@pytest.mark.parametrize(
    ("product", "suffix"),
    [
        ("slope", "slp"),
        ("spot_count", "ldec"),
        ("elevation_uncertainty", "toterr"),
        ("slope_uncertainty", "slperr"),
    ],
)
def test_builds_documented_site04_product_urls(product, suffix):
    assert build_lola_product_url("Site04", product) == (
        f"{NASA_ARCHIVE}Site04/Site04_final_adj_5mpp_{suffix}.tif"
    )


def test_unknown_site_is_rejected():
    with pytest.raises(ValueError, match="Unknown LOLA study site"):
        build_lola_product_url("Site99", "elevation")


def test_unknown_product_is_rejected():
    with pytest.raises(ValueError, match="Unsupported LOLA product type"):
        build_lola_product_url("Site01", "made_up")
