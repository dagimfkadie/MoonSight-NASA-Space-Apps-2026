from moonsight.catalog import LOLA_STUDY_SITES, NASA_LOLA_SITES_URL, get_site


def test_catalog_contains_nasa_documented_site_ids():
    assert [site.site_id for site in LOLA_STUDY_SITES] == [
        "Site01",
        "Site04",
        "Site07",
        "Site11",
        "Site20",
        "Site23",
    ]


def test_site_lookup_returns_documented_name():
    assert get_site("Site04").name == "Shackleton rim"


def test_unknown_site_is_rejected():
    try:
        get_site("Site99")
    except ValueError as exc:
        assert "Unknown LOLA study site" in str(exc)
    else:
        raise AssertionError("Unknown site should raise ValueError")


def test_all_catalog_entries_point_to_nasa_source():
    assert all(site.source_url == NASA_LOLA_SITES_URL for site in LOLA_STUDY_SITES)
