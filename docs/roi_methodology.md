# ROI Methodology — Inventory Guardian (Pilot Draft)

**Generated:** 2025-11-06T07:45:54Z

This module estimates **protected value** (USD) from four contributors:
1. **Dead stock carrying cost avoided** — stale inventory value × monthly carrying cost %.
2. **Stockouts avoided** — stockout events avoided × average contribution margin per event.
3. **Promo bleed reduction** — promo gross sales × (actual − planned discount) × intervention fraction.
4. **Alerts mix proxy** — conservative value per alert level (critical = $75, warning = $25, info = $5).

> These are conservative placeholders to make ROI visible during pilot setup. Replace with **pilot‑specific benchmarks** as data accrues (POS exports, shrink logs, promo plans).

## Defaults (MVP)
- Stale inventory: **$5,000**, monthly carrying **2%** → **$100**.
- Stockouts avoided: **8 events**, **$35** margin → **$280**.
- Promo bleed: promo sales **$12,000**, plan **10%**, actual **16%**, influenced **50%** → **$360**.
- Alerts mix proxy: one info alert → **$5** (adjusts with real alerts).

**Total example:** $100 + $280 + $360 + $5 = **$745** protected this month.

## How to tune (with pilot data)
- Provide average on‑hand age bands and carrying % for dead stock.
- Export stockout log (OOS minutes × hourly rate or event × margin).
- Provide promo calendar (planned vs. realized discounts).
- Map alert types to specific shrink/ops costs.

## Validation
- Keep monthly notes and receipts for each intervention (markdown or spreadsheet).
- Compare a **baseline month** to a **post‑alerts month** for claim defensibility.
