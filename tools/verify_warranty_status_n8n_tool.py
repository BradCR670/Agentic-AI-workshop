"""n8n Custom Code Tool: mock warranty status lookup."""

import json
from calendar import monthrange
from datetime import date, datetime


MOCK_WARRANTY_LOOKUP = {
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


def parse_input(raw_query):
    if isinstance(raw_query, dict):
        return raw_query

    try:
        return json.loads(str(raw_query))
    except Exception:
        return {}


def verify_warranty_status(model_name, purchase_date):
    normalized_model = str(model_name or "").strip().upper()

    if not normalized_model or not purchase_date:
        return {
            "model_name": normalized_model,
            "status": "missing_input",
            "coverage_end_date": None,
            "days_remaining": None,
            "details": "Provide model and purchase_date.",
        }

    warranty_record = MOCK_WARRANTY_LOOKUP.get(normalized_model)

    if warranty_record is None:
        return {
            "model_name": normalized_model,
            "status": "unknown_model",
            "coverage_end_date": None,
            "days_remaining": None,
            "details": "No mock warranty rule is available for this model.",
        }

    try:
        purchased_on = datetime.strptime(str(purchase_date), "%Y-%m-%d").date()
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


try:
    raw_query = _query
except NameError:
    try:
        raw_query = query
    except NameError:
        raw_query = "{}"
tool_input = parse_input(raw_query)
result = verify_warranty_status(
    tool_input.get("model"),
    tool_input.get("purchase_date"),
)

return json.dumps(result)
