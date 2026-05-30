"""
PACE — In-Memory Mock Database
Replace with PostgreSQL + SQLAlchemy in production.
"""
from datetime import datetime, timedelta
import random

# ── USERS ─────────────────────────────────────────────────────
users_db: dict = {
    "user_alex": {
        "id": "user_alex",
        "name": "Alex Runner",
        "email": "alex@pace.run",
        "password": "secret123",  # plain-text only for mock; use bcrypt in prod
        "location": "Jakarta, Indonesia",
        "fitness_score": 78,
        "fatigue_score": 42,
        "form_status": "Good",
        "vo2_max": 52,
        "total_activities": 148,
        "followers": 312,
        "following": 89,
        "weekly_goal_km": 50,
        "token": "mock_token_alex_2024",
    }
}

# ── ACTIVITIES ────────────────────────────────────────────────
def _days_ago(n: int) -> str:
    return (datetime.now() - timedelta(days=n)).strftime("%d %b %Y")

activities_db: list = [
    {
        "id": "act_001", "user_id": "user_alex", "type": "run",
        "name": "Morning Tempo Run", "date": _days_ago(0),
        "distance_km": 10.2, "duration_seconds": 3060,
        "avg_pace_sec_per_km": 300, "avg_hr": 162, "calories": 650,
        "elevation_m": 48,
    },
    {
        "id": "act_002", "user_id": "user_alex", "type": "run",
        "name": "Easy Aerobic Run", "date": _days_ago(1),
        "distance_km": 8.5, "duration_seconds": 2890,
        "avg_pace_sec_per_km": 340, "avg_hr": 144, "calories": 480,
        "elevation_m": 22,
    },
    {
        "id": "act_003", "user_id": "user_alex", "type": "ride",
        "name": "Weekend Ride", "date": _days_ago(2),
        "distance_km": 32.0, "duration_seconds": 5400,
        "avg_pace_sec_per_km": 169, "avg_hr": 138, "calories": 820,
        "elevation_m": 210,
    },
    {
        "id": "act_004", "user_id": "user_alex", "type": "run",
        "name": "Long Run", "date": _days_ago(4),
        "distance_km": 16.0, "duration_seconds": 5760,
        "avg_pace_sec_per_km": 360, "avg_hr": 148, "calories": 980,
        "elevation_m": 65,
    },
    {
        "id": "act_005", "user_id": "user_alex", "type": "run",
        "name": "Interval Training", "date": _days_ago(6),
        "distance_km": 7.0, "duration_seconds": 1980,
        "avg_pace_sec_per_km": 283, "avg_hr": 175, "calories": 510,
        "elevation_m": 30,
    },
]

# ── WEEKLY PROGRESS ───────────────────────────────────────────
weekly_progress_db: dict = {
    "user_alex": {
        "total_km": 34.7,
        "goal_km": 50,
        "change_pct": 14,
        "days": [8.5, 10.2, 0, 7.0, 0, 9.0, 0],
        "runs": 4,
        "avg_pace_sec": 328,
        "total_time_min": 204,
    }
}

# ── ANALYTICS ─────────────────────────────────────────────────
analytics_db: dict = {
    "user_alex": {
        "week": {
            "total_km": 48.7,
            "total_time_min": 268,
            "avg_pace_sec": 328,
            "avg_hr": 153,
            "dist_change_pct": 12,
            "pace_change_sec": 8,
            "pace_data": [345, 338, 331, 328, 322, 318, 315],
            "hr_data": [149, 152, 155, 153, 158, 150, 147],
            "hr_zones": [
                {"name": "Z1", "range": "<120", "pct": 8, "color": "#3B82F6"},
                {"name": "Z2", "range": "120-140", "pct": 32, "color": "#10B981"},
                {"name": "Z3", "range": "140-160", "pct": 38, "color": "#F59E0B"},
                {"name": "Z4", "range": "160-175", "pct": 18, "color": "#EF4444"},
                {"name": "Z5", "range": ">175", "pct": 4, "color": "#8B5CF6"},
            ],
        },
        "month": {
            "total_km": 192.4,
            "total_time_min": 1060,
            "avg_pace_sec": 332,
            "avg_hr": 151,
            "dist_change_pct": 9,
            "pace_change_sec": 6,
            "pace_data": [350, 345, 340, 336, 333, 330, 332, 328, 325, 322, 320, 318],
            "hr_data": [150, 153, 151, 155, 152, 149, 154, 151, 148, 153, 150, 147],
            "hr_zones": [
                {"name": "Z1", "range": "<120", "pct": 6, "color": "#3B82F6"},
                {"name": "Z2", "range": "120-140", "pct": 35, "color": "#10B981"},
                {"name": "Z3", "range": "140-160", "pct": 40, "color": "#F59E0B"},
                {"name": "Z4", "range": "160-175", "pct": 16, "color": "#EF4444"},
                {"name": "Z5", "range": ">175", "pct": 3, "color": "#8B5CF6"},
            ],
        },
        "year": {
            "total_km": 1840.0,
            "total_time_min": 10200,
            "avg_pace_sec": 335,
            "avg_hr": 152,
            "dist_change_pct": 22,
            "pace_change_sec": 18,
            "pace_data": [358, 352, 348, 344, 340, 336, 335, 332, 330, 328, 325, 322],
            "hr_data": [155, 154, 153, 153, 152, 151, 152, 151, 150, 150, 149, 148],
            "hr_zones": [
                {"name": "Z1", "range": "<120", "pct": 7, "color": "#3B82F6"},
                {"name": "Z2", "range": "120-140", "pct": 33, "color": "#10B981"},
                {"name": "Z3", "range": "140-160", "pct": 39, "color": "#F59E0B"},
                {"name": "Z4", "range": "160-175", "pct": 17, "color": "#EF4444"},
                {"name": "Z5", "range": ">175", "pct": 4, "color": "#8B5CF6"},
            ],
        },
        "all": {
            "total_km": 4220.0,
            "total_time_min": 23500,
            "avg_pace_sec": 342,
            "avg_hr": 154,
            "dist_change_pct": 35,
            "pace_change_sec": 28,
            "pace_data": [375, 368, 362, 356, 350, 345, 342, 338, 335, 332, 328, 325],
            "hr_data": [158, 157, 156, 155, 154, 154, 153, 152, 152, 151, 150, 149],
            "hr_zones": [
                {"name": "Z1", "range": "<120", "pct": 8, "color": "#3B82F6"},
                {"name": "Z2", "range": "120-140", "pct": 31, "color": "#10B981"},
                {"name": "Z3", "range": "140-160", "pct": 40, "color": "#F59E0B"},
                {"name": "Z4", "range": "160-175", "pct": 17, "color": "#EF4444"},
                {"name": "Z5", "range": ">175", "pct": 4, "color": "#8B5CF6"},
            ],
        },
    }
}

# ── TRAINING PLAN ─────────────────────────────────────────────
training_plan_db: dict = {
    "user_alex": {
        "today": {
            "name": "Tempo Intervals",
            "type": "tempo",
            "distance_km": 10,
            "duration_min": 55,
            "zone": 3,
            "description": "4×1km repeats at threshold pace with 90s recovery.",
        },
        "week": [
            {"day": "Mon", "name": "Easy Run", "distance_km": 8, "zone": 2, "done": True},
            {"day": "Tue", "name": "Tempo Intervals", "distance_km": 10, "zone": 3, "done": False},
            {"day": "Wed", "name": "Rest / Cross-train", "distance_km": 0, "zone": 0, "done": False},
            {"day": "Thu", "name": "Medium-Long Run", "distance_km": 14, "zone": 2, "done": False},
            {"day": "Fri", "name": "Rest Day", "distance_km": 0, "zone": 0, "done": False},
            {"day": "Sat", "name": "Long Run", "distance_km": 20, "zone": 2, "done": False},
            {"day": "Sun", "name": "Recovery Run", "distance_km": 6, "zone": 1, "done": False},
        ],
    }
}

# ── COMMUNITY FEED ────────────────────────────────────────────
community_feed_db: list = [
    {
        "id": "feed_001", "user_name": "Budi Setiawan", "user_initials": "BS",
        "user_color": "#3B82F6", "activity_name": "Morning Tempo",
        "distance_km": 10.2, "pace_str": "5'02\"/km", "location": "Senayan, Jakarta",
        "time_ago": "2h ago", "likes": 24, "comments": 5, "liked_by_me": False,
    },
    {
        "id": "feed_002", "user_name": "Rina Pratiwi", "user_initials": "RP",
        "user_color": "#8B5CF6", "activity_name": "Half Marathon Prep",
        "distance_km": 18.5, "pace_str": "5'28\"/km", "location": "Kelapa Gading",
        "time_ago": "4h ago", "likes": 41, "comments": 9, "liked_by_me": True,
    },
    {
        "id": "feed_003", "user_name": "Dimas Haryanto", "user_initials": "DH",
        "user_color": "#10B981", "activity_name": "Easy Sunday Run",
        "distance_km": 7.8, "pace_str": "5'58\"/km", "location": "TMII, Jakarta",
        "time_ago": "6h ago", "likes": 15, "comments": 2, "liked_by_me": False,
    },
    {
        "id": "feed_004", "user_name": "Sari Wahyu", "user_initials": "SW",
        "user_color": "#F59E0B", "activity_name": "Track Session",
        "distance_km": 12.0, "pace_str": "4'45\"/km", "location": "GBK Senayan",
        "time_ago": "1d ago", "likes": 67, "comments": 14, "liked_by_me": False,
    },
    {
        "id": "feed_005", "user_name": "Fajar Nugraha", "user_initials": "FN",
        "user_color": "#EF4444", "activity_name": "Hill Repeats",
        "distance_km": 9.0, "pace_str": "5'18\"/km", "location": "Bogor",
        "time_ago": "1d ago", "likes": 33, "comments": 7, "liked_by_me": False,
    },
]

# ── PERSONAL RECORDS ──────────────────────────────────────────
personal_records_db: dict = {
    "user_alex": [
        {"distance_label": "1 km",  "time": "3'42\"", "date": "12 Mar 2024"},
        {"distance_label": "5 km",  "time": "19'48\"", "date": "5 Jan 2024"},
        {"distance_label": "10 km", "time": "41'22\"", "date": "20 Oct 2023"},
        {"distance_label": "Half",  "time": "1:31'05\"", "date": "8 Oct 2023"},
        {"distance_label": "Full",  "time": "3:22'40\"", "date": "14 May 2023"},
    ]
}

# ── BADGES ────────────────────────────────────────────────────
badges_db: dict = {
    "user_alex": [
        {"id": "b1", "icon": "🔥", "name": "7-Day Streak"},
        {"id": "b2", "icon": "🏅", "name": "Sub-20 5K"},
        {"id": "b3", "icon": "🌟", "name": "100 Runs"},
        {"id": "b4", "icon": "⚡", "name": "Speed Demon"},
        {"id": "b5", "icon": "🏔️", "name": "Hill Climber"},
        {"id": "b6", "icon": "🌙", "name": "Night Owl"},
    ]
}

# ── DEVICES ───────────────────────────────────────────────────
devices_db: list = [
    {"id": "dev_garmin", "name": "Garmin Forerunner 265", "icon": "⌚", "connected": True, "type": "watch"},
    {"id": "dev_hrm",    "name": "Garmin HRM-Pro",        "icon": "💓", "connected": True,  "type": "hrm"},
    {"id": "dev_apple",  "name": "Apple Watch Series 9",  "icon": "⌚", "connected": False, "type": "watch"},
    {"id": "dev_strava", "name": "Strava",                "icon": "🟠", "connected": True,  "type": "app"},
    {"id": "dev_wahoo",  "name": "Wahoo KICKR",           "icon": "🚴", "connected": False, "type": "trainer"},
]

# ── LIVE RUN (polling state per user) ─────────────────────────
live_run_db: dict = {}
