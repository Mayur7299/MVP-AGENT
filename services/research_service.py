import uuid
from datetime import datetime, timezone
from typing import Optional, List

from models.schemas import (
    ReportData,
    ReportStatus,
    ReportListItem,
    MarketSection,
    CompetitorInsight,
    MarketSignal,
    RecommendationItem,
)

from ai_engine.claude_engine import generate_market_report


_reports_store: dict[str, ReportData] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def create_research_job(
    query: str,
    sector: Optional[str],
    region: Optional[str],
    company_size: Optional[str],
    depth: str
) -> ReportData:

    report_id = str(uuid.uuid4())

    report = ReportData(
        report_id=report_id,
        query=query,
        sector=sector,
        region=region,
        company_size=company_size,
        status=ReportStatus.PROCESSING,
        created_at=_now_iso(),
        completed_at=None,
        executive_summary="",
        market_overview=None,
        competitors=[],
        signals=[],
        recommendations=[],
        risk_factors=[],
        opportunities=[],
        conclusion=""
    )

    _reports_store[report_id] = report

    try:
        ai_data = await generate_market_report(
            query=query,
            sector=sector,
            region=region,
            depth=depth
        )

        # Basic fields
        report.executive_summary = ai_data.get("executive_summary", "")
        report.conclusion = ai_data.get("conclusion", "")
        report.risk_factors = ai_data.get("risk_factors", [])
        report.opportunities = ai_data.get("opportunities", [])

        # Market Overview (safe mapping)
        market_overview_raw = ai_data.get("market_overview")
        if isinstance(market_overview_raw, dict):
            report.market_overview = MarketSection(**market_overview_raw)

        # Competitors (defensive mapping)
        competitors_raw = ai_data.get("competitors", [])
        safe_competitors = []

        for c in competitors_raw:
            if isinstance(c, dict):
                safe_competitors.append(CompetitorInsight(**c))
            else:
                safe_competitors.append(
                    CompetitorInsight(
                        name=str(c),
                        market_position="Unknown",
                        strengths=[],
                        weaknesses=[],
                        estimated_market_share="Unknown"
                    )
                )

        report.competitors = safe_competitors

        # Signals (defensive mapping)
        signals_raw = ai_data.get("signals", [])
        safe_signals = []

        for s in signals_raw:
            if isinstance(s, dict):
                safe_signals.append(MarketSignal(**s))
            else:
                safe_signals.append(
                    MarketSignal(
                        title=str(s),
                        source="AI Generated",
                        summary=str(s),
                        relevance_score=0.5,
                        timestamp="N/A"
                    )
                )

        report.signals = safe_signals

        # Recommendations (defensive mapping)
        recs_raw = ai_data.get("recommendations", [])
        safe_recommendations = []

        for r in recs_raw:
            if isinstance(r, dict):
                safe_recommendations.append(RecommendationItem(**r))
            else:
                safe_recommendations.append(
                    RecommendationItem(
                        priority="medium",
                        action=str(r),
                        rationale="AI generated suggestion",
                        timeline="3-6 months"
                    )
                )

        report.recommendations = safe_recommendations

        report.status = ReportStatus.COMPLETED
        report.completed_at = _now_iso()

    except Exception as e:
        report.status = ReportStatus.FAILED
        report.executive_summary = f"Report generation failed: {str(e)}"

    _reports_store[report_id] = report
    return report


def get_report(report_id: str) -> Optional[ReportData]:
    return _reports_store.get(report_id)


def list_reports() -> List[ReportListItem]:
    return [
        ReportListItem(
            report_id=r.report_id,
            query=r.query,
            sector=r.sector,
            status=r.status,
            created_at=r.created_at
        )
        for r in sorted(
            _reports_store.values(),
            key=lambda x: x.created_at,
            reverse=True
        )
    ]


def delete_report(report_id: str) -> bool:
    if report_id in _reports_store:
        del _reports_store[report_id]
        return True
    return False