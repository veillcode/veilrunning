"""
PACE — Activities Router
GET  /api/v1/activities/
POST /api/v1/activities/
GET  /api/v1/activities/{activity_id}
GET  /api/v1/activities/live/{user_id}
"""
from fastapi import APIRouter, Query, HTTPException
from app.schemas.pace_schemas import Activity, ActivityCreate, LiveRunData
from app.models.database import activities_db, users_db, weekly_progress_db, live_run_db
from app.services.helpers import calculate_pace, format_pace, format_duration
from datetime import datetime
from typing import List
import random
import uuid

router = APIRouter()


@router.get("/", response_model=List[Activity])
async def list_activities(
    user_id: str = Query(default="user_alex"),
    limit: int = Query(default=20, le=100),
):
    acts = [a for a in activities_db if a["user_id"] == user_id]
    return [Activity(**a) for a in acts[:limit]]


@router.post("/", response_model=Activity, status_code=201)
async def create_activity(
    body: ActivityCreate,
    user_id: str = Query(default="user_alex"),
):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    pace = calculate_pace(body.duration_seconds, body.distance_km)
    cal = body.calories or round(body.distance_km * 62)
    act = {
        "id": f"act_{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "type": body.type,
        "name": body.name,
        "date": datetime.now().strftime("%d %b %Y"),
        "distance_km": body.distance_km,
        "duration_seconds": body.duration_seconds,
        "avg_pace_sec_per_km": pace,
        "avg_hr": body.avg_hr,
        "calories": cal,
        "elevation_m": body.elevation_m,
    }
    activities_db.insert(0, act)

    # Update weekly progress
    wp = weekly_progress_db.get(user_id)
    if wp and body.type == "run":
        wp["total_km"] = round(wp["total_km"] + body.distance_km, 1)
        wp["total_time_min"] += body.duration_seconds // 60
        wp["runs"] += 1
        today_idx = datetime.now().weekday()  # 0=Mon
        wp["days"][today_idx] = round(wp["days"][today_idx] + body.distance_km, 1)

    users_db[user_id]["total_activities"] = users_db[user_id].get("total_activities", 0) + 1

    return Activity(**act)


@router.get("/live/{user_id}", response_model=LiveRunData)
async def get_live_run(user_id: str):
    """Polling endpoint — returns simulated live run data."""
    state = live_run_db.get(user_id, {
        "seconds": 0, "distance_km": 0.0, "hr": 150, "calories": 0, "status": "idle"
    })
    # Simulate increments if running
    if state.get("status") == "running":
        state["seconds"] += 5
        state["distance_km"] = round(state["distance_km"] + 0.015, 3)
        state["hr"] = min(178, max(140, state["hr"] + random.randint(-2, 3)))
        state["calories"] = round(state["calories"] + 1.04, 1)
        live_run_db[user_id] = state

    pace = state["distance_km"] and state["seconds"] / state["distance_km"] or 0
    return LiveRunData(
        seconds=state["seconds"],
        distance_km=state["distance_km"],
        pace_sec_per_km=pace,
        hr=state["hr"],
        calories=int(state["calories"]),
        status=state.get("status", "idle"),
    )


@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str):
    act = next((a for a in activities_db if a["id"] == activity_id), None)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return Activity(**act)
