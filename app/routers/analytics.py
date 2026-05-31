from fastapi import APIRouter, Query, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.database_setup import get_db, ActivityDB
from app.schemas.pace_schemas import AnalyticsPeriod, VO2MaxResponse
from app.models.database_setup import UserDB
from app.services.helpers import vo2_level
from datetime import datetime, timedelta, timezone
from typing import Optional

router = APIRouter()

WIB = timezone(timedelta(hours=7))

def get_period_range(period: str):
    now = datetime.now(WIB)
    if period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    elif period == "year":
        start = now - timedelta(days=365)
    else:
        start = datetime(2000, 1, 1, tzinfo=WIB)
    return start

@router.get("/summary")
async def get_summary(
    user_id: str = Query(default="user_alex"),
    period: str = Query(default="week"),
    db: Session = Depends(get_db)
):
    start = get_period_range(period)
    acts = db.query(ActivityDB).filter(
        ActivityDB.user_id == user_id,
        ActivityDB.created_at >= start.replace(tzinfo=None)
    ).all()

    if not acts:
        return {
            "total_km": 0, "avg_pace_sec": 0, "total_time_min": 0,
            "avg_hr": 0, "dist_change_pct": 0, "pace_change_sec": 0,
            "pace_data": [], "hr_data": [], "hr_zones": [0,0,0,0,0]
        }

    total_km = sum(a.distance_km for a in acts)
    total_sec = sum(a.duration_seconds for a in acts)
    total_time_min = total_sec // 60
    avg_pace_sec = round(total_sec / total_km) if total_km > 0 else 0
    hr_list = [a.avg_hr for a in acts if a.avg_hr]
    avg_hr = round(sum(hr_list) / len(hr_list)) if hr_list else 0
    pace_data = [round(a.avg_pace_sec_per_km) for a in acts[-7:]]
    hr_data = [a.avg_hr or 0 for a in acts[-7:]]

    return {
        "total_km": round(total_km, 1),
        "avg_pace_sec": avg_pace_sec,
        "total_time_min": total_time_min,
        "avg_hr": avg_hr,
        "dist_change_pct": 0,
        "pace_change_sec": 0,
        "pace_data": pace_data if pace_data else [avg_pace_sec],
        "hr_data": hr_data if hr_data else [avg_hr],
        "hr_zones": [5, 30, 40, 20, 5]
    }

@router.get("/vo2max")
async def get_vo2max(
    user_id: str = Query(default="user_alex"),
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    v = user.vo2_max
    level, desc = vo2_level(v)
    return {"vo2_max": v, "level": level, "description": desc}

@router.get("/pace-chart/{user_id}")
async def get_pace_chart(user_id: str, period: str = Query(default="week"), db: Session = Depends(get_db)):
    start = get_period_range(period)
    acts = db.query(ActivityDB).filter(
        ActivityDB.user_id == user_id,
        ActivityDB.created_at >= start.replace(tzinfo=None)
    ).all()
    pace_data = [round(a.avg_pace_sec_per_km) for a in acts]
    avg = round(sum(pace_data)/len(pace_data)) if pace_data else 0
    return {"pace_data": pace_data, "avg_pace_sec": avg}

@router.get("/hr-zones/{user_id}")
async def get_hr_zones(user_id: str, period: str = Query(default="week"), db: Session = Depends(get_db)):
    start = get_period_range(period)
    acts = db.query(ActivityDB).filter(
        ActivityDB.user_id == user_id,
        ActivityDB.created_at >= start.replace(tzinfo=None)
    ).all()
    hr_list = [a.avg_hr for a in acts if a.avg_hr]
    avg = round(sum(hr_list)/len(hr_list)) if hr_list else 0
    return {"hr_zones": [5, 30, 40, 20, 5], "avg_hr": avg}