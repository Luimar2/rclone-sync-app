from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.systemd import (
    instalar_systemd,
    status_systemd,
    desativar_systemd,
    proxima_execucao
)
from services.app_config import carregar_config, salvar_config
from services.event_logger import log_agendamento_alterado

router = APIRouter(prefix="/agendamento", tags=["Agendamento"])


INTERVALOS_VALIDOS = ["1h", "6h", "12h", "daily", "custom"]


class AgendamentoRequest(BaseModel):
    intervalo: str
    horario_customizado: str = ""


@router.post("/instalar")
async def instalar(payload: AgendamentoRequest):
    if payload.intervalo not in INTERVALOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Intervalo inválido. Opções: {INTERVALOS_VALIDOS}"
        )

    if payload.intervalo == "custom" and not payload.horario_customizado:
        raise HTTPException(
            status_code=400,
            detail="Horário customizado é obrigatório quando intervalo é 'custom'"
        )

    resultado = instalar_systemd(payload.intervalo, payload.horario_customizado)

    if not resultado["sucesso"]:
        raise HTTPException(status_code=500, detail=resultado["erro"])

    config = carregar_config()
    config.agendamento.intervalo = payload.intervalo
    config.agendamento.horario_customizado = payload.horario_customizado
    config.agendamento.ativo = True
    salvar_config(config)
    log_agendamento_alterado("instalado", payload.intervalo, payload.horario_customizado)

    return resultado


@router.get("/status")
async def get_status():
    return status_systemd()


@router.get("/proxima-execucao")
async def get_proxima_execucao():
    return proxima_execucao()


@router.post("/desativar")
async def desativar():
    resultado = desativar_systemd()
    if not resultado["sucesso"]:
        raise HTTPException(status_code=500, detail=resultado["erro"])

    config = carregar_config()
    config.agendamento.ativo = False
    salvar_config(config)
    log_agendamento_alterado("desativado")

    return resultado