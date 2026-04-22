from fastapi import APIRouter, HTTPException
from services.rclone import listar_remotes, rclone_disponivel

router = APIRouter(prefix="/config", tags=["Configuração"])


@router.get("/status")
async def status_rclone():
    return {"rclone_disponivel": rclone_disponivel()}


@router.get("/remotes")
async def get_remotes():
    remotes = listar_remotes()
    return {"remotes": remotes, "total": len(remotes)}