# MoonSight deployment guide

## Correct hosting platform

MoonSight is a Python + Streamlit server application. Deploy it on **Streamlit Community Cloud**. Cloudflare Pages' standard static-site deployment (including `npx wrangler deploy`) does not run a Streamlit Python server.

## Deployment settings

Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub. The GitHub account must have admin access to this public repository.

Choose **Create app** → **Yup, I have an app**, then use:

| Setting | Value |
| --- | --- |
| Repository | `dagimfkadie/MoonSight-NASA-Space-Apps-2026` |
| Branch | `main` |
| Main file path | `app.py` |
| Python version | `3.11` |
| Secrets | Leave empty |

Select **Deploy**. The app will be assigned a public `.streamlit.app` URL after the build succeeds.

## Why Python 3.11?

The repository's GitHub Actions CI workflow installs and tests the project with Python 3.11. Selecting the same version keeps the deployment environment aligned with the version used for automated checks.

## Dependencies

The root `requirements.txt` is the dependency manifest used by Community Cloud. It includes Rasterio and the other runtime packages, plus `-e .` to install MoonSight's `src/moonsight` package from `pyproject.toml`.

No `packages.txt`, API secrets, Node.js build, or custom start command is required by the current application.

## Troubleshooting

1. Open the app's **Manage app → Logs** panel.
2. Find the first actual error in the build or runtime log.
3. For a dependency error, check the failing package and Python version before changing dependency pins.
4. For an import error, confirm the repository, `main` branch, root `app.py` entrypoint, and `-e .` line in `requirements.txt`.
5. For a NASA data download error after the app starts, distinguish that runtime data-source failure from a deployment/build failure. The app reports a message and the other tabs should remain available.

The app is an educational prototype. A successful deployment does not certify the scientific validity of live NASA/JPL responses or landing safety.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
