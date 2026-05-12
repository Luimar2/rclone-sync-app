# RcloneSync - Interface gráfica para rclone com Google Drive no Linux
# Copyright (C) 2026 Luimar2
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
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
from services.event_logger import (
    log_par_criado,
    log_par_editado,
    log_par_excluido
)
from services.providers import PROVIDERS
import uuid

router = APIRouter(prefix="/config", tags=["Configuração"])


# --- Providers ---

@router.get("/providers")
async def listar_providers():
    """Retorna todos os providers registrados com seus metadados."""
    return {"providers": [p.to_dict() for p in PROVIDERS]}


# --- Ambiente ---

@router.get("/status")
async def status_rclone():
    return {"rclone_disponivel": rclone_disponivel()}


# --- Remotes ---

@router.get("/remotes")
async def get_remotes(provider: str = "gdrive"):
    """Lista remotes filtrados pelo provider informado."""
    try:
        remotes = listar_remotes(provider_id=provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"remotes": remotes, "total": len(remotes), "provider": provider}


@router.post("/remotes/{nome}")
async def criar_remote(nome: str):
    resultado = criar_remote_gdrive(nome)
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return {"mensagem": f"Remote '{nome}' criado com sucesso"}


@router.get("/remotes/{nome}/verificar")
async def checar_remote(nome: str, provider: str = "gdrive"):
    try:
        resultado = verificar_remote(nome, provider_id=provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
    provider: str = "gdrive"
    filtros: FiltrosSinc = FiltrosSinc()


@router.post("/pares")
async def adicionar_par(payload: ParRequest):
    config = carregar_config()
    novo_par = ParSincronizacao(
        id=str(uuid.uuid4()),
        local_path=payload.local_path,
        remote_name=payload.remote_name,
        remote_path=payload.remote_path,
        provider=payload.provider,
        filtros=payload.filtros
    )
    config.pares.append(novo_par)
    salvar_config(config)
    log_par_criado(novo_par.id, novo_par.local_path, novo_par.remote_name, novo_par.remote_path)
    return {"mensagem": "Par adicionado", "par": novo_par}


class ParEditRequest(BaseModel):
    local_path: Optional[str] = None
    remote_path: Optional[str] = None
    filtros: Optional[FiltrosSinc] = None


@router.patch("/pares/{par_id}")
async def editar_par(par_id: str, payload: ParEditRequest):
    config = carregar_config()
    for par in config.pares:
        if par.id == par_id:
            campos_alterados = {}
            if payload.local_path is not None:
                campos_alterados["local_path"] = {"antes": par.local_path, "depois": payload.local_path}
                par.local_path = payload.local_path
            if payload.remote_path is not None:
                campos_alterados["remote_path"] = {"antes": par.remote_path, "depois": payload.remote_path}
                par.remote_path = payload.remote_path
            if payload.filtros is not None:
                campos_alterados["filtros"] = "atualizado"
                par.filtros = payload.filtros
            salvar_config(config)
            log_par_editado(par_id, campos_alterados)
            return {"mensagem": "Par atualizado", "par": par}
    raise HTTPException(status_code=404, detail="Par não encontrado")


@router.delete("/pares/{par_id}")
async def remover_par(par_id: str):
    config = carregar_config()
    par = next((p for p in config.pares if p.id == par_id), None)
    if not par:
        raise HTTPException(status_code=404, detail="Par não encontrado")
    config.pares = [p for p in config.pares if p.id != par_id]
    salvar_config(config)
    log_par_excluido(par_id, par.local_path, par.remote_name, par.remote_path)
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

# --- Navegação de diretórios (file picker) ---

@router.get("/dirs")
async def listar_dirs(path: str = "/home"):
    """
    Retorna subdiretórios de um caminho para o seletor de pasta local.
    Apenas diretórios legíveis pelo usuário atual.
    """
    import os
    from pathlib import Path as FSPath

    try:
        base = FSPath(path).expanduser().resolve()
        if not base.is_dir():
            raise HTTPException(status_code=400, detail="Caminho inválido ou não é um diretório.")

        entries = []
        try:
            for entry in sorted(base.iterdir()):
                if entry.is_dir() and not entry.name.startswith('.'):
                    entries.append({
                        "name": entry.name,
                        "path": str(entry),
                        "readable": os.access(entry, os.R_OK)
                    })
        except PermissionError:
            pass

        return {
            "current": str(base),
            "parent": str(base.parent) if base != base.parent else None,
            "dirs": entries
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
