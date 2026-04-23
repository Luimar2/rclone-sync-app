from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rclone import (
    listar_remotes,
    rclone_disponivel,
    criar_remote_gdrive,
    verificar_remote,
    deletar_remote
)
from services.app_config import (
    carregar_config,
    salvar_config,
    ParSincronizacao,
    FiltrosSinc
)
import uuid

router = APIRouter(prefix="/config", tags=["Configuração"])


# --- Ambiente ---

@router.get("/status")
async def status_rclone():
    return {"rclone_disponivel": rclone_disponivel()}


# --- Remotes ---

@router.get("/remotes")
async def get_remotes():
    remotes = listar_remotes()
    return {"remotes": remotes, "total": len(remotes)}


@router.post("/remotes/{nome}")
async def criar_remote(nome: str):
    resultado = criar_remote_gdrive(nome)
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return {"mensagem": f"Remote '{nome}' criado com sucesso"}


@router.get("/remotes/{nome}/verificar")
async def checar_remote(nome: str):
    resultado = verificar_remote(nome)
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return {"sucesso": True, "info": resultado["info"]}


@router.delete("/remotes/{nome}")
async def remover_remote(nome: str):
    resultado = deletar_remote(nome)
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return {"mensagem": f"Remote '{nome}' removido"}


# --- Pares de sincronização ---

@router.get("/pares")
async def listar_pares():
    config = carregar_config()
    return {"pares": config.pares}


class ParRequest(BaseModel):
    local_path: str
    remote_name: str
    remote_path: str
    filtros: FiltrosSinc = FiltrosSinc()


@router.post("/pares")
async def adicionar_par(payload: ParRequest):
    config = carregar_config()
    novo_par = ParSincronizacao(
        id=str(uuid.uuid4()),
        local_path=payload.local_path,
        remote_name=payload.remote_name,
        remote_path=payload.remote_path,
        filtros=payload.filtros
    )
    config.pares.append(novo_par)
    salvar_config(config)
    return {"mensagem": "Par adicionado", "par": novo_par}


@router.delete("/pares/{par_id}")
async def remover_par(par_id: str):
    config = carregar_config()
    config.pares = [p for p in config.pares if p.id != par_id]
    salvar_config(config)
    return {"mensagem": "Par removido"}


@router.patch("/pares/{par_id}/ativo")
async def toggle_par(par_id: str, ativo: bool):
    config = carregar_config()
    for par in config.pares:
        if par.id == par_id:
            par.ativo = ativo
            salvar_config(config)
            return {"mensagem": f"Par {'ativado' if ativo else 'desativado'}"}
    raise HTTPException(status_code=404, detail="Par não encontrado")