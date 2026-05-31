# app/routers/activities.py
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database_setup import get_db, ActivityDB, UserDB
from app.schemas.pace_schemas import Activity, ActivityCreate, LiveRunData
from app.services.helpers import calculate_pace
from datetime import datetime, timezone, timedelta
WIB = timezone(timedelta(hours=7))
from typing import List
import uuid, random

router = APIRouter()

@router.get("/", response_model=List[Activity])
async def list_activities(
    user_id: str = Query(default="user_alex"),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db)
):
    acts = db.query(ActivityDB).filter(ActivityDB.user_id == user_id)\
             .order_by(ActivityDB.created_at.desc()).limit(limit).all()
    return [Activity(
        id=a.id, user_id=a.user_id, type=a.type, name=a.name, date=a.date,
        distance_km=a.distance_km, duration_seconds=a.duration_seconds,
        avg_pace_sec_per_km=a.avg_pace_sec_per_km, avg_hr=a.avg_hr,
        calories=a.calories, elevation_m=a.elevation_m
    ) for a in acts]

@router.post("/", response_model=Activity, status_code=201)
async def create_activity(
    body: ActivityCreate,
    user_id: str = Query(default="user_alex"),
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pace = calculate_pace(body.duration_seconds, body.distance_km)
    cal = body.calories or round(body.distance_km * 62)
    act = ActivityDB(
        id=f"act_{uuid.uuid4().hex[:8]}", user_id=user_id,
        type=body.type, name=body.name,
        date=datetime.now(WIB).strftime("%d %b %Y, %H:%M"),
        distance_km=body.distance_km, duration_seconds=body.duration_seconds,
        avg_pace_sec_per_km=pace, avg_hr=body.avg_hr,
        calories=cal, elevation_m=body.elevation_m,
    )
    db.add(act)
    user.total_activities = (user.total_activities or 0) + 1
    db.commit()
    db.refresh(act)
    return Activity(
        id=act.id, user_id=act.user_id, type=act.type, name=act.name, date=act.date,
        distance_km=act.distance_km, duration_seconds=act.duration_seconds,
        avg_pace_sec_per_km=act.avg_pace_sec_per_km, avg_hr=act.avg_hr,
        calories=act.calories, elevation_m=act.elevation_m
    )

@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str, db: Session = Depends(get_db)):
    act = db.query(ActivityDB).filter(ActivityDB.id == activity_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return Activity(
        id=act.id, user_id=act.user_id, type=act.type, name=act.name, date=act.date,
        distance_km=act.distance_km, duration_seconds=act.duration_seconds,
        avg_pace_sec_per_km=act.avg_pace_sec_per_km, avg_hr=act.avg_hr,
        calories=act.calories, elevation_m=act.elevation_m
    )
