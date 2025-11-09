# DNS Setup (Pre-flight)

Goal: `https://app.<your-domain>` serves the frontend; `/api` proxied to backend via service mesh or ALB.

## Records
- **A / AAAA (ALIAS)** → point `app.<your-domain>` to your **ALB** (recommended) or public VM IP.
- **Optional:** `api.<your-domain>` → CNAME to same ALB, if splitting hosts.

## Steps (generic)
1. Create/identify your domain in your DNS provider.
2. Add records:
   - **ALB:** A/AAAA **ALIAS** (or CNAME if provider supports) to the ALB DNS name.
   - **VM:** A (IPv4) and AAAA (IPv6) to your server IP.
3. (TLS) Request an **ACM** certificate for `app.<your-domain>` (and `api.<your-domain>` if used).
4. Wait for validation; attach certificate to the ALB HTTPS listener.

## Acceptance checks
```bash
# DNS resolution
dig +short app.<your-domain>
# HTTP reachability (after deploy)
curl -I https://app.<your-domain>
```
