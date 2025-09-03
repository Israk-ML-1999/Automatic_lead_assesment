# FastAPI app + /run endpoint

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from app.pipeline import run_pipeline

app = FastAPI(title="AI Sales Campaign CRM — MVP (Groq)")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(file: str = "data/leads.csv", batch_size: int = 10, max_concurrent_batches: int = 5):
    stats = run_pipeline(file, batch_size=batch_size, max_concurrent_batches=max_concurrent_batches)
    return JSONResponse({"message": "pipeline completed", "stats": stats})

@app.get("/report/latest")
def report_latest():
    reports = sorted(Path("reports").glob("report-*.md"), reverse=True)
    if not reports:
        return JSONResponse({"error": "no reports yet"}, status_code=404)
    return FileResponse(reports[0])
