"""
PACE — Premium Running App
Backend API (FastAPI)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from app.routers import (
    auth,
    users,
    activities,
    analytics,
    training_plan,
    community,
    ai_coach,
    devices,
)

app = FastAPI(
    title="PACE API",
    description="Backend API untuk aplikasi lari premium PACE",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROUTERS ───────────────────────────────────────────────────
app.include_router(auth.router,          prefix="/api/v1/auth",          tags=["Auth"])
app.include_router(users.router,         prefix="/api/v1/users",         tags=["Users"])
app.include_router(activities.router,    prefix="/api/v1/activities",    tags=["Activities"])
app.include_router(analytics.router,     prefix="/api/v1/analytics",     tags=["Analytics"])
app.include_router(training_plan.router, prefix="/api/v1/training-plan", tags=["Training Plan"])
app.include_router(community.router,     prefix="/api/v1/community",     tags=["Community"])
app.include_router(ai_coach.router,      prefix="/api/v1/ai-coach",      tags=["AI Coach"])
app.include_router(devices.router,       prefix="/api/v1/devices",       tags=["Devices"])

# ── ROOT ENDPOINTS ────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {"message": "PACE API is running 🏃", "version": "1.0.0"}

@app.get("/health", tags=["Root"])
async def health_check():
    return {"status": "healthy"}

# ── SERVE FRONTEND (index.html) ───────────────────────────────
# Taruh index.html di folder yang sama dengan main.py
# Lalu akses via http://localhost:8000/app/index.html
if os.path.exists("index.html"):
    app.mount("/app", StaticFiles(directory=".", html=True), name="static")