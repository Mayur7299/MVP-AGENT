from fastapi import APIRouter, HTTPException
from models.schemas import ResearchQuery, ReportData
from services.research_service import create_research_job, list_reports, get_report, delete_report

router = APIRouter()


@router.post("/", response_model=ReportData)
async def run_research(query: ResearchQuery):
    """Submit a research query and generate a market intelligence report."""
    report = await create_research_job(
        query=query.query,
        sector=query.sector,
        region=query.region,
        company_size=query.company_size,
        depth=query.depth or "standard"
    )
    return report


@router.get("/", response_model=list)
def get_all_reports():
    """List all research reports."""
    return list_reports()


@router.get("/{report_id}", response_model=ReportData)
def get_single_report(report_id: str):
    """Get a specific report by ID."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.delete("/{report_id}")
def remove_report(report_id: str):
    """Delete a report."""
    success = delete_report(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Report deleted successfully"}
