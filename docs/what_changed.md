# What changed — Shree Car Care, Anand (sample data)

All data in this project is sample data.

## Row counts

- Rows in raw file: 25
- Exact duplicate rows removed: 2
- Rows dropped — blank amount: 3
- Rows in clean file: 20
- Total amount in clean file: Rs 1,58,989.00

25 − 2 − 3 = 20. That matches the clean file.

## Cleaning rules, in order

### 1. Remove exact duplicates
Rule: if a row is an exact copy of an earlier row, keep the first copy, drop the rest.
Removed: 2 rows
- Both were the 04/10/2026 Kiran Patel — Interior Detailing — ₹3,499 — Card row, copied twice.

### 2. Fix dates
Rule: read DD/MM/YYYY and YYYY-MM-DD, write everything as YYYY-MM-DD.
Changed: all 20 clean rows now use YYYY-MM-DD.
No rows were dropped for a bad date. All dates in the raw file were in one of those two formats.

### 3. Fix service names
Rule: map every spelling to one standard name.
- "Ceramic Coating", "ceramic coating", "Ceramic coat" → Ceramic Coating
- "Car Wash", "Car wash", "car wash" → Car Wash
- "Interior Detailing", "Interior Detaling" (typo) → Interior Detailing
- "Exterior Polish", "Exterior polish" → Exterior Polish
- "Paint Protection Film", "Paint protection film" → Paint Protection Film

Result in the clean file:
- Ceramic Coating: 7 bookings, Rs 87,000.00
- Car Wash: 4 bookings, Rs 1,996.00
- Interior Detailing: 4 bookings, Rs 13,996.00
- Exterior Polish: 3 bookings, Rs 5,997.00
- Paint Protection Film: 2 bookings, Rs 50,000.00

### 4. Fix amounts
Rule: strip ₹, Rs and commas, turn the rest into a number with 2 decimals.
Examples from the raw file: `₹12,500` → `12500.00`, `1,999` → `1999.00`, `12500` → `12500.00`.

### 5. Drop rows with no amount
Rule: if the amount is blank, drop the row and write it in the log. Don't guess an amount.
Dropped: 3 rows
- 08/10/2026, Rahul Gupta, Car Wash
- 14/10/2026, Priya Nair, Ceramic coat
- 16/10/2026, Rahul Gupta, Car wash

These 3 are listed in `output/cleaning_log.txt`.

### 6. Fix payment modes
Rule: map any case to one of Cash, UPI or Card.
- "Cash", "cash", "CASH" → Cash
- "UPI", "upi" → UPI
- "Card", "card", "CARD" → Card

Result in the clean file:
- Cash: 9 bookings
- UPI: 7 bookings
- Card: 4 bookings

### 7. Fix phones
Rule: remove spaces from phone numbers. Keep the row even if the phone is missing.
- Rows with a missing phone, kept: 3
  - 03/10/2026, Rohit Desai, Car Wash
  - 08/10/2026, Anjali Mehta, Ceramic Coating
  - 13/10/2026, Sneha Joshi, Paint Protection Film
- No phone numbers were guessed or filled in.

### 8. Sort the clean file
Rule: sort by date, then by customer name.
This is only to make the clean file easy to read. It does not change any totals.

## Outputs

- `data/clean_bookings.csv` — 20 rows, clean
- `output/monthly_report_summary.csv` — 5 services + a TOTAL row, 20 bookings, Rs 1,58,989.00
- `output/cleaning_log.txt` — the same counts and the 3 dropped rows, written by the script
