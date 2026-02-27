from fastapi import APIRouter, HTTPException
from models.schemas import ReportData
from services.research_service import get_report, list_reports

router = APIRouter()


@router.get("/", response_model=list)
def get_reports():
    """Get all reports summary list."""
    return list_reports()


@router.get("/{report_id}", response_model=ReportData)
def get_report_detail(report_id: str):
    """Get full report details."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
