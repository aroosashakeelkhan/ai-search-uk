# app/main.py
from app.db import init_db, search, count
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


app = FastAPI(title="AI Search UK — MVP", version="0.1.0")


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search_endpoint(q: str = Query(..., min_length=2), limit: int = 5, offset: int = 0):
    results = search(q, limit, offset)
    total = count(q)
    return JSONResponse({"query": q, "total": total, "results": results})
