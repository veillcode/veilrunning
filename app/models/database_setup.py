# app/models/database_setup.py
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pace.db")

# Fix untuk Railway PostgreSQL URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── MODELS ────────────────────────────────────────
class UserDB(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String, default="")
    fitness_score = Column(Integer, default=50)
    fatigue_score = Column(Integer, default=20)
    form_status = Column(String, default="Good")
    vo2_max = Column(Integer, default=40)
    weekly_goal_km = Column(Float, default=40.0)
    total_activities = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    token = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ActivityDB(Base):
    __tablename__ = "activities"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    type = Column(String, default="run")
    name = Column(String, nullable=False)
    date = Column(String, default="")
    distance_km = Column(Float, default=0.0)
    duration_seconds = Column(Integer, default=0)
    avg_pace_sec_per_km = Column(Float, default=0.0)
    avg_hr = Column(Integer, nullable=True)
    calories = Column(Integer, default=0)
    elevation_m = Column(Float, nullable=True)
    gps_coords = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CommunityFeedDB(Base):
    __tablename__ = "community_feed"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    location = Column(String, default="")
    title = Column(String, nullable=False)
    distance_km = Column(Float, default=0.0)
    duration_seconds = Column(Integer, default=0)
    avg_pace_sec_per_km = Column(Float, default=0.0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    posted_at = Column(DateTime, default=datetime.utcnow)

class LikeDB(Base):
    __tablename__ = "likes"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    feed_id = Column(String, nullable=False)

# ── DB SESSION ────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    _seed_default_data()

def _seed_default_data():
    db = SessionLocal()
    try:
        # Seed default user jika belum ada
        existing = db.query(UserDB).filter(UserDB.id == "user_alex").first()
        if not existing:
            db.add(UserDB(
                id="user_alex", name="Alex Morgan", email="alex@pace.run",
                password="password123", location="London, UK",
                fitness_score=82, fatigue_score=54, form_status="Good",
                vo2_max=52, weekly_goal_km=70, total_activities=4,
                followers=213, following=89, token="mock_token_user_alex"
            ))
            # Seed activities
            from datetime import timedelta
            acts = [
                ActivityDB(id="act_001", user_id="user_alex", type="run", name="Morning Run", date="Today, 7:14 AM", distance_km=10.12, duration_seconds=3542, avg_pace_sec_per_km=350, avg_hr=152, calories=658),
                ActivityDB(id="act_002", user_id="user_alex", type="run", name="Lunch Easy Run", date="Yesterday", distance_km=5.63, duration_seconds=1980, avg_pace_sec_per_km=352, avg_hr=144, calories=366),
                ActivityDB(id="act_003", user_id="user_alex", type="ride", name="Evening Ride", date="Mon, 6 Jan", distance_km=32.5, duration_seconds=5400, avg_pace_sec_per_km=166, avg_hr=138, calories=812),
                ActivityDB(id="act_004", user_id="user_alex", type="run", name="Long Run Sunday", date="Sun, 5 Jan", distance_km=18.2, duration_seconds=6372, avg_pace_sec_per_km=350, avg_hr=158, calories=1183),
            ]
            for a in acts:
                db.add(a)
            # Seed community feed
            feeds = [
                CommunityFeedDB(id="feed_001", user_id="u2", user_name="Sarah Chen", location="London, UK", title="PB at Hyde Park parkrun! 🏆", distance_km=5.0, duration_seconds=1260, avg_pace_sec_per_km=252, likes=42, comments=8),
                CommunityFeedDB(id="feed_002", user_id="u3", user_name="Marcus Webb", location="Manchester", title="Cold but worth it 🥶", distance_km=12.4, duration_seconds=4092, avg_pace_sec_per_km=330, likes=28, comments=5),
                CommunityFeedDB(id="feed_003", user_id="u4", user_name="Emma Patel", location="Birmingham", title="Half marathon prep continues", distance_km=16.8, duration_seconds=5544, avg_pace_sec_per_km=330, likes=61, comments=14),
                CommunityFeedDB(id="feed_004", user_id="u5", user_name="Tom Okafor", location="Bristol", title="Early morning 10K in the fog 🌫️", distance_km=10.0, duration_seconds=3180, avg_pace_sec_per_km=318, likes=19, comments=3),
            ]
            for f in feeds:
                db.add(f)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
    finally:
        db.close()
