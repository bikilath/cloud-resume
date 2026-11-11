# Cloud Resume Challenge - Azure

A personal cloud portfolio project combining a static resume website, a Python visitor-counter API and GitHub Actions deployment workflows.

## Architecture

```text
Browser -> Static website (public/)
                  |
                  | POST /api/visitor/
                  v
          Azure Functions (Python)
                  |
                  v
          Azure Table Storage
```

The counter implementation uses **Azure Table Storage**, not Cosmos DB. The frontend currently targets a specific Azure Static Web Apps API URL in `public/assets/js/script.js`.

## Repository structure

```text
public/
  index.html                     Resume webpage
  assets/css/style.css           Styles
  assets/js/script.js            Visitor-counter client
  assets/images/profile.jpeg     Profile image
api/
  GetVisitorCount/__init__.py     Counter implementation
  GetVisitorCount/function.json   HTTP trigger definition
  requirements.txt               API dependencies
.github/workflows/
  deploy-pages.yml               GitHub Pages deployment
  azure-static-web-apps-*.yml     Azure Static Web Apps deployment
```

## Preview the website locally

From the repository root:

```bash
python3 -m http.server 8000 --directory public
```

Open `http://localhost:8000`. This serves the frontend only. The JavaScript still calls the configured Azure endpoint; the counter can show an offline state if that endpoint is unavailable or rejects the origin.

## Deployment configuration

### GitHub Pages

The Pages workflow uploads `public/` and runs on pushes to `main` or `pages`, or a manual trigger. Configure repository Pages settings to use GitHub Actions. Pages hosts the static files; it does not run the Python API.

### Azure Static Web Apps

The Azure workflow uses `public/` for the application and `api/` for the API. It runs for pushes to `main` and selected pull-request events, which may create preview deployments. It references a repository deployment-token secret. Configure the corresponding Azure resource and secret before using this workflow in another repository.

The API expects `AzureWebJobsStorage` in its environment and a `VisitorCounts` table. Configure connection strings in application settings, never in committed files. Replace the frontend API URL and configure allowed origins for your own deployment.

## Current limitations and next improvements

This is a learning project; deployment success and live availability must be checked in the target environment.

- The Python API mixes decorator-based registration with a `function.json` layout, and the repository lacks `host.json`. Standardize the Functions project layout before documenting a complete local backend workflow.
- CORS headers currently target the Azure site, so GitHub Pages and local previews require additional configuration.
- The counter uses a read-modify-write operation; concurrent requests can lose increments. Add concurrency control before treating counts as reliable analytics.
- Improve backend error handling and add API tests.
- Review the deployment action versions and verify both workflows before relying on them.
- Infrastructure provisioning templates are not currently included in this repository.

## Technologies

Azure Static Web Apps, Azure Functions, Azure Table Storage, GitHub Actions, Python, JavaScript, HTML and CSS.
