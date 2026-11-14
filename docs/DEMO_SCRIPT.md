# MoonSight Demo Script

This script is a suggested walkthrough for a short project demonstration. Adjust the timing to the official event's current presentation requirements. It describes the current prototype and must not imply that unverified live-data paths have passed validation.

## Before recording or presenting

- [ ] Start from the exact repository commit intended for submission.
- [ ] Launch the app in a clean environment and inspect all four tabs.
- [ ] Confirm whether NASA archive and JPL Horizons network requests work on the demo connection.
- [ ] If external services are unavailable, use clearly labelled screenshots or previously retrieved data with documented provenance. Do not present mock data as live NASA data.
- [ ] Hide personal notifications, credentials and private browser tabs.
- [ ] Keep the README and User Guide available as references.

## Suggested 3-minute walkthrough

### 0:00–0:25 — Introduce the problem

"Exploring lunar south-pole terrain involves more than looking at one map. Researchers need to understand elevation, slope, measurement coverage and uncertainty, as well as how the apparent directions of the Sun and Earth change over time. MoonSight brings selected public data sources into one educational exploration interface."

### 0:25–1:15 — Explore terrain data

1. Open **Terrain explorer**.
2. Select one of the listed LOLA study regions and a product such as elevation or slope.
3. Explain the source archive and displayed units.
4. Show the 2-D terrain view and, for elevation, the sampled 3-D view.
5. Explain that the statistics and visualizations use bounded nearest-neighbour samples.

Suggested narration: "These are NASA LOLA archive products. MoonSight makes them easier to inspect, but the preview is downsampled and the displayed statistics are sample statistics—not a full-resolution hazard analysis."

### 1:15–1:45 — Compare regions

1. Open **Compare regions**.
2. Choose the same product for two regions.
3. Explain the descriptive statistics and CSV export.

Suggested narration: "This comparison helps users inspect differences in the sampled data. It does not calculate a weighted score or rank landing sites."

### 1:45–2:30 — Sun and Earth geometry

1. Open **Sun & Earth geometry**.
2. Enter a documented lunar geodetic observer coordinate and date.
3. Request Sun and Earth observer ephemerides if the live API is available.
4. Explain azimuth and elevation and show the CSV export if appropriate.

Suggested narration: "These directions come from JPL Horizons for the coordinate entered by the user. They are geometric directions; this prototype does not account for local terrain obstruction or establish communications availability."

If the API has not been independently validated, state that the live request is a demonstration of the integration and that independent comparison remains pending.

### 2:30–3:00 — Close with limitations and next steps

"MoonSight is an educational prototype, not a landing-safety or mission-planning system. Our next priorities are to verify real NASA raster metadata, confirm the lunar coordinate reference frame, independently compare Horizons results, and only then investigate terrain-aware visibility."

## Questions the team should be ready to answer

- Which NASA LOLA products are used, and what are their units?
- What does the app sample, and why are the statistics not full-raster statistics?
- How does the user provide the lunar observer coordinate?
- What does apparent azimuth/elevation tell us—and what does it not tell us?
- Which scientific validation tasks remain pending?
- What did each team member contribute?
- How was generative AI used, and how did the team verify AI-assisted work?

## Demo integrity

- Never claim a live request succeeded unless the result was actually returned during the demo or is clearly identified as a saved result.
- Never call a sample statistic a full-resolution measurement.
- Never present a site ranking, landing-safety score, power estimate or communications result; these are not implemented.
- If a feature fails, explain the failure honestly and show the documented fallback rather than hiding it.

**Status:** Suggested narration and walkthrough prepared. A successful rehearsal and final recording are still required.
