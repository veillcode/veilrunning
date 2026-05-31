# app/routers/community.py
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.models.database_setup import get_db, CommunityFeedDB, LikeDB
from app.schemas.pace_schemas import FeedItem, LikeRequest
from typing import List
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/feed", response_model=List[FeedItem])
async def get_feed(
    tab: str = Query(default="following"),
    user_id: str = Query(default="user_alex"),
    limit: int = Query(default=20, le=50),
    db: Session = Depends(get_db)
):
    feeds = db.query(CommunityFeedDB).order_by(CommunityFeedDB.posted_at.desc()).limit(limit).all()
    result = []
    for f in feeds:
        liked = db.query(LikeDB).filter(LikeDB.user_id == user_id, LikeDB.feed_id == f.id).first()
        result.append(FeedItem(
            id=f.id, user_id=f.user_id, user_name=f.user_name,
            location=f.location, title=f.title,
            distance_km=f.distance_km, duration_seconds=f.duration_seconds,
            avg_pace_sec_per_km=f.avg_pace_sec_per_km,
            likes=f.likes, comments=f.comments,
            liked_by_me=bool(liked),
            posted_at=f.posted_at.isoformat() if f.posted_at else ""
        ))
    return result

@router.post("/like")
async def like_activity(body: LikeRequest, user_id: str = Query(default="user_alex"), db: Session = Depends(get_db)):
    feed = db.query(CommunityFeedDB).filter(CommunityFeedDB.id == body.feed_id).first()
    if not feed:
        return {"success": False, "message": "Feed item not found"}
    existing = db.query(LikeDB).filter(LikeDB.user_id == user_id, LikeDB.feed_id == body.feed_id).first()
    if existing:
        db.delete(existing)
        feed.likes = max(0, feed.likes - 1)
        liked = False
    else:
        db.add(LikeDB(id=str(uuid.uuid4()), user_id=user_id, feed_id=body.feed_id))
        feed.likes += 1
        liked = True
    db.commit()
    return {"success": True, "likes": feed.likes, "liked_by_me": liked}
