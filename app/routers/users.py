"""
PACE — Users Router
GET /api/v1/users/{user_id}/profile
GET /api/v1/users/{user_id}/weekly-progress
GET /api/v1/users/{user_id}/personal-records
GET /api/v1/users/{user_id}/badges
"""
from fastapi import APIRouter, HTTPException
from app.schemas.pace_schemas import UserProfile, WeeklyProgress, PersonalRecord, Badge
from app.models.database import users_db, weekly_progress_db, personal_records_db, badges_db
from typing import List

router = APIRouter()


def _get_user(user_id: str) -> dict:
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/profile", response_model=UserProfile)
async def get_profile(user_id: str):
    u = _get_user(user_id)
    return UserProfile(**{k: v for k, v in u.items() if k != "password" and k != "token"})


@router.get("/{user_id}/weekly-progress", response_model=WeeklyProgress)
async def get_weekly_progress(user_id: str):
    _get_user(user_id)
    progress = weekly_progress_db.get(user_id)
    if not progress:
        raise HTTPException(status_code=404, detail="No progress data found")
    return WeeklyProgress(**progress)


@router.get("/{user_id}/personal-records", response_model=List[PersonalRecord])
async def get_personal_records(user_id: str):
    _get_user(user_id)
    return [PersonalRecord(**pr) for pr in personal_records_db.get(user_id, [])]


@router.get("/{user_id}/badges", response_model=List[Badge])
async def get_badges(user_id: str):
    _get_user(user_id)
    return [Badge(**b) for b in badges_db.get(user_id, [])]
