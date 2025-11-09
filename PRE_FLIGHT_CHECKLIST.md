# Pre-flight Checklist (Gate N — Plan)

- [ ] Container images exist in registry (backend + frontend).
- [ ] VPC ID and Subnet IDs collected.
- [ ] ACM certificate ARN available for `app.<domain>`.
- [ ] DNS provider access confirmed.
- [ ] `terraform/terraform.tfvars` drafted from `vars_example.tfvars` with placeholders replaced.

Acceptance (next step `/deploy.cloud.apply`):
- We'll validate images can be pulled, `terraform.tfvars` is present, and DNS/ACM values are provided.
