## Deploying to Azure (quick guide)

Option A — Web App for Containers (using Dockerfile):
1. Push repo to GitHub.
2. Create Azure Container Registry (ACR) and push a container image, or use GitHub Actions to build and push.
3. Create Web App for Containers and point it to the image in ACR.

Option B — App Service (Linux) with source deploy:
- Configure App Service to build from the repository, or use a GitHub Action that builds the Docker image and deploys.

Note: Expose port 8501 and set any environment variables you need. For heavy workloads, increase the plan size.
