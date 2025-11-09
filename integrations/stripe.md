# Stripe Integration (Read‑only Webhooks)

**Endpoint:** `POST /webhooks/stripe`
Use Stripe CLI to forward events locally:
```bash
stripe listen --events checkout.session.completed,invoice.paid,customer.subscription.created \\
  --forward-to http://localhost:8000/webhooks/stripe
```
