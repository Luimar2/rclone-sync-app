import asyncio
from pathlib import Path
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.app_config import carregar_config
from services.event_logger import listar_eventos

router = APIRouter(prefix="/logs", tags=["Logs"])

LOG_DIR = Path.home() / ".local/state/rclone-bisync"


def ultimo_log() -> Path | None:
    logs = sorted(LOG_DIR.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
    return logs[0] if logs else None


@router.get("/listar")
async def listar_logs():
    if not LOG_DIR.exists():
        return {"logs": []}
    logs = sorted(
        LOG_DIR.glob("*.log"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    return {
        "logs": [
            {
                "nome": f.name,
                "path": str(f),
                "tamanho": f.stat().st_size,
            }
            for f in logs[:20]
        ]
    }


@router.get("/ler/{nome}")
async def ler_log(nome: str):
    arquivo = LOG_DIR / nome
    if not arquivo.exists():
        return {"conteudo": ""}
    return {"conteudo": arquivo.read_text(errors="ignore")}


@router.websocket("/ws")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    try:
        ultimo = ultimo_log()
        posicao = ultimo.stat().st_size if ultimo else 0

        while True:
            atual = ultimo_log()

            if atual and atual != ultimo:
                ultimo = atual
                posicao = 0

            if ultimo and ultimo.exists():
                conteudo = ultimo.read_text(errors="ignore")
                linhas = conteudo[posicao:]
                if linhas:
                    await websocket.send_text(linhas)
                    posicao = len(conteudo)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass

@router.get("/eventos")
async def listar_eventos_app(limite: int = 100):
    return {"eventos": listar_eventos(limite)}
