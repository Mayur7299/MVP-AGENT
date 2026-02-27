from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ReportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchQuery(BaseModel):
    query: str = Field(..., min_length=10, description="Business research query")
    sector: Optional[str] = Field(None, description="Industry sector")
    region: Optional[str] = Field(None, description="Target region/market")
    company_size: Optional[str] = Field(None, description="Target company size (MSME/Startup/Enterprise)")
    depth: Optional[str] = Field("standard", description="Research depth: quick | standard | deep")


class MarketSignal(BaseModel):
    title: str
    source: str
    summary: str
    relevance_score: float
    timestamp: str


class CompetitorInsight(BaseModel):
    name: str
    market_position: str
    strengths: List[str]
    weaknesses: List[str]
    estimated_market_share: Optional[str]


class MarketSection(BaseModel):
    market_size: str
    growth_rate: str
    key_trends: List[str]
    target_segments: List[str]
    geographic_focus: str


class RecommendationItem(BaseModel):
    priority: str  # high | medium | low
    action: str
    rationale: str
    timeline: str


class ReportData(BaseModel):
    report_id: str
    query: str
    sector: Optional[str]
    region: Optional[str]
    status: ReportStatus
    created_at: str
    completed_at: Optional[str]

    # Report sections
    executive_summary: Optional[str]
    market_overview: Optional[MarketSection]
    competitors: Optional[List[CompetitorInsight]]
    signals: Optional[List[MarketSignal]]
    recommendations: Optional[List[RecommendationItem]]
    risk_factors: Optional[List[str]] = []
    opportunities: Optional[List[str]] = []
    conclusion: Optional[str] = ""


class ReportListItem(BaseModel):
    report_id: str
    query: str
    sector: Optional[str]
    status: ReportStatus
    created_at: str


class GenerateReportRequest(BaseModel):
    query_id: str
