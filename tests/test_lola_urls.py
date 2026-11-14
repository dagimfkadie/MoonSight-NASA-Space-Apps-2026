import pytest

from moonsight.data.lola import build_lola_product_url


@pytest.mark.parametrize(
    ("product", "suffix"),
    [
        ("elevation", "surf"),
        ("slope", "slp"),
        ("spot_count", "ldec"),
        ("elevation_uncertainty", "toterr"),
        ("slope_uncertainty", "slperr"),
    ],
)
def test_builds_archive_url_for_each_supported_product(product, suffix):
    url = build_lola_product_url("Site04", product)
    assert url == (
        "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/"
        f"Site04/Site04_final_adj_5mpp_{suffix}.tif"
    )


def test_unknown_site_is_rejected():
    with pytest.raises(ValueError, match="Unknown LOLA study site"):
        build_lola_product_url("Site99", "elevation")


def test_unknown_product_is_rejected():
    with pytest.raises(ValueError, match="Unsupported LOLA product"):
        build_lola_product_url("Site04", "unknown")
