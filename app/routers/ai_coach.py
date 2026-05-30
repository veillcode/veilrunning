"""
PACE — AI Coach Router
GET  /api/v1/ai-coach/recommendation
POST /api/v1/ai-coach/chat

Chat uses the Anthropic Claude API.
Set ANTHROPIC_API_KEY env var for real responses; falls back to mock if unset.
"""
# Baris 9-11 ubah jadi:
from fastapi import APIRouter, Query
from pace_schemas import AIRecommendation, ChatRequest, ChatResponse
from database import users_db, analytics_db, activities_db
import os
import httpx

router = APIRouter()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-20250514"


def _build_system_prompt(user: dict, analytics: dict) -> str:
    return (
        "You are PACE AI Coach, a friendly and knowledgeable running coach assistant. "
        "You give concise, actionable advice tailored to the runner's data. "
        "Keep replies short (2-4 sentences). Respond in the same language the user writes in. "
        f"Runner profile: Name={user['name']}, "
        f"VO2max={user['vo2_max']}, "
        f"Fitness score={user['fitness_score']}/100, "
        f"Fatigue score={user['fatigue_score']}/100, "
        f"Form status={user['form_status']}, "
        f"Weekly km this week={analytics.get('total_km', '?')}."
    )


async def _call_claude(system: str, message: str) -> str:
    if not ANTHROPIC_API_KEY:
        # Mock fallback
        return _mock_response(message)

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 300,
                "system": system,
                "messages": [{"role": "user", "content": message}],
            },
        )
        data = resp.json()
        return data["content"][0]["text"]


def _mock_response(message: str) -> str:
    msg = message.lower()
    if any(w in msg for w in ["pace", "kecepatan", "speed"]):
        return (
            "For your fitness level, aim for an easy pace around 5'45\"–6'00\"/km for Zone 2 runs. "
            "Tempo runs should feel comfortably hard at around 5'00\"/km. "
            "Consistency at easy paces builds your aerobic base the most."
        )
    if any(w in msg for w in ["recovery", "istirahat", "rest", "capek", "fatigue"]):
        return (
            "Your fatigue score looks moderate. Focus on sleep and nutrition today. "
            "A short 20-min walk or stretching session is better than forcing a hard run. "
            "You'll come back stronger tomorrow."
        )
    if any(w in msg for w in ["marathon", "half", "race", "lomba"]):
        return (
            "Based on your current VO2max and training load, you're building good race fitness! "
            "Make sure your long run hits 80% of race distance at least 3 weeks before race day. "
            "Keep 80% of your runs easy and 20% quality."
        )
    return (
        "Great question! Based on your recent training data, you're making solid progress. "
        "Keep your easy runs truly easy (conversational pace) and save the intensity "
        "for your scheduled quality sessions. Consistency is key! 🏃"
    )


@router.get("/recommendation", response_model=AIRecommendation)
async def get_recommendation(user_id: str = Query(default="user_alex")):
    user = users_db.get(user_id, users_db["user_alex"])
    fat = user["fatigue_score"]
    name = user["name"].split()[0]

    if fat > 70:
        reco_name, reco_detail = "Rest Day", "No running today"
        reco_desc = (
            "Your body needs recovery. High fatigue reduces performance and raises injury risk. "
            "Take a full rest day with light stretching or a short walk."
        )
    elif fat > 55:
        reco_name, reco_detail = "Recovery Run", "5 km · Zone 1–2"
        reco_desc = (
            "A light run will improve circulation and speed recovery "
            "without adding meaningful training stress."
        )
    else:
        reco_name, reco_detail = "Easy Run", "8 km · Zone 2"
        reco_desc = (
            "Based on your training load and recovery status, "
            "an easy aerobic run will efficiently build your aerobic base."
        )

    return AIRecommendation(
        greeting=f"Hi {name}! 👋",
        reco_name=reco_name,
        reco_detail=reco_detail,
        reco_desc=reco_desc,
        fitness_score=user["fitness_score"],
        fatigue_score=user["fatigue_score"],
        form_status=user["form_status"],
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest):
    user = users_db.get(body.user_id, users_db["user_alex"])
    analytics = analytics_db.get(body.user_id, {}).get("week", {})
    system = _build_system_prompt(user, analytics)
    reply = await _call_claude(system, body.message)
    return ChatResponse(reply=reply)
