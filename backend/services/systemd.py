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
from pathlib import Path
import subprocess


SYSTEMD_DIR = Path.home() / ".config" / "systemd" / "user"
SERVICE_NAME = "rclone-sync-app"


INTERVALOS = {
    "1h":    "OnUnitActiveSec=1h",
    "6h":    "OnUnitActiveSec=6h",
    "12h":   "OnUnitActiveSec=12h",
    "daily": "OnCalendar=daily",
    "custom": None
}


def _conteudo_service() -> str:
    return """[Unit]
Description=RcloneSync App — sincronização agendada
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'curl -s -X POST http://localhost:8000/sync/executar-todos'
StandardOutput=journal
StandardError=journal
"""


def _conteudo_timer(intervalo: str, horario_customizado: str = "") -> str:
    if intervalo == "custom" and horario_customizado:
        agendamento = f"OnCalendar={horario_customizado}"
    else:
        agendamento = INTERVALOS.get(intervalo, "OnCalendar=daily")

    return f"""[Unit]
Description=RcloneSync App — timer de sincronização

[Timer]
{agendamento}
Persistent=true

[Install]
WantedBy=timers.target
"""


def instalar_systemd(intervalo: str, horario_customizado: str = "") -> dict:
    try:
        SYSTEMD_DIR.mkdir(parents=True, exist_ok=True)

        service_file = SYSTEMD_DIR / f"{SERVICE_NAME}.service"
        timer_file = SYSTEMD_DIR / f"{SERVICE_NAME}.timer"

        service_file.write_text(_conteudo_service())
        timer_file.write_text(_conteudo_timer(intervalo, horario_customizado))

        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "--user", "enable", "--now",
                        f"{SERVICE_NAME}.timer"], check=True)

        return {"sucesso": True, "mensagem": "Timer instalado e ativo"}

    except subprocess.CalledProcessError as e:
        return {"sucesso": False, "erro": str(e)}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}


def status_systemd() -> dict:
    resultado = subprocess.run(
        ["systemctl", "--user", "status", f"{SERVICE_NAME}.timer"],
        capture_output=True,
        text=True
    )
    ativo = resultado.returncode == 0
    return {
        "ativo": ativo,
        "detalhes": resultado.stdout.strip()
    }


def desativar_systemd() -> dict:
    try:
        subprocess.run(
            ["systemctl", "--user", "disable", "--now", f"{SERVICE_NAME}.timer"],
            check=True
        )
        return {"sucesso": True, "mensagem": "Timer desativado"}
    except subprocess.CalledProcessError as e:
        return {"sucesso": False, "erro": str(e)}


def proxima_execucao() -> dict:
    resultado = subprocess.run(
        ["systemctl", "--user", "list-timers", f"{SERVICE_NAME}.timer"],
        capture_output=True,
        text=True
    )
    return {"info": resultado.stdout.strip()}