"""
PACE — Devices Router
GET  /api/v1/devices/
POST /api/v1/devices/connect
"""
from fastapi import APIRouter, HTTPException
from app.schemas.pace_schemas import Device, ConnectDeviceRequest
from app.models.database import devices_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[Device])
async def list_devices():
    return [Device(**d) for d in devices_db]


@router.post("/connect")
async def connect_device(body: ConnectDeviceRequest):
    device = next((d for d in devices_db if d["id"] == body.device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device["connected"] = not device["connected"]
    status = "connected" if device["connected"] else "disconnected"
    return {"success": True, "device_id": body.device_id, "status": status, "name": device["name"]}
