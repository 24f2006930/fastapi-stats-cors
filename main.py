import os
import time
import uuid
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = os.getenv("STUDENT_EMAIL", "24f2006930@ds.study.iitm.ac.in")
ALLOWED_ORIGIN = "https://dash-idl1i0.example.com"

app = FastAPI(title="Stats API")

# Only this exact origin is allowed. Starlette's CORSMiddleware responds to
# allowed preflights and omits ACAO for disallowed origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_metadata(request: Request, call_next):
    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        # Return a response here so the required headers are applied to it too.
        elapsed = max(0.0, time.perf_counter() - started)
        response = JSONResponse(status_code=500, content={"detail": "Internal server error"})
    elapsed = max(0.0, time.perf_counter() - started)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/stats")
async def stats(values: Annotated[str, Query(description="Comma-separated integers")]):
    try:
        numbers = [int(part.strip()) for part in values.split(",")]
        if not numbers or any(part.strip() == "" for part in values.split(",")):
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be a comma-separated list of integers")

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }


@app.get("/")
async def root():
    return {"status": "ok", "endpoint": "/stats?values=1,2,3"}
