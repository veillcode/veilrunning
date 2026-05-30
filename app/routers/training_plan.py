"""
PACE — Training Plan Router
GET /api/v1/training-plan/today
GET /api/v1/training-plan/week
"""
from fastapi import APIRouter, Query, HTTPException
from app.schemas.pace_schemas import TodayPlan, WeeklyPlanDay
from app.models.database import training_plan_db
from typing import List

router = APIRouter()


@router.get("/today", response_model=TodayPlan)
async def get_today_plan(user_id: str = Query(default="user_alex")):
    plan = training_plan_db.get(user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    return TodayPlan(**plan["today"])


@router.get("/week", response_model=List[WeeklyPlanDay])
async def get_week_plan(user_id: str = Query(default="user_alex")):
    plan = training_plan_db.get(user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    return [WeeklyPlanDay(**d) for d in plan["week"]]
