# Phase 4 — Scientific calculation engine

## Implemented

- [x] JPL Horizons API client for observer-table queries.
- [x] User-entered lunar geodetic observer coordinates; no invented coordinates are assigned to LOLA tiles.
- [x] Sun (target 10) and Earth (target 399) request support.
- [x] Apparent azimuth/elevation quantity 4, airless setting, UTC time.
- [x] CSV ephemeris parsing with missing-angle handling.
- [x] Input validation for longitude, latitude, altitude, target and request duration.
- [x] Network/API error handling.
- [x] Unit tests using synthetic response fixtures and a fake HTTP session.

## Formula and interpretation

Horizons supplies apparent topocentric azimuth and elevation. MoonSight does not derive these angles from an unverified simplified orbital model. Azimuth is clockwise from north; elevation is relative to the local plane perpendicular to zenith.

For the Sun, elevation above zero is only a geometric direction indicator. It is not a terrain-aware illumination-duration calculation or solar-power estimate.

For Earth, elevation above zero is only a geometric visibility indicator. It does not prove an unobstructed terrain path or radio communication.

## Coordinate inputs

Horizons geodetic SITE_COORD order is east longitude (degrees), latitude (degrees), altitude (kilometres). The observer is sent as `coord@301`, a topocentric site on the Moon. Users must provide a documented lunar surface coordinate. A named LOLA study-region ID is not automatically converted into latitude/longitude.

## Validation still required

- [ ] Run a live JPL Horizons query from the deployed app and inspect the returned metadata/table.
- [ ] Independently verify the exact geodetic coordinate convention and reference model for the selected lunar observer.
- [ ] Compare a known observer query against a manually configured Horizons interface query.
- [ ] Add rate limiting/caching before public deployment.
- [ ] Verify the full repository test suite.
- [ ] Do not mark live astronomy validation complete until a real API response has been inspected.
