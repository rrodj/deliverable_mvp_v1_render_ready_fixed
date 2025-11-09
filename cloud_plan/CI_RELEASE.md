# CI Release Plan — Inventory Guardian (Containers + Tags)

**Generated:** 2025-11-07T17:34:10Z

This plan publishes **two images** to a registry (choose **GHCR** *or* **AWS ECR**), tags them, and prepares values for Terraform.

Artifacts:
- Backend: `deploy/Dockerfile.backend` → image `inventory-guardian/backend:<tag>`
- Frontend: `deploy/Dockerfile.frontend` → image `inventory-guardian/frontend:<tag>`

## Option A — GitHub Container Registry (GHCR)
**Inputs (GitHub Secrets):**
- `GHCR_USERNAME` — your GitHub username or org
- `GHCR_TOKEN` — a PAT with `write:packages` scope

**Workflow snippet:**
```yaml
name: release
on:
  push:
    tags: [ 'v*.*.*' ]
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        run: echo "${ secrets.GHCR_TOKEN }" | docker login ghcr.io -u "${ secrets.GHCR_USERNAME }" --password-stdin

      - name: Build images
        run: |
          docker build -t ghcr.io/${ github.repository_owner }/inventory-guardian/backend:${ github.ref_name } -f deploy/Dockerfile.backend .
          docker build -t ghcr.io/${ github.repository_owner }/inventory-guardian/frontend:${ github.ref_name } -f deploy/Dockerfile.frontend .

      - name: Push
        run: |
          docker push ghcr.io/${ github.repository_owner }/inventory-guardian/backend:${ github.ref_name }
          docker push ghcr.io/${ github.repository_owner }/inventory-guardian/frontend:${ github.ref_name }

      - name: Release outputs
        run: |
          echo "BACKEND_IMAGE=ghcr.io/${ github.repository_owner }/inventory-guardian/backend:${ github.ref_name }" >> $GITHUB_ENV
          echo "FRONTEND_IMAGE=ghcr.io/${ github.repository_owner }/inventory-guardian/frontend:${ github.ref_name }" >> $GITHUB_ENV
```

## Option B — AWS Elastic Container Registry (ECR)
**Inputs (GitHub Secrets):**
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- `ECR_ACCOUNT_ID` (12-digit)

**Workflow snippet:**
```yaml
name: release-ecr
on:
  push:
    tags: [ 'v*.*.*' ]
jobs:
  build-and-push-ecr:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ${ secrets.AWS_REGION }
          aws-access-key-id: ${ secrets.AWS_ACCESS_KEY_ID }
          aws-secret-access-key: ${ secrets.AWS_SECRET_ACCESS_KEY }

      - name: Login to ECR
        run: |
          aws ecr get-login-password --region ${ secrets.AWS_REGION } |           docker login --username AWS --password-stdin ${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com

      - name: Build
        run: |
          docker build -t backend:${ github.ref_name } -f deploy/Dockerfile.backend .
          docker build -t frontend:${ github.ref_name } -f deploy/Dockerfile.frontend .

      - name: Tag & Push
        run: |
          docker tag backend:${ github.ref_name } ${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/inventory-guardian/backend:${ github.ref_name }
          docker tag frontend:${ github.ref_name } ${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/inventory-guardian/frontend:${ github.ref_name }
          docker push ${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/inventory-guardian/backend:${ github.ref_name }
          docker push ${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/inventory-guardian/frontend:${ github.ref_name }

      - name: Release outputs
        run: |
          echo "BACKEND_IMAGE=${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/inventory-guardian/backend:${ github.ref_name }" >> $GITHUB_ENV
          echo "FRONTEND_IMAGE=${ secrets.ECR_ACCOUNT_ID }.dkr.ecr.${ secrets.AWS_REGION }.amazonaws.com/inventory-guardian/frontend:${ github.ref_name }" >> $GITHUB_ENV
```

## After publish (common)
- Update `terraform/vars_example.tfvars` with the two image URLs (or pass via `-var-file`).
- Preflight check:
  ```bash
  # GHCR
  docker pull ghcr.io/<org>/inventory-guardian/backend:vX.Y.Z
  docker pull ghcr.io/<org>/inventory-guardian/frontend:vX.Y.Z

  # or ECR
  aws ecr describe-images --repository-name inventory-guardian/backend --image-ids imageTag=vX.Y.Z
  aws ecr describe-images --repository-name inventory-guardian/frontend --image-ids imageTag=vX.Y.Z
  ```
