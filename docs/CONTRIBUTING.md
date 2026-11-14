# Contributing to MoonSight

Thank you for helping improve MoonSight. This is an educational prototype; prioritize correctness, traceability and clear limitations over unsupported claims.

## Before changing code

1. Read the [Project Overview](PROJECT_OVERVIEW.md), [Architecture](ARCHITECTURE.md) and [Scientific Methodology](SCIENTIFIC_METHODOLOGY.md).
2. Check existing issues and pull requests to avoid duplicate work.
3. Discuss substantial changes with the team before changing shared interfaces or project scope.
4. Never commit credentials, API keys, private information or large unreviewed data files.

## Development setup

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
streamlit run app.py
```

Activate the virtual environment before installing or running the application.

## Change guidelines

- Keep data retrieval, calculations and presentation separated.
- Preserve units, coordinate frames, timestamps and source attribution.
- Validate user input and handle missing or invalid data explicitly.
- Do not silently substitute missing values with zero.
- Label sampled outputs as samples; do not imply full-raster analysis.
- Avoid adding site rankings, landing-safety scores or mission claims without a documented and independently validated method.
- Keep external service requests bounded and handle service failures clearly.
- Add or update tests for changed behavior.
- Update user-facing documentation when workflows or limitations change.

## Pull request checklist

- [ ] The change has a clear purpose and bounded scope.
- [ ] Code and documentation are understandable to another team member.
- [ ] Tests were added or updated where appropriate.
- [ ] Relevant checks were run and their results are reported accurately.
- [ ] Data sources, units, coordinate systems and assumptions are documented.
- [ ] No secrets, personal information or unauthorized data are included.
- [ ] Scientific claims are supported and limitations are stated.
- [ ] AI assistance is disclosed where applicable.

## Reporting a bug

Include the operating system, Python version, steps to reproduce, expected behavior, actual behavior and relevant error output. Remove credentials and personal information before sharing logs.

## Team and authorship

Only credit people for contributions they actually made. Agree on authorship and review responsibilities with the team before final submission. This guide does not create or imply a team agreement.
