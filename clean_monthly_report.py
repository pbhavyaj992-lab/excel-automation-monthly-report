"""
Clean a messy bookings CSV and make a monthly report.

This is the sample project for Shree Car Care, Anand.
All data here is sample data, not real customers.

What it does:
- Reads data/raw_bookings_messy.csv
- Removes exact duplicate rows
- Fixes dates to YYYY-MM-DD
- Fixes service names to one spelling each
- Fixes payment modes to Cash / UPI / Card
- Cleans amounts (removes Rs symbol and commas)
- Drops rows with no amount, and writes why in the log
- Writes data/clean_bookings.csv
- Writes output/monthly_report_summary.csv
- Writes output/cleaning_log.txt

Needs only Python's built-in csv module. No extra install needed.
Run it from the project folder:
    python3 clean_monthly_report.py
"""

import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# Folders, relative to this file
BASE = Path(__file__).parent
RAW_FILE = BASE / "data" / "raw_bookings_messy.csv"
CLEAN_FILE = BASE / "data" / "clean_bookings.csv"
SUMMARY_FILE = BASE / "output" / "monthly_report_summary.csv"
LOG_FILE = BASE / "output" / "cleaning_log.txt"

# One name for each service, no matter how it was typed in the raw file
SERVICE_MAP = {
    "ceramic coating": "Ceramic Coating",
    "ceramic coat": "Ceramic Coating",
    "car wash": "Car Wash",
    "interior detailing": "Interior Detailing",
    "interior detaling": "Interior Detailing",  # common typo in the raw file
    "exterior polish": "Exterior Polish",
    "paint protection film": "Paint Protection Film",
}


def clean_date(text):
    """Try DD/MM/YYYY first, then YYYY-MM-DD. Return YYYY-MM-DD or ''."""
    text = text.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def clean_amount(text):
    """Remove Rs symbol, commas and spaces. Return a float or None."""
    text = text.strip().replace("₹", "").replace("Rs", "").replace(",", "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def clean_payment(text):
    """Cash, UPI and Card - same word, whatever the case was."""
    text = text.strip().lower()
    if text == "cash":
        return "Cash"
    if text == "upi":
        return "UPI"
    if text == "card":
        return "Card"
    return text.title()


def main():
    log = []
    log.append("Shree Car Care, Anand - cleaning log")
    log.append("Sample data only.")
    log.append("")

    with open(RAW_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)

    total_raw = len(raw_rows)
    log.append(f"Rows in raw file: {total_raw}")

    # 1. Drop exact duplicate rows, keep the first copy
    seen = set()
    unique_rows = []
    duplicates = 0
    for row in raw_rows:
        key = tuple((row.get(k) or "").strip() for k in row)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique_rows.append(row)
    log.append(f"Exact duplicate rows removed: {duplicates}")

    # 2. Clean each row, drop rows with no usable amount
    clean_rows = []
    blank_amounts = 0
    missing_phones = 0
    for row in unique_rows:
        amount = clean_amount(row.get("Amount", ""))
        if amount is None:
            blank_amounts += 1
            log.append(
                f"Dropped - no amount: {row.get('Date','')} "
                f"{row.get('Customer','')} - {row.get('Service','')}"
            )
            continue

        phone = (row.get("Phone", "") or "").replace(" ", "").strip()
        if not phone:
            missing_phones += 1

        service = SERVICE_MAP.get(
            (row.get("Service", "") or "").strip().lower(),
            (row.get("Service", "") or "").strip().title(),
        )

        clean_rows.append(
            {
                "Date": clean_date(row.get("Date", "")),
                "Customer": (row.get("Customer", "") or "").strip(),
                "Phone": phone,
                "Service": service,
                "Amount": f"{amount:.2f}",
                "Payment_Mode": clean_payment(row.get("Payment_Mode", "")),
            }
        )

    # Sort by date, then customer, so the clean file is easy to read
    clean_rows.sort(key=lambda r: (r["Date"], r["Customer"]))

    total_clean = len(clean_rows)
    log.append(f"Rows dropped - blank amount: {blank_amounts}")
    log.append(f"Rows with missing phone (kept): {missing_phones}")
    log.append(f"Rows in clean file: {total_clean}")

    total_amount = sum(float(r["Amount"]) for r in clean_rows)
    log.append(f"Total amount in clean file: Rs {total_amount:,.2f}")
    log.append("")

    # 3. Write the clean file
    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CLEAN_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Date", "Customer", "Phone", "Service", "Amount", "Payment_Mode"]
        )
        writer.writeheader()
        writer.writerows(clean_rows)

    # 4. Monthly summary by service
    by_service = defaultdict(lambda: {"count": 0, "total": 0.0})
    for row in clean_rows:
        by_service[row["Service"]]["count"] += 1
        by_service[row["Service"]]["total"] += float(row["Amount"])

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Service", "Bookings", "Total_Amount_Rs"])
        for service in sorted(by_service):
            data = by_service[service]
            writer.writerow([service, data["count"], f"{data['total']:.2f}"])
        writer.writerow(["TOTAL", total_clean, f"{total_amount:.2f}"])

    # 5. Small counts for the log, by service and by payment
    log.append("Bookings by service:")
    for service in sorted(by_service):
        data = by_service[service]
        log.append(f"  {service}: {data['count']} bookings, Rs {data['total']:,.2f}")
    log.append("")
    log.append("Bookings by payment mode:")
    for mode, count in sorted(Counter(r["Payment_Mode"] for r in clean_rows).items()):
        log.append(f"  {mode}: {count}")
    log.append("")

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text("\n".join(log), encoding="utf-8")

    print(f"Raw rows: {total_raw}")
    print(f"Duplicates removed: {duplicates}")
    print(f"Blank amounts dropped: {blank_amounts}")
    print(f"Clean rows: {total_clean}")
    print(f"Total: Rs {total_amount:,.2f}")
    print(f"Wrote: {CLEAN_FILE}")
    print(f"Wrote: {SUMMARY_FILE}")
    print(f"Wrote: {LOG_FILE}")


if __name__ == "__main__":
    main()
