# Terraform Vars — Example (fill and pass with -var-file)

project_name             = "inventory-guardian"
region                   = "us-east-1"

# Images (from CI release)
container_image_backend  = "ghcr.io/your-org/inventory-guardian/backend:v0.1.0"
container_image_frontend = "ghcr.io/your-org/inventory-guardian/frontend:v0.1.0"

# Capacity
desired_count            = 1
cpu_backend              = 256
memory_backend           = 512
cpu_frontend             = 256
memory_frontend          = 512

# Networking (use your existing VPC/subnets)
vpc_id                   = "vpc-xxxx"
public_subnet_ids        = ["subnet-aaaa", "subnet-bbbb"]
private_subnet_ids       = ["subnet-cccc", "subnet-dddd"]

# Domain & TLS
domain_name              = "example.com"
subdomain_app            = "app"
subdomain_api            = "api"
certificate_arn          = "arn:aws:acm:us-east-1:123456789012:certificate/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Env (prefer SSM/Secrets Manager in apply step)
app_env                  = "production"
cors_origins             = "https://app.example.com"
demo_api_token           = "set-a-random-dev-token"
stripe_webhook_secret    = "whsec_placeholder"
stripe_price_starter     = "price_starter_xxx"
stripe_price_pro         = "price_pro_xxx"
stripe_price_enterprise  = "price_enterprise_xxx"
billing_portal_url       = "https://billing-portal.example/placeholder"
