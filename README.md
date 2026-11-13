# Excel automation — messy bookings to a clean monthly report

Hi, I'm Bhavya. I clean messy Excel / CSV files and turn them into a report you can actually use.

This one is a sample. I made it for a fictional car care business in Anand, called Shree Car Care. All the names, phones and amounts here are sample data. No real customers.

## The problem

The bookings sheet was a mess. Dates were in two formats. The same service was typed in three different ways. Some amounts had ₹ and commas, some didn't. A few rows were copied twice. And 3 rows had no amount at all.

If you tried to total that sheet in Excel, you'd get the wrong answer. Or you'd spend an hour fixing it by hand every month.

## What I did

I wrote a small Python script. It reads the messy file, cleans it, and gives you two things back.

1. A clean bookings file
2. A monthly summary by service

It runs in seconds. You just put your new messy file in the same place and run it again next month.

## Before / after

Before:
- 25 rows in `data/raw_bookings_messy.csv`
- Dates like `02/10/2026` and `2026-10-03` mixed together
- "Ceramic Coating", "ceramic coating" and "Ceramic coat" all meant the same thing
- Amounts like `₹12,500`, `12500` and `12,500`
- Cash / cash / CASH, same for UPI and Card
- 2 duplicate rows, 3 rows with no amount

After:
- 20 clean rows in `data/clean_bookings.csv`
- All dates as `YYYY-MM-DD`
- One spelling for each service
- All amounts as plain numbers, like `12500.00`
- Payment as Cash, UPI or Card only
- Total for October 2026: **Rs 1,58,989**

The summary is in `output/monthly_report_summary.csv`. Ceramic Coating was the biggest part — 7 bookings, Rs 87,000.

## How to run it

You need Python 3. That's it. No extra packages.

```bash
python3 clean_monthly_report.py
```

It reads `data/raw_bookings_messy.csv` and writes:
- `data/clean_bookings.csv`
- `output/monthly_report_summary.csv`
- `output/cleaning_log.txt`

The log tells you what was removed and why. Nothing is deleted silently.

## Files

- `clean_monthly_report.py` — the script, plain Python, only the built-in csv module
- `data/raw_bookings_messy.csv` — the messy input, sample data
- `data/clean_bookings.csv` — the clean output
- `output/monthly_report_summary.csv` — bookings and total by service
- `output/cleaning_log.txt` — what was changed
- `docs/what_changed.md` — every cleaning rule, with row counts

## What this is good for

Any service business that keeps bookings in Excel. Car care, salons, clinics, shops. Same story everywhere. Messy sheet in, clean report out.

If your sheet has different columns or different service names, I can change the script for your file. The idea stays the same.
