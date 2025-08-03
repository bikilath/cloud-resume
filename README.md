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

The application is automatically deployed to Azure through GitHub Actions when changes are pushed to the `main` branch.

## Visitor Counter

The visitor counter is implemented using:
1. Frontend JavaScript that calls an API
2. Azure Function (Python) that increments a counter
3. Azure Table Storage to persist the count
