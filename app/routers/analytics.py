"""
PACE — Analytics Router
GET /api/v1/analytics/summary
GET /api/v1/analytics/pace-chart/{user_id}
GET /api/v1/analytics/hr-zones/{user_id}
GET /api/v1/analytics/vo2max
"""
from fastapi import APIRouter, Query, HTTPException
from app.schemas.pace_schemas import AnalyticsPeriod, VO2MaxResponse
from app.models.database import analytics_db, users_db
from app.services.helpers import vo2_level

router = APIRouter()

VALID_PERIODS = {"week", "month", "year", "all"}


@router.get("/summary", response_model=AnalyticsPeriod)
async def get_summary(
    user_id: str = Query(default="user_alex"),
    period: str = Query(default="week"),
):
    if period not in VALID_PERIODS:
        raise HTTPException(status_code=400, detail=f"period must be one of {VALID_PERIODS}")
    user_analytics = analytics_db.get(user_id)
    if not user_analytics:
        raise HTTPException(status_code=404, detail="Analytics not found for user")
    data = user_analytics.get(period)
    if not data:
        raise HTTPException(status_code=404, detail=f"No data for period '{period}'")
    return AnalyticsPeriod(**data)


@router.get("/pace-chart/{user_id}")
async def get_pace_chart(user_id: str, period: str = Query(default="week")):
    user_analytics = analytics_db.get(user_id, {})
    data = user_analytics.get(period, {})
    return {"pace_data": data.get("pace_data", []), "avg_pace_sec": data.get("avg_pace_sec", 0)}


@router.get("/hr-zones/{user_id}")
async def get_hr_zones(user_id: str, period: str = Query(default="week")):
    user_analytics = analytics_db.get(user_id, {})
    data = user_analytics.get(period, {})
    return {"hr_zones": data.get("hr_zones", []), "avg_hr": data.get("avg_hr", 0)}


@router.get("/vo2max", response_model=VO2MaxResponse)
async def get_vo2max(user_id: str = Query(default="user_alex")):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    v = user["vo2_max"]
    level, desc = vo2_level(v)
    return VO2MaxResponse(vo2_max=v, level=level, description=desc)
