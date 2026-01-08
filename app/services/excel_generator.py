import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def _build_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate totals by status."""
    summary = df.groupby("Status", as_index=False)["Amount"].sum()
    summary = summary.rename(columns={"Amount": "TotalAmount"})
    return summary


def _write_excel(df: pd.DataFrame, summary: pd.DataFrame, output_path: Path) -> Path:
    wb = Workbook()

    # Summary sheet
    ws_summary = wb.active
    ws_summary.title = "Summary"
    ws_summary.append(["Status", "Total Amount"])
    for _, row in summary.iterrows():
        ws_summary.append([row["Status"], float(row["TotalAmount"])])
    ws_summary["A1"].font = Font(bold=True)
    ws_summary["B1"].font = Font(bold=True)
    for col in ("A", "B"):
        ws_summary[f"{col}1"].alignment = Alignment(horizontal="center")

    # Detail sheet
    ws_detail = wb.create_sheet("Details")
    ws_detail.append(df.columns.tolist())
    for row in df.itertuples(index=False):
        ws_detail.append(list(row))
    for cell in ws_detail[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    wb.save(output_path)
    return output_path


def _write_pdf(summary: pd.DataFrame, output_path: Path) -> Path:
    c = canvas.Canvas(str(output_path), pagesize=LETTER)
    width, height = LETTER
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 1 * inch, "Claims Totals by Status")
    c.setFont("Helvetica", 12)

    y = height - 1.5 * inch
    c.drawString(1 * inch, y, "Status")
    c.drawString(3 * inch, y, "Total Amount")
    y -= 0.3 * inch

    for _, row in summary.iterrows():
        c.drawString(1 * inch, y, str(row["Status"]))
        c.drawString(3 * inch, y, f"{float(row['TotalAmount']):,.2f}")
        y -= 0.25 * inch
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch

    c.showPage()
    c.save()
    return output_path


def generate_reports(csv_bytes: bytes) -> Tuple[Dict[str, float], Path, Path]:
    """
    Accept CSV bytes, compute totals by status, generate Excel and PDF.

    Returns:
        summary_dict: mapping of status to totals
        excel_path: path to generated Excel file
        pdf_path: path to generated PDF file
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        df = pd.read_csv(pd.io.common.BytesIO(csv_bytes))
        required_cols = {"ClaimID", "Status", "Amount", "Date", "Type"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        summary = _build_summary(df)

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        excel_path = tmpdir_path / f"claims_report_{timestamp}.xlsx"
        pdf_path = tmpdir_path / f"claims_report_{timestamp}.pdf"

        _write_excel(df, summary, excel_path)
        _write_pdf(summary, pdf_path)

        summary_dict = {row["Status"]: float(row["TotalAmount"]) for _, row in summary.iterrows()}

        # Move files out of the temporary directory scope
        final_excel = Path(tempfile.mkstemp(suffix=".xlsx")[1])
        final_pdf = Path(tempfile.mkstemp(suffix=".pdf")[1])
        excel_path.replace(final_excel)
        pdf_path.replace(final_pdf)

        return summary_dict, final_excel, final_pdf
