from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from services.research_service import get_report
from services.export_service import export_to_json, export_to_text

router = APIRouter()


@router.get("/{report_id}/json")
def export_json(report_id: str):
    """Export report as JSON file."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    data = export_to_json(report)
    return Response(
        content=data,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=ciagent_report_{report_id[:8]}.json"}
    )


@router.get("/{report_id}/text")
def export_text(report_id: str):
    """Export report as plain text/markdown."""
    report = get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    data = export_to_text(report)
    return Response(
        content=data,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=ciagent_report_{report_id[:8]}.md"}
    )
