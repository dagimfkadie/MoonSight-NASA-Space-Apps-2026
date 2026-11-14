from datetime import date

import pytest

from moonsight.astronomy.horizons import (
    fetch_lunar_observer_ephemeris,
    parse_observer_csv,
)


def test_parse_observer_csv_extracts_azimuth_and_elevation():
    text = """header
$$SOE
2026-Nov-14 00:00, , , 120.5, 15.25
2026-Nov-14 01:00, , , 130.0, -2.0
$$EOE
footer"""
    rows = parse_observer_csv(text)
    assert len(rows) == 2
    assert rows[0].azimuth_deg == 120.5
    assert rows[0].elevation_deg == 15.25
    assert rows[1].elevation_deg == -2.0


def test_parser_preserves_unavailable_angles_as_none():
    rows = parse_observer_csv("$$SOE\n2026-Nov-14 00:00, , , n.a., n.a.\n$$EOE")
    assert rows[0].azimuth_deg is None
    assert rows[0].elevation_deg is None


def test_parser_rejects_missing_delimiters():
    with pytest.raises(ValueError, match="delimiters"):
        parse_observer_csv("no ephemeris here")


def test_horizons_rejects_invalid_location_before_network():
    with pytest.raises(ValueError, match="Latitude"):
        fetch_lunar_observer_ephemeris(
            "Sun", 0, -91, 0, date(2026, 11, 14)
        )


def test_horizons_rejects_unknown_target():
    with pytest.raises(ValueError, match="Unsupported target"):
        fetch_lunar_observer_ephemeris(
            "Mars", 0, -89, 0, date(2026, 11, 14)
        )


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "signature": {"source": "NASA/JPL Horizons API", "version": "1.0"},
            "result": (
                "Ephemeris\n$$SOE\n"
                "2026-Nov-14 00:00, , , 25.0, 30.0\n"
                "$$EOE"
            )
        }


class FakeSession:
    def __init__(self):
        self.params = None

    def get(self, url, *, params, timeout):
        self.params = params
        return FakeResponse()


def test_horizons_request_uses_moon_surface_observer_and_correct_coordinate_order():
    session = FakeSession()
    rows = fetch_lunar_observer_ephemeris(
        "Earth", 12.5, -88.2, 0.15, date(2026, 11, 14), session=session
    )
    assert rows[0].azimuth_deg == 25.0
    assert session.params["CENTER"] == "coord@301"
    assert session.params["SITE_COORD"] == "12.50000000,-88.20000000,0.15000"
    assert session.params["QUANTITIES"] == "4"


def test_horizons_preserves_negative_longitude_as_west_longitude():
    session = FakeSession()
    fetch_lunar_observer_ephemeris(
        "Sun", -90.0, -89.0, 0.0, date(2026, 11, 14), session=session
    )
    assert session.params["SITE_COORD"] == "-90.00000000,-89.00000000,0.00000"
