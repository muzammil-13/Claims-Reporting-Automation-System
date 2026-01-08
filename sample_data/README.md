# Sample Mock Data

This directory contains sample/mock claims data files for testing the Claims Reporting Automation System.

## File Format

All CSV files must contain the following columns:
- `ClaimID`: Unique identifier for the claim
- `Status`: Claim status (e.g., Paid, Denied, Pending)
- `Amount`: Claim amount (numeric)
- `Date`: Claim date (YYYY-MM-DD format)
- `Type`: Claim type (e.g., Medical, Dental, Vision)

## Example File

`claims_export_2025.txt` - Sample claims data with 15 records

## Usage

You can upload these files via the API endpoint:
```
POST /reports/upload
```

Or test locally using curl:
```bash
curl -X POST "http://localhost:8000/reports/upload" \
  -F "file=@sample_data/claims_export_2025.txt"
```

## Notes

- Files can be `.csv` or `.txt` format
- The API accepts CSV files with the required columns
- Dates should be in YYYY-MM-DD format
- Amounts should be numeric values
