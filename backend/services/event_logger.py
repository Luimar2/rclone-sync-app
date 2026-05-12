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
"""
Issue 8 — Sistema de logs de eventos da aplicação.
Registra criação, edição, exclusão de pares e alterações de agendamento.
"""

import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path.home() / ".local" / "state" / "rclone-sync-app"
EVENT_LOG_FILE = LOG_DIR / "events.log"


def _registrar(tipo: str, descricao: str, dados: dict = None):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entrada = {
        "timestamp": datetime.now().isoformat(),
        "tipo": tipo,
        "descricao": descricao,
        "dados": dados or {}
    }
    with EVENT_LOG_FILE.open("a") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def log_par_criado(par_id: str, local_path: str, remote_name: str, remote_path: str):
    _registrar(
        "PAR_CRIADO",
        f"Par criado: {local_path} → {remote_name}:{remote_path}",
        {"par_id": par_id, "local_path": local_path,
         "remote_name": remote_name, "remote_path": remote_path}
    )


def log_par_editado(par_id: str, campos_alterados: dict):
    _registrar(
        "PAR_EDITADO",
        f"Par editado: {par_id}",
        {"par_id": par_id, "campos_alterados": campos_alterados}
    )


def log_par_excluido(par_id: str, local_path: str, remote_name: str, remote_path: str):
    _registrar(
        "PAR_EXCLUIDO",
        f"Par excluído: {local_path} → {remote_name}:{remote_path}",
        {"par_id": par_id, "local_path": local_path,
         "remote_name": remote_name, "remote_path": remote_path}
    )


def log_agendamento_alterado(acao: str, intervalo: str = "", horario_customizado: str = ""):
    _registrar(
        f"AGENDAMENTO_{acao.upper()}",
        f"Agendamento {acao}: intervalo={intervalo or '-'}",
        {"acao": acao, "intervalo": intervalo,
         "horario_customizado": horario_customizado}
    )


def listar_eventos(limite: int = 100) -> list[dict]:
    if not EVENT_LOG_FILE.exists():
        return []
    linhas = EVENT_LOG_FILE.read_text().splitlines()
    eventos = []
    for linha in reversed(linhas[-limite:]):
        try:
            eventos.append(json.loads(linha))
        except json.JSONDecodeError:
            continue
    return eventos
