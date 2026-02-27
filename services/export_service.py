import json
from models.schemas import ReportData
from io import BytesIO


def export_to_json(report: ReportData) -> bytes:
    """Export report as formatted JSON bytes."""
    data = report.model_dump(mode="json")
    return json.dumps(data, indent=2).encode("utf-8")


def export_to_text(report: ReportData) -> str:
    """Export report as plain text (markdown-style)."""
    lines = []

    lines.append(f"# CIAGENT MARKET INTELLIGENCE REPORT")
    lines.append(f"## Query: {report.query}")
    if report.sector:
        lines.append(f"**Sector:** {report.sector}")
    if report.region:
        lines.append(f"**Region:** {report.region}")
    lines.append(f"**Generated:** {report.completed_at or report.created_at}")
    lines.append("")

    if report.executive_summary:
        lines.append("## Executive Summary")
        lines.append(report.executive_summary)
        lines.append("")

    if report.market_overview:
        mo = report.market_overview
        lines.append("## Market Overview")
        lines.append(f"- **Market Size:** {mo.market_size}")
        lines.append(f"- **Growth Rate:** {mo.growth_rate}")
        lines.append(f"- **Geographic Focus:** {mo.geographic_focus}")
        lines.append(f"\n**Key Trends:**")
        for t in mo.key_trends:
            lines.append(f"  - {t}")
        lines.append(f"\n**Target Segments:**")
        for s in mo.target_segments:
            lines.append(f"  - {s}")
        lines.append("")

    if report.competitors:
        lines.append("## Competitive Landscape")
        for c in report.competitors:
            lines.append(f"\n### {c.name} ({c.market_position})")
            if c.estimated_market_share:
                lines.append(f"Market Share: {c.estimated_market_share}")
            lines.append(f"Strengths: {', '.join(c.strengths)}")
            lines.append(f"Weaknesses: {', '.join(c.weaknesses)}")
        lines.append("")

    if report.recommendations:
        lines.append("## Recommendations")
        for i, r in enumerate(report.recommendations, 1):
            lines.append(f"\n{i}. [{r.priority.upper()}] {r.action}")
            lines.append(f"   Rationale: {r.rationale}")
            lines.append(f"   Timeline: {r.timeline}")
        lines.append("")

    if report.risk_factors:
        lines.append("## Risk Factors")
        for risk in report.risk_factors:
            lines.append(f"- {risk}")
        lines.append("")

    if report.opportunities:
        lines.append("## Opportunities")
        for opp in report.opportunities:
            lines.append(f"- {opp}")
        lines.append("")

    if report.conclusion:
        lines.append("## Conclusion")
        lines.append(report.conclusion)

    return "\n".join(lines)
