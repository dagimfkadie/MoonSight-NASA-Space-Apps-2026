"""JPL Horizons observer ephemeris client for user-specified lunar surface coordinates."""

from __future__ import annotations

import csv
import io
import math
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

import requests

HORIZONS_API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
MOON_CENTER_ID = 301
TARGETS = {"Sun": "10", "Earth": "399"}


@dataclass(frozen=True, slots=True)
class ObserverPosition:
    """One apparent topocentric direction returned by JPL Horizons."""

    time_utc: str
    azimuth_deg: float | None
    elevation_deg: float | None


def _as_angle(value: str) -> float | None:
    cleaned = value.strip()
    if not cleaned or cleaned.lower() in {"n.a.", "na", "--"}:
        return None
    try:
        number = float(cleaned)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def parse_observer_csv(result_text: str) -> list[ObserverPosition]:
    """Parse Horizons CSV rows between its $$SOE and $$EOE delimiters.

    With QUANTITIES=4, the first three CSV columns are time and presence
    markers; apparent azimuth and elevation follow in columns 4 and 5.
    """
    if "$$SOE" not in result_text or "$$EOE" not in result_text:
        raise ValueError("Horizons response is missing ephemeris table delimiters.")
    table = result_text.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    positions: list[ObserverPosition] = []
    for row in csv.reader(io.StringIO(table)):
        if len(row) < 5:
            continue
        timestamp = row[0].strip()
        if not timestamp:
            continue
        positions.append(
            ObserverPosition(
                time_utc=timestamp,
                azimuth_deg=_as_angle(row[3]),
                elevation_deg=_as_angle(row[4]),
            )
        )
    if not positions:
        raise ValueError("Horizons returned no usable observer rows.")
    return positions


def fetch_lunar_observer_ephemeris(
    target: str,
    longitude_east_deg: float,
    latitude_deg: float,
    altitude_km: float,
    start_date: date,
    *,
    days: int = 1,
    timeout_seconds: float = 45.0,
    session: Any = requests,
) -> list[ObserverPosition]:
    """Retrieve apparent AZ/EL at a user-entered lunar geodetic location.

    SITE_COORD order follows Horizons' geodetic convention:
    east longitude (degrees), latitude (degrees), altitude (km).
    The coordinates are user inputs; this function does not assign them to
    any named LOLA study region.
    """
    if target not in TARGETS:
        raise ValueError(f"Unsupported target {target!r}; choose Sun or Earth.")
    if not -180.0 <= longitude_east_deg <= 180.0:
        raise ValueError("East longitude must be between -180 and 180 degrees.")
    if not -90.0 <= latitude_deg <= 90.0:
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not -20.0 <= altitude_km <= 100.0:
        raise ValueError("Altitude must be between -20 and 100 km.")
    if not 1 <= days <= 3:
        raise ValueError("Request duration must be between 1 and 3 days.")

    stop_date = start_date + timedelta(days=days)
    params = {
        "format": "json",
        "COMMAND": TARGETS[target],
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": f"coord@{MOON_CENTER_ID}",
        "COORD_TYPE": "GEODETIC",
        "SITE_COORD": (
            f"{longitude_east_deg:.8f},{latitude_deg:.8f},{altitude_km:.5f}"
        ),
        "START_TIME": start_date.isoformat(),
        "STOP_TIME": stop_date.isoformat(),
        "STEP_SIZE": "1h",
        "QUANTITIES": "4",
        "CSV_FORMAT": "YES",
        "APPARENT": "AIRLESS",
        "TIME_TYPE": "UT",
        "TIME_DIGITS": "MINUTES",
    }
    try:
        response = session.get(
            HORIZONS_API_URL, params=params, timeout=timeout_seconds
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not reach JPL Horizons: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("JPL Horizons returned invalid JSON.") from exc

    if not isinstance(payload, dict):
        raise TypeError("JPL Horizons returned an unexpected response structure.")
    if payload.get("error"):
        raise RuntimeError(f"JPL Horizons error: {payload['error']}")
    signature = payload.get("signature")
    if not isinstance(signature, dict) or not signature.get("version"):
        raise RuntimeError("JPL Horizons response is missing its API signature/version.")
    if signature.get("source") != "NASA/JPL Horizons API":
        raise RuntimeError("Response signature does not identify the NASA/JPL Horizons API.")
    result = payload.get("result")
    if not isinstance(result, str):
        raise TypeError("JPL Horizons response did not contain an ephemeris result.")
    return parse_observer_csv(result)
