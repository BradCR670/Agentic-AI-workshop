"""Mock warranty status lookup tool."""

from calendar import monthrange
from datetime import date, datetime
from typing import Any


_MOCK_WARRANTY_LOOKUP: dict[str, dict[str, Any]] = {
    "GTW465ASNWW": {
        "coverage_months": 12,
        "coverage_type": "standard laundry coverage",
        "notes": "Parts and labor are covered for the first year.",
    },
    "GFW850SPNRS": {
        "coverage_months": 36,
        "coverage_type": "premium front-load washer coverage",
        "notes": "Includes motor and drum coverage through the extended term.",
    },
    "GSS25GYPFS": {
        "coverage_months": 24,
        "coverage_type": "refrigerator sealed-system coverage",
        "notes": "Sealed-system components receive extra attention in service review.",
    },
    "JGB735SPSS": {
        "coverage_months": 18,
        "coverage_type": "gas range limited coverage",
        "notes": "Igniter and control-board diagnostics are prioritized.",
    },
    "PDT715SYNFS": {
        "coverage_months": 30,
        "coverage_type": "dishwasher quiet-package coverage",
        "notes": "Pump, rack, and leak-sensor claims are eligible during coverage.",
    },
}


def verify_warranty_status(model_name: str, purchase_date: str) -> dict[str, object]:
    """Return mocked warranty status for a model and ISO purchase date."""
    normalized_model = model_name.strip().upper()
    warranty_record = _MOCK_WARRANTY_LOOKUP.get(normalized_model)

    if warranty_record is None:
        return {
            "model_name": normalized_model,
            "status": "unknown_model",
            "coverage_end_date": None,
            "days_remaining": None,
            "details": "No mock warranty rule is available for this model.",
        }

    try:
        purchased_on = datetime.strptime(purchase_date, "%Y-%m-%d").date()
    except ValueError:
        return {
            "model_name": normalized_model,
            "status": "invalid_purchase_date",
            "coverage_end_date": None,
            "days_remaining": None,
            "details": "Use YYYY-MM-DD format for purchase_date.",
        }

    coverage_months = int(warranty_record["coverage_months"])
    month_index = purchased_on.month - 1 + coverage_months
    coverage_year = purchased_on.year + month_index // 12
    coverage_month = month_index % 12 + 1
    coverage_day = min(purchased_on.day, monthrange(coverage_year, coverage_month)[1])
    coverage_end = date(coverage_year, coverage_month, coverage_day)
    days_remaining = (coverage_end - date.today()).days
    status = "active" if days_remaining >= 0 else "expired"

    return {
        "model_name": normalized_model,
        "status": status,
        "coverage_end_date": coverage_end.isoformat(),
        "days_remaining": max(days_remaining, 0),
        "details": f"{warranty_record['coverage_type']}: {warranty_record['notes']}",
    }
