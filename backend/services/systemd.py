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