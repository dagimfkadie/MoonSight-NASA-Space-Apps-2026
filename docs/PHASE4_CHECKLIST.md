# Phase 4 — Scientific calculation engine

## Implemented

- [x] JPL Horizons API client for observer-table queries.
- [x] User-entered lunar geodetic observer coordinates; no invented coordinates are assigned to LOLA tiles.
- [x] Sun (target 10) and Earth (target 399) request support.
- [x] Apparent azimuth/elevation quantity 4, airless setting, UTC time.
- [x] CSV ephemeris parsing with missing-angle handling.
- [x] Validate the JPL Horizons JSON signature/version before accepting a result.
- [x] Input validation for longitude, latitude, altitude, target and request duration.
- [x] Network/API error handling.
- [x] Unit tests using synthetic response fixtures and a fake HTTP session.

## Formula and interpretation

Horizons supplies apparent topocentric azimuth and elevation. MoonSight does not derive these angles from an unverified simplified orbital model. Azimuth is clockwise from north; elevation is relative to the local plane perpendicular to zenith.

For the Sun, elevation above zero is only a geometric direction indicator. It is not a terrain-aware illumination-duration calculation or solar-power estimate.

For Earth, elevation above zero is only a geometric visibility indicator. It does not prove an unobstructed terrain path or radio communication.

## Coordinate inputs

Horizons geodetic SITE_COORD order is east longitude (degrees), latitude (degrees), altitude (kilometres). The observer is sent as `coord@301`, a topocentric site on the Moon. Users must provide a documented lunar surface coordinate. A named LOLA study-region ID is not automatically converted into latitude/longitude.

## Independent documentation check

The current JPL Horizons API reference confirms that `CENTER`, `COORD_TYPE`, `SITE_COORD`, `STEP_SIZE`, `TIME_TYPE`, `QUANTITIES`, `APPARENT`, and `CSV_FORMAT` are supported observer-table parameters. The Horizons manual identifies observer quantity 4 as apparent azimuth/elevation, measured clockwise from north with elevation relative to the plane perpendicular to local zenith. This verifies the documented parameter choices, but not a successful live request from MoonSight.

Sources:
- https://ssd-api.jpl.nasa.gov/doc/horizons.html
- https://ssd.jpl.nasa.gov/horizons/manual.html

## Validation still required

- [ ] Run a live JPL Horizons query from the deployed app and inspect the returned metadata/table.
- [ ] Independently verify the exact geodetic coordinate convention and reference model for the selected lunar observer.
- [ ] Compare a known observer query against a manually configured Horizons interface query.
- [ ] Add rate limiting/caching before public deployment.
- [ ] Verify the full repository test suite.
- [ ] Do not mark live astronomy validation complete until a real API response has been inspected.
