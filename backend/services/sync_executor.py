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
import subprocess
import time
from pathlib import Path
from services.log_parser import detectar_tipo_erro


WORKDIR = Path.home() / ".local/share/rclone/bisync"
LOG_DIR = Path.home() / ".local/state/rclone-bisync"
RESYNC_FLAG_DIR = Path.home() / ".local/share/rclone-sync-app/resync-flags"


def flags_suportadas() -> list[str]:
    """Detecta a versão do rclone e retorna flags compatíveis."""
    resultado = subprocess.run(
        ["rclone", "--version"],
        capture_output=True, text=True
    )
    primeira_linha = resultado.stdout.splitlines()[0]
    import re
    match = re.search(r'v(\d+)\.(\d+)', primeira_linha)
    if not match:
        return []

    major = int(match.group(1))
    minor = int(match.group(2))

    flags = []
    # --recover e --resilient foram introduzidos no v1.64
    if (major, minor) >= (1, 64):
        flags += ["--recover", "--resilient"]

    return flags


def precisa_resync(local_path: str) -> bool:
    flag = RESYNC_FLAG_DIR / (local_path.replace("/", "_") + ".initialized")
    return not flag.exists()


def marcar_inicializado(local_path: str):
    RESYNC_FLAG_DIR.mkdir(parents=True, exist_ok=True)
    flag = RESYNC_FLAG_DIR / (local_path.replace("/", "_") + ".initialized")
    flag.touch()


def limpar_lock_rclone(local_path: str, remote_path: str):
    """Remove lockfile órfão do rclone bisync se existir."""
    import re
    session = re.sub(r'[/\\]', '_', local_path).strip('_')
    remote_clean = re.sub(r'[:/]', '_', remote_path).strip('_')
    lock_file = WORKDIR / f"{session}..{remote_clean}.lck"

    if lock_file.exists():
        subprocess.run(
            ["rclone", "deletefile", str(lock_file)],
            capture_output=True, text=True
        )


def executar_bisync(local_path: str, remote_path: str,
                    filtros_extras: list[str] = []) -> dict:
    WORKDIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    from datetime import datetime
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = LOG_DIR / f"rclone-bisync-{data}.log"

    # Primeira execução sempre usa --resync
    primeiro_sync = precisa_resync(local_path)

    if primeiro_sync:
        resultado = _rodar_bisync(
            local_path, remote_path, log_file,
            resync=True, filtros_extras=filtros_extras
        )
        if resultado["sucesso"]:
            marcar_inicializado(local_path)
        return {
            "sucesso": resultado["sucesso"],
            "log": str(log_file),
            "tentativas": 1,
            "resync_inicial": True
        }

    max_tentativas = 3

    for tentativa in range(1, max_tentativas + 1):
        resultado = _rodar_bisync(
            local_path, remote_path, log_file,
            filtros_extras=filtros_extras
        )

        if resultado["sucesso"]:
            return {
                "sucesso": True,
                "log": str(log_file),
                "tentativas": tentativa
            }

        conteudo = log_file.read_text(errors="ignore") if log_file.exists() else ""
        tipo_erro = detectar_tipo_erro(conteudo)

        if tipo_erro == "CRITICAL":
            resultado_resync = _rodar_bisync(
                local_path, remote_path, log_file,
                resync=True, filtros_extras=filtros_extras
            )
            return {
                "sucesso": resultado_resync["sucesso"],
                "log": str(log_file),
                "tentativas": tentativa,
                "resync": True
            }

        if tipo_erro == "TRANSIENT":
            espera = tentativa * 20
            time.sleep(espera)
            continue

        break

    return {"sucesso": False, "log": str(log_file), "tentativas": max_tentativas}


def _rodar_bisync(
    local_path: str,
    remote_path: str,
    log_file: Path,
    resync: bool = False,
    filtros_extras: list[str] = []
) -> dict:
    Path(local_path).mkdir(parents=True, exist_ok=True)
    limpar_lock_rclone(local_path, remote_path)

    args = [
        "rclone", "bisync",
        local_path, remote_path,
        "--log-file", str(log_file),
        "--log-level", "INFO",
        "--drive-skip-gdocs",
        "--workdir", str(WORKDIR),
    ] + flags_suportadas() + filtros_extras

    if resync:
        args.append("--resync")

    resultado = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return {"sucesso": resultado.returncode == 0}