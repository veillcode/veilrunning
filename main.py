from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.activities import router as activities_router
from app.routers.analytics import router as analytics_router
from app.routers.training_plan import router as training_plan_router
from app.routers.community import router as community_router
from app.routers.ai_coach import router as ai_coach_router
from app.routers.devices import router as devices_router

app = FastAPI(
    title="PACE API",
    description="Backend API untuk aplikasi lari premium PACE",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,          prefix="/api/v1/auth",          tags=["Auth"])
app.include_router(users_router,         prefix="/api/v1/users",         tags=["Users"])
app.include_router(activities_router,    prefix="/api/v1/activities",    tags=["Activities"])
app.include_router(analytics_router,     prefix="/api/v1/analytics",     tags=["Analytics"])
app.include_router(training_plan_router, prefix="/api/v1/training-plan", tags=["Training Plan"])
app.include_router(community_router,     prefix="/api/v1/community",     tags=["Community"])
app.include_router(ai_coach_router,      prefix="/api/v1/ai-coach",      tags=["AI Coach"])
app.include_router(devices_router,       prefix="/api/v1/devices",       tags=["Devices"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "PACE API is running 🏃", "version": "1.0.0"}

@app.get("/health", tags=["Root"])
async def health_check():
    return {"status": "healthy"}

if os.path.exists("index.html"):
    app.mount("/app", StaticFiles(directory=".", html=True), name="static")