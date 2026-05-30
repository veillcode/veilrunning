"""
PACE — Auth Router
POST /api/v1/auth/login
POST /api/v1/auth/register
"""
from fastapi import APIRouter, HTTPException
from app.schemas.pace_schemas import LoginRequest, RegisterRequest, AuthResponse
from app.models.database import users_db
import uuid

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest):
    user = next(
        (u for u in users_db.values() if u["email"] == body.email),
        None,
    )
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return AuthResponse(
        token=user["token"],
        user_id=user["id"],
        name=user["name"],
        message="Login successful",
    )


@router.post("/register", response_model=AuthResponse)
async def register(body: RegisterRequest):
    if any(u["email"] == body.email for u in users_db.values()):
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = f"user_{uuid.uuid4().hex[:8]}"
    token = f"mock_token_{user_id}"
    users_db[user_id] = {
        "id": user_id,
        "name": body.name,
        "email": body.email,
        "password": body.password,
        "location": body.location,
        "fitness_score": 50,
        "fatigue_score": 20,
        "form_status": "Good",
        "vo2_max": 40,
        "total_activities": 0,
        "followers": 0,
        "following": 0,
        "weekly_goal_km": 40,
        "token": token,
    }
    return AuthResponse(token=token, user_id=user_id, name=body.name, message="Registered!")
