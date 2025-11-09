# Terraform Cloud Plan (Pre-flight Only)

**Generated:** 2025-11-07T17:34:10Z

This plan assumes AWS ECS Fargate + ALB. Templates are stubs in the MVP repo (`deploy/terraform/`). In **/deploy.cloud.apply** we will provide an apply pack and CI job.

## What to prepare
- **Registry images** published (see `CI_RELEASE.md`).
- **VPC/Subnets** available (IDs noted).
- **ACM** certificate validated for `app.<domain>` (and `api.<domain>` if separate).
- **DNS** ready to point to ALB.

## Usage
1. Copy `terraform/vars_example.tfvars` to `terraform/terraform.tfvars` and fill placeholders.
2. Initialize Terraform (when apply pack is generated):
   ```bash
   terraform init
   terraform plan -var-file=terraform/terraform.tfvars
   ```

## State (optional pre-flight)
Use a remote backend (S3 + DynamoDB) — configure during apply:
- S3 bucket: `tfstate-<project>`
- DynamoDB table: `tfstate-lock`

No cloud resources are created by this plan pack alone.
