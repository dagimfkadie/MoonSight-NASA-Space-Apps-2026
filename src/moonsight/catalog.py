"""Metadata for study regions listed in NASA's South Pole LOLA DEM archive.

The catalog intentionally contains no invented latitude/longitude coordinates.
The region identifiers and names below are transcribed from the NASA archive page.
"""

from dataclasses import dataclass
NASA_LOLA_SITES_URL = "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/"


@dataclass(frozen=True, slots=True)
class StudySite:
    """A named LOLA study-region product group."""

    site_id: str
    name: str
    description: str
    source_url: str = NASA_LOLA_SITES_URL


LOLA_STUDY_SITES: tuple[StudySite, ...] = (
    StudySite("Site01", "Connecting ridge", "NASA LOLA south-pole study-region product group."),
    StudySite("Site04", "Shackleton rim", "NASA LOLA south-pole study-region product group."),
    StudySite("Site07", "Peak near Shackleton", "NASA LOLA south-pole study-region product group."),
    StudySite("Site11", "de Gerlache rim", "NASA LOLA south-pole study-region product group."),
    StudySite("Site20", "Leibnitz beta plateau", "NASA LOLA south-pole study-region product group."),
    StudySite("Site23", "Malapert massif", "NASA LOLA south-pole study-region product group."),
)


def get_site(site_id: str) -> StudySite:
    """Return a known study site or raise ValueError for an unknown identifier."""
    for site in LOLA_STUDY_SITES:
        if site.site_id == site_id:
            return site
    raise ValueError(f"Unknown LOLA study site: {site_id}")
