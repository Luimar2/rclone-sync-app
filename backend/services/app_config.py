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
    provider: str = "gdrive"   # id do provider — padrão gdrive para retrocompatibilidade
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