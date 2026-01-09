import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.report import Report
from app.services import excel_generator, ml_service, storage

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Check file extension and content type
    allowed_content_types = (
        "text/csv",
        "application/vnd.ms-excel",
        "text/plain",
        "application/octet-stream",
    )
    allowed_extensions = (".csv", ".txt")
    
    # Validate file - check extension first, then content type
    is_valid = False
    if file.filename:
        # Check if file has a valid extension
        file_lower = file.filename.lower()
        is_valid = file_lower.endswith(allowed_extensions)
    
    # If extension check failed, check content type
    if not is_valid:
        if file.content_type:
            is_valid = file.content_type in allowed_content_types
        else:
            # If no content type provided, reject
            is_valid = False
    
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=f"File must be a CSV (.csv or .txt). Received: content_type={file.content_type}, filename={file.filename}",
        )

    csv_bytes = await file.read()
    try:
        summary, excel_path, pdf_path = excel_generator.generate_reports(csv_bytes)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    excel_blob_name = f"reports/{uuid.uuid4()}_{excel_path.name}"
    pdf_blob_name = f"reports/{uuid.uuid4()}_{pdf_path.name}"

    excel_url = storage.upload_file(excel_path, excel_blob_name)
    pdf_url = storage.upload_file(pdf_path, pdf_blob_name)

    report_record = Report(
        filename=file.filename,
        gcs_url=excel_url,
        status="processed",
    )
    db.add(report_record)
    db.commit()
    db.refresh(report_record)

    return {
        "id": report_record.id,
        "filename": report_record.filename,
        "excel_url": excel_url,
        "pdf_url": pdf_url,
        "summary": summary,
    }


@router.post("/predict")
async def predict_claims(file: UploadFile = File(...)):
    """
    Predict outcomes for pending claims using ML model.
    
    Accepts a CSV file with claims data and returns predictions
    for claims with 'Pending' status.
    """
    # Validate file type
    allowed_content_types = (
        "text/csv",
        "application/vnd.ms-excel",
        "text/plain",
        "application/octet-stream",
    )
    allowed_extensions = (".csv", ".txt")
    
    is_valid = False
    if file.filename:
        file_lower = file.filename.lower()
        is_valid = file_lower.endswith(allowed_extensions)
    
    if not is_valid:
        if file.content_type:
            is_valid = file.content_type in allowed_content_types
        else:
            is_valid = False
    
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=f"File must be a CSV (.csv or .txt). Received: content_type={file.content_type}, filename={file.filename}",
        )
    
    # Read file content
    csv_bytes = await file.read()
    
    if len(csv_bytes) == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    
    try:
        # Run ML prediction
        result = ml_service.predict_claims_from_bytes(csv_bytes)
        return {
            "filename": file.filename,
            "success": True,
            **result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}",
        ) from e


@router.get("")
def list_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "gcs_url": r.gcs_url,
            "status": r.status,
            "created_at": r.created_at,
        }
        for r in reports
    ]
