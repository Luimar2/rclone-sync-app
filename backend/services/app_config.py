import json
from pathlib import Path
from pydantic import BaseModel


CONFIG_DIR = Path.home() / ".config" / "rclone-sync-app"
CONFIG_FILE = CONFIG_DIR / "config.json"


class FiltrosSinc(BaseModel):
    arquivos_temporarios: bool = True
    lixeira: bool = True
    cache: bool = True
    git: bool = True
    arquivos_ocultos: bool = False
    avancado: str = ""


class ParSincronizacao(BaseModel):
    id: str
    local_path: str
    remote_name: str
    remote_path: str
    filtros: FiltrosSinc = FiltrosSinc()
    ativo: bool = True


class AgendamentoConfig(BaseModel):
    intervalo: str = "daily"
    horario_customizado: str = ""
    ativo: bool = False


class AppConfig(BaseModel):
    pares: list[ParSincronizacao] = []
    agendamento: AgendamentoConfig = AgendamentoConfig()


def carregar_config() -> AppConfig:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        salvar_config(AppConfig())
    return AppConfig.model_validate_json(CONFIG_FILE.read_text())


def salvar_config(config: AppConfig) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(config.model_dump_json(indent=2))