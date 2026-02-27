from dotenv import load_dotenv
import os
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import research, reports, export
print("LOADED KEY:", os.getenv("GEMINI_API_KEY"))
app = FastAPI(
    title="CIAgent API",
    description="AI-powered market intelligence and business decision-support system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research.router, prefix="/api/research", tags=["Research"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])

@app.get("/")
def root():
    return {"status": "CIAgent API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
