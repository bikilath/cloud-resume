# Cloud Resume Challenge - Azure

This repository contains my implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/) for Azure.

## Project Structure

- `frontend/`: Contains the static website files (HTML, CSS, JS)
- `backend/`: Contains the Azure Function code and infrastructure as code templates
- `.github/workflows/`: Contains GitHub Actions workflows for CI/CD

## Technologies Used

- Azure Static Web Apps
- Azure Functions
- Azure Storage (Tables)
- GitHub Actions
- Python
- JavaScript

## Deployment

### GitHub Pages Deployment
The static website is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. To set this up:

1. Go to your repository settings
2. Navigate to "Pages" under "Code and automation"
3. Under "Build and deployment":
   - Set Source to "GitHub Actions"
   - The workflow will handle the rest automatically

The site will be available at `https://<your-username>.github.io/cloud-resume/`

No additional secrets are required as GitHub Pages deployment uses built-in GitHub token and permissions.

### Azure Deployment
The application can also be deployed to Azure through GitHub Actions when changes are pushed to the `main` branch.

## Visitor Counter

The visitor counter is implemented using:
1. Frontend JavaScript that calls an API
2. Azure Function (Python) that increments a counter
3. Azure Table Storage to persist the count
