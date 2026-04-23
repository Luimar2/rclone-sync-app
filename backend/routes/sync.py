from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.sync_executor import executar_bisync
from services.snapshot import criar_snapshot
from services.lock import SyncLock, LockError

router = APIRouter(prefix="/sync", tags=["Sincronização"])


class SyncRequest(BaseModel):
    local_path: str
    remote_path: str
    criar_snapshot: bool = True


@router.post("/executar")
async def executar_sync(payload: SyncRequest):
    try:
        with SyncLock():
            if payload.criar_snapshot:
                criar_snapshot(payload.local_path)

            resultado = executar_bisync(payload.local_path, payload.remote_path)
            return resultado

    except LockError as e:
        raise HTTPException(status_code=409, detail=str(e))