"""
PACE — Pydantic Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any


# ── AUTH ──────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    location: Optional[str] = "Indonesia"

class AuthResponse(BaseModel):
    token: str
    user_id: str
    name: str
    message: str


# ── USER ──────────────────────────────────────────────────────
class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    location: str
    fitness_score: int
    fatigue_score: int
    form_status: str
    vo2_max: int
    total_activities: int
    followers: int
    following: int
    weekly_goal_km: int

class WeeklyProgress(BaseModel):
    total_km: float
    goal_km: int
    change_pct: int
    days: List[float]
    runs: int
    avg_pace_sec: int
    total_time_min: int

class PersonalRecord(BaseModel):
    distance_label: str
    time: str
    date: str

class Badge(BaseModel):
    id: str
    icon: str
    name: str


# ── ACTIVITY ──────────────────────────────────────────────────
class ActivityCreate(BaseModel):
    type: str = "run"
    name: str = "Run"
    distance_km: float
    duration_seconds: int
    avg_hr: Optional[int] = None
    calories: Optional[int] = None
    elevation_m: Optional[int] = 0

class Activity(BaseModel):
    id: str
    user_id: str
    type: str
    name: str
    date: str
    distance_km: float
    duration_seconds: int
    avg_pace_sec_per_km: int
    avg_hr: Optional[int] = None
    calories: Optional[int] = None
    elevation_m: Optional[int] = 0


# ── ANALYTICS ─────────────────────────────────────────────────
class HRZone(BaseModel):
    name: str
    range: str
    pct: int
    color: str

class AnalyticsPeriod(BaseModel):
    total_km: float
    total_time_min: int
    avg_pace_sec: int
    avg_hr: int
    dist_change_pct: int
    pace_change_sec: int
    pace_data: List[float]
    hr_data: List[float]
    hr_zones: List[HRZone]

class VO2MaxResponse(BaseModel):
    vo2_max: int
    level: str
    description: str


# ── TRAINING PLAN ─────────────────────────────────────────────
class TodayPlan(BaseModel):
    name: str
    type: str
    distance_km: float
    duration_min: int
    zone: int
    description: str

class WeeklyPlanDay(BaseModel):
    day: str
    name: str
    distance_km: float
    zone: int
    done: bool


# ── COMMUNITY ─────────────────────────────────────────────────
class FeedItem(BaseModel):
    id: str
    user_name: str
    user_initials: str
    user_color: str
    activity_name: str
    distance_km: float
    pace_str: str
    location: str
    time_ago: str
    likes: int
    comments: int
    liked_by_me: bool

class LikeRequest(BaseModel):
    feed_id: str
    user_id: Optional[str] = "user_alex"


# ── AI COACH ──────────────────────────────────────────────────
class AIRecommendation(BaseModel):
    greeting: str
    reco_name: str
    reco_detail: str
    reco_desc: str
    fitness_score: int
    fatigue_score: int
    form_status: str

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "user_alex"

class ChatResponse(BaseModel):
    reply: str


# ── DEVICES ───────────────────────────────────────────────────
class Device(BaseModel):
    id: str
    name: str
    icon: str
    connected: bool
    type: str

class ConnectDeviceRequest(BaseModel):
    device_id: str


# ── LIVE RUN ──────────────────────────────────────────────────
class LiveRunData(BaseModel):
    seconds: int
    distance_km: float
    pace_sec_per_km: float
    hr: int
    calories: int
    status: str
