from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.sync_executor import executar_bisync
from services.snapshot import criar_snapshot
from services.lock import SyncLock, LockError
from services.app_config import carregar_config, FiltrosSinc

router = APIRouter(prefix="/sync", tags=["Sincronização"])


# --- Modelo ---

class SyncRequest(BaseModel):
    local_path: str
    remote_path: str
    criar_snapshot: bool = True


# --- Filtros ---

def montar_filtros(filtros: FiltrosSinc) -> list[str]:
    args = []
    if filtros.arquivos_temporarios:
        args += ["--exclude", "*.tmp", "--exclude", "*.temp"]
    if filtros.lixeira:
        args += ["--exclude", ".Trash/**"]
    if filtros.cache:
        args += ["--exclude", "**/cache/**", "--exclude", "**/Cache/**"]
    if filtros.git:
        args += ["--exclude", ".git/**"]
    if filtros.arquivos_ocultos:
        args += ["--exclude", ".*"]
    if filtros.avancado:
        for linha in filtros.avancado.splitlines():
            linha = linha.strip()
            if linha:
                args += ["--filter", linha]
    return args


# --- Endpoints ---

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


@router.post("/executar-todos")
async def executar_todos():
    config = carregar_config()
    pares_ativos = [p for p in config.pares if p.ativo]

    if not pares_ativos:
        return {"mensagem": "Nenhum par ativo configurado", "resultados": []}

    resultados = []

    try:
        with SyncLock():
            for par in pares_ativos:
                filtros_args = montar_filtros(par.filtros) if par.filtros else []

                criar_snapshot(par.local_path)

                resultado = executar_bisync(
                    par.local_path,
                    f"{par.remote_name}:{par.remote_path}",
                    filtros_extras=filtros_args
                )
                resultados.append({
                    "par": f"{par.local_path} → {par.remote_name}:{par.remote_path}",
                    **resultado
                })

    except LockError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {"resultados": resultados}