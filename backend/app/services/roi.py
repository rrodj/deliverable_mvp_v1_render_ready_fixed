import datetime
from typing import Dict, Any, List, Optional

def _round(x: float) -> float:
    return round(float(x or 0.0), 2)

def calc_dead_stock_savings(inventory_value_stale: float, carrying_cost_rate_monthly: float = 0.02) -> float:
    """Estimate savings by eliminating carrying cost on stale inventory this month.
    Example: $5,000 stale * 2% monthly = $100 protected.
    """
    return _round(inventory_value_stale * carrying_cost_rate_monthly)

def calc_stockout_avoided_loss(stockout_events_avoided: int, avg_margin_per_event: float) -> float:
    """Estimate avoided contribution loss from stockouts prevented by alerts/process.
    Example: 8 events * $35 = $280 protected.
    """
    return _round(stockout_events_avoided * avg_margin_per_event)

def calc_promo_bleed_reduction(gross_sales_promos: float, planned_discount_rate: float, actual_discount_rate: float, intervention_fraction: float = 0.5) -> float:
    """Estimate savings by reducing promo bleed (discount above plan) for a fraction of sales after intervention.
    Example: $12,000 promo sales * (16% - 10%) * 50% = $360 protected.
    """
    extra = max(0.0, actual_discount_rate - planned_discount_rate)
    return _round(gross_sales_promos * extra * intervention_fraction)

_ALERT_VALUE = {"critical": 75.0, "warning": 25.0, "info": 5.0}

def calc_alert_savings(alerts: List[Dict[str, Any]]) -> float:
    """Translate alert mix into conservative savings proxy.
    This is intentionally modest and should be refined with real pilot data.
    """
    total = 0.0
    for a in alerts or []:
        lvl = (a.get("level") or "info").lower()
        total += _ALERT_VALUE.get(lvl, 5.0)
    return _round(total)

def _default_seed() -> Dict[str, Any]:
    # Conservative defaults so widget renders out-of-the-box
    return {
        "dead_stock": {"inventory_value_stale": 5000.0, "carrying_cost_rate_monthly": 0.02},
        "stockouts": {"stockout_events_avoided": 8, "avg_margin_per_event": 35.0},
        "promo_bleed": {"gross_sales_promos": 12000.0, "planned_discount_rate": 0.10, "actual_discount_rate": 0.16, "intervention_fraction": 0.5},
    }

def monthly_roi_summary(*, alerts: Optional[List[Dict[str, Any]]] = None, seed: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Compose a monthly ROI snapshot from provided inputs and alert mix."""
    seed = seed or _default_seed()
    month = datetime.datetime.utcnow().strftime("%Y-%m")

    dead_stock_in = seed.get("dead_stock", {})
    dead_stock_usd = calc_dead_stock_savings(dead_stock_in.get("inventory_value_stale", 0.0), dead_stock_in.get("carrying_cost_rate_monthly", 0.02))

    stockouts_in = seed.get("stockouts", {})
    stockouts_usd = calc_stockout_avoided_loss(stockouts_in.get("stockout_events_avoided", 0), stockouts_in.get("avg_margin_per_event", 0.0))

    promo_in = seed.get("promo_bleed", {})
    promo_usd = calc_promo_bleed_reduction(promo_in.get("gross_sales_promos", 0.0), promo_in.get("planned_discount_rate", 0.0), promo_in.get("actual_discount_rate", 0.0), promo_in.get("intervention_fraction", 0.5))

    alerts_usd = calc_alert_savings(alerts or [])

    total = _round(dead_stock_usd + stockouts_usd + promo_usd + alerts_usd)

    return {
        "month": month,
        "components": {
            "dead_stock": {"usd": dead_stock_usd, "inputs": dead_stock_in},
            "stockouts": {"usd": stockouts_usd, "inputs": stockouts_in},
            "promo_bleed": {"usd": promo_usd, "inputs": promo_in},
            "alerts": {"usd": alerts_usd, "value_map": _ALERT_VALUE},
        },
        "total_protected_usd": total,
        "assumptions": {
            "note": "Conservative heuristics. Replace with pilot benchmarks as data accrues."
        }
    }
