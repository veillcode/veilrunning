"""
PACE — Community Router
GET  /api/v1/community/feed
POST /api/v1/community/like
"""
from fastapi import APIRouter, Query
from app.schemas.pace_schemas import FeedItem, LikeRequest
from app.models.database import community_feed_db
from typing import List

router = APIRouter()


@router.get("/feed", response_model=List[FeedItem])
async def get_feed(
    tab: str = Query(default="following"),
    limit: int = Query(default=20, le=50),
):
    return [FeedItem(**item) for item in community_feed_db[:limit]]


@router.post("/like")
async def like_activity(body: LikeRequest):
    item = next((f for f in community_feed_db if f["id"] == body.feed_id), None)
    if not item:
        return {"success": False, "message": "Feed item not found"}
    item["liked_by_me"] = not item["liked_by_me"]
    item["likes"] += 1 if item["liked_by_me"] else -1
    return {"success": True, "likes": item["likes"], "liked_by_me": item["liked_by_me"]}
