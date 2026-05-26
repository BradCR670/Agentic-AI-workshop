import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


INPUT_FILE = Path("service_calls.csv")
OUTPUT_FILE = Path("triaged_service_calls.csv")
HIGH_PRIORITY = "High Priority"
STANDARD_PRIORITY = "Standard Priority"


def parse_claim_value(value):
    cleaned_value = value.replace("$", "").replace(",", "").strip()

    try:
        return Decimal(cleaned_value)
    except InvalidOperation:
        return Decimal("0")


def determine_priority(row):
    claim_value = parse_claim_value(row.get("CLAIM_VALUE", "0"))
    warranty_status = row.get("WARRANTY_STATUS", "").strip().lower()

    if claim_value >= Decimal("500") and warranty_status == "valid":
        return HIGH_PRIORITY

    return STANDARD_PRIORITY


def main():
    with INPUT_FILE.open("r", newline="") as input_file:
        reader = csv.DictReader(input_file)
        fieldnames = list(reader.fieldnames or [])

        if "PRIORITY" not in fieldnames:
            fieldnames.append("PRIORITY")

        rows = []
        for row in reader:
            row["PRIORITY"] = determine_priority(row)
            rows.append(row)

    with OUTPUT_FILE.open("w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Triaged {len(rows)} service calls into {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
