# AI assistance disclosure

This record describes AI assistance used while developing MoonSight. The team must review this record, add all tools actually used, and identify human review accurately before submission.

## AI tools

| Tool | Purpose | Work assisted | Human verification status |
|---|---|---|---|
| ChatGPT (OpenAI) | Planning, explanations, code drafting, code review suggestions and documentation | Python package design; NASA LOLA downloader and raster summaries; Plotly terrain preview; JPL Horizons client; Streamlit UI; tests; phase checklists and README | AI-generated changes were committed to GitHub. Full clean-environment tests, live data checks, and human review by every contributor remain outstanding. |

## AI-assisted files/features in this development session

- `src/moonsight/astronomy/horizons.py`: JPL Horizons request construction, response validation and observer-table parsing.
- `src/moonsight/terrain/preview.py`: bounded raster preview, 2-D heatmap and 3-D surface helper.
- `app.py`: Streamlit tabs for terrain exploration, descriptive region comparison, and user-entered Sun/Earth ephemeris requests.
- `tests/test_horizons.py`, `tests/test_terrain_preview.py`, and `tests/test_app_smoke.py`: synthetic test fixtures, expected behavior, and a Streamlit startup smoke test.
- `docs/PHASE1_CHECKLIST.md`, `docs/PHASE2_CHECKLIST.md`, `docs/PHASE4_CHECKLIST.md`, `docs/PHASE5_CHECKLIST.md`, `docs/ARCHITECTURE.md`, and `README.md`: documentation and status records.

## Human contributions

Add each team member's name or agreed public identifier, actual tasks, and evidence. Do not attribute AI-generated code to a student as independently authored work.

| Contributor | Actual contribution | Evidence |
|---|---|---|
| Team members | Must be completed by the team from their actual work | Pending confirmation |

## Verification record

| Area | Verification performed | Remaining work |
|---|---|---|
| Terrain preview | Four focused synthetic preview tests were previously recorded as passing in an isolated test package | Run committed tests in a clean clone; test against a real NASA raster |
| Raster statistics | Three focused synthetic summary tests were previously recorded as passing | Run full repository suite |
| Horizons client | Test cases added for parsing, input validation, request parameters and response signature | Execute tests; perform live query and compare against Horizons interface |
| Streamlit interface | Code committed; AppTest startup smoke test added to the suite | Execute AppTest/CI, launch app, inspect all tabs and exports |
| CI | GitHub Actions workflow committed | Confirm workflow run and fix any failures |

## Media

No AI-generated images, video or audio are required by the current prototype. If the team adds AI-generated or AI-edited media, record the tool, the exact asset, and the required attribution/permissions after checking current NASA Space Apps rules.

## Accuracy commitment

AI assistance is not proof that code works or scientific results are correct. The team is responsible for understanding, reviewing, testing and accurately describing all submitted work. Do not claim AI-generated code or content was independently written by a team member.
