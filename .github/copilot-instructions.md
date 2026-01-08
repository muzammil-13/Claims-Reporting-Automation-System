# AI Agent Instructions for Claims Reporting Automation System

## Project Overview

FastAPI backend for a cloud-native claims processing pipeline: file upload → CSV parsing → Excel/PDF report generation → Google Cloud Storage upload → database metadata storage. Mock data only (production-safe).

## Core Architecture & Data Flow

### Service Boundaries

- **API Layer** ([app/api/reports.py](app/api/reports.py)): File upload validation, request routing, response assembly
- **Excel/PDF Generator** ([app/services/excel_generator.py](app/services/excel_generator.py)): DataFrame aggregation (groupby status/amount), multi-sheet workbooks (Summary + Details), PDF canvas rendering
- **Cloud Storage** ([app/services/storage.py](app/services/storage.py)): GCS bucket uploads with public URLs, requires `GCP_BUCKET_NAME` env var
- **Database** ([app/db/](app/db/)): SQLAlchemy ORM with Report model (id, filename, gcs_url, status, created_at)

### Data Processing Pattern

```
UploadFile (CSV bytes) 
→ pandas.read_csv() 
→ DataFrame groupby aggregation 
→ openpyxl Workbook creation (2 sheets) + reportlab PDF canvas 
→ tempfile Path objects 
→ GCS blob.upload_from_filename() 
→ Report DB record with GCS URL
```

## Critical Developer Workflows

### Local Development & Debugging

```bash
pip install -r requirements.txt
# Run with SQLite default (no database setup needed for initial testing)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- Health endpoint: `GET /health` returns `{"status": "ok"}`
- Upload endpoint: `POST /reports/upload` (multipart form data)
- Requires: Valid CSV/TXT file with "Status" and "Amount" columns (see sample_data/)

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (defaults to SQLite: `sqlite:///./claims.db`)
- `GCP_BUCKET_NAME`: Required for upload_file() to work; raises RuntimeError if missing
- Load from `.env` file via `python-dotenv` (see SETUP_ENV.md)

### Dependency Notes

- **pandas**: DataFrame creation/groupby operations (2.2.2)
- **openpyxl**: Workbook multi-sheet creation with styling (3.1.2)
- **reportlab**: PDF canvas rendering (4.1.0)
- **SQLAlchemy**: ORM with sessionmaker pattern for DB access (2.0.30)
- **google-cloud-storage**: GCS client auth via ADC (Application Default Credentials)

## Project-Specific Patterns & Conventions

### File Validation

- Accept .csv, .txt extensions + specific content types (text/csv, text/plain, application/vnd.ms-excel)
- Extension check first (case-insensitive), fallback to content-type validation
- Reject ambiguous uploads (no extension + no content-type)

### Report Generation

- Summary aggregation: `df.groupby("Status", as_index=False)["Amount"].sum()`
- Excel output: 2 worksheets named "Summary" and "Details" with formatted headers (bold, centered)
- PDF output: reportlab canvas at LETTER pagesize, manual text positioning (inch-based coordinates)
- All outputs use `tempfile` for temp storage before GCS upload

### Database Session Pattern

- Use `get_db()` dependency in FastAPI endpoints to get Session
- Session yields via context manager; always closes in finally block
- No explicit transaction management; autocommit=False, autoflush=False

### Storage Blob Naming

- Pattern: `reports/{uuid4()}_{original_filename}` for organized GCS bucket structure
- `blob.make_public()` enables direct URL sharing

## Integration Points & Cross-Component Communication

### Request → Report Generation Flow

1. [reports.py](app/api/reports.py) validates file, reads bytes
2. Calls `excel_generator.generate_reports(csv_bytes)` → returns (summary_df, excel_Path, pdf_Path)
3. Uploads via `storage.upload_file(file_path, gcs_blob_name)` → gets public URL
4. Creates Report ORM record with gcs_url, commits to DB
5. Returns JSON with id, filename, excel_url, pdf_url, summary dict

### Mock Data Structure

- [sample_data/claims_export_2025.txt](sample_data/claims_export_2025.txt): CSV format with Status and Amount columns for testing
- Use for manual testing or fixtures if adding tests

## Common Implementation Tasks

### Adding a New Report Field

1. Update Report model in [app/models/report.py](app/models/report.py) with new Column
2. Update [app/api/reports.py](app/api/reports.py) response dict to include field
3. Migration: SQLite auto-creates; PostgreSQL requires Alembic migration (not yet in project)

### Extending Report Formatting

- Excel: Add worksheets via `wb.create_sheet(name)` in [excel_generator.py](app/services/excel_generator.py)
- PDF: Extend canvas drawing after line 48 (current y-position tracking pattern)

### Debugging File Upload Issues

- Check content-type and extension in allowed lists (line 16-28 of [reports.py](app/api/reports.py))
- Verify CSV has Status and Amount columns (groupby will KeyError otherwise)
- Test with sample_data/claims_export_2025.txt
