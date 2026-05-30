"""
PACE — Premium Running App
Backend API (FastAPI)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import langsung karena struktur flat
from auth import router as auth_router
from users import router as users_router
from activities import router as activities_router
from analytics import router as analytics_router
from training_plan import router as training_plan_router
from community import router as community_router
from ai_coach import router as ai_coach_router
from devices import router as devices_router

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
app.include_router(auth_router,          prefix="/api/v1/auth",          tags=["Auth"])
app.include_router(users_router,         prefix="/api/v1/users",         tags=["Users"])
app.include_router(activities_router,    prefix="/api/v1/activities",    tags=["Activities"])
app.include_router(analytics_router,     prefix="/api/v1/analytics",     tags=["Analytics"])
app.include_router(training_plan_router, prefix="/api/v1/training-plan", tags=["Training Plan"])
app.include_router(community_router,     prefix="/api/v1/community",     tags=["Community"])
app.include_router(ai_coach_router,      prefix="/api/v1/ai-coach",      tags=["AI Coach"])
app.include_router(devices_router,       prefix="/api/v1/devices",       tags=["Devices"])

# ── ROOT ENDPOINTS ────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {"message": "PACE API is running 🏃", "version": "1.0.0"}

@app.get("/health", tags=["Root"])
async def health_check():
    return {"status": "healthy"}

# ── SERVE FRONTEND ───────────────────────────────
if os.path.exists("index.html"):
    app.mount("/app", StaticFiles(directory=".", html=True), name="static")