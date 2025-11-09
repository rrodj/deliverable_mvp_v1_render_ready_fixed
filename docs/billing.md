# Billing Enablement (MVP Stub) — Inventory Guardian

**Generated:** 2025-11-06T08:19:15Z

This patch adds:
- **Price model:** Starter / Pro / Enterprise (monthly).
- **Webhook wiring:** `/webhooks/stripe` applies subscription events into billing state.
- **Billing endpoints:** `/billing/prices`, `/billing/status`, `/billing/portal` (stub).
- **Frontend Settings:** shows plan; button to open billing portal.

## Local test with Stripe CLI (no secrets committed)
1. Start backend on port **8000**.
2. In another terminal, run:
   ```bash
   stripe listen --events checkout.session.completed,customer.subscription.created,customer.subscription.updated,customer.subscription.deleted \\
     --forward-to http://localhost:8000/webhooks/stripe
   ```
   Copy the printed `whsec_...` value into your local `.env` (e.g., `.env.stripe`).

3. Send sample events:
   ```bash
   curl -sS http://localhost:8000/webhooks/stripe -H "Content-Type: application/json" -H "Stripe-Signature: t=0,v1=stub" --data @examples/stripe/checkout.session.completed.json | jq .
   curl -sS http://localhost:8000/webhooks/stripe -H "Content-Type: application/json" -H "Stripe-Signature: t=0,v1=stub" --data @examples/stripe/customer.subscription.created.json | jq .
   ```

4. Check status:
   ```bash
   curl -H "Authorization: Bearer demo-token-please-change" http://localhost:8000/billing/status | jq .
   ```

## Environment
Fill placeholders in `.env.stripe.example` (copy to `.env.stripe` locally):
- `STRIPE_WEBHOOK_SECRET` — from Stripe CLI (dev) or dashboard (prod).
- `STRIPE_PRICE_STARTER`, `STRIPE_PRICE_PRO`, `STRIPE_PRICE_ENTERPRISE` — your price IDs.
- `STRIPE_BILLING_PORTAL_URL` — optional link to a hosted customer portal (or your route).

## Notes
- This is a **read-only** billing stub — no live API calls to Stripe are made.
- Event application updates in-memory state only; persist later when DB is integrated.
