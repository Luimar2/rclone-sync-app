import subprocess
import time
from pathlib import Path
from services.log_parser import detectar_tipo_erro


WORKDIR = Path.home() / ".local/share/rclone/bisync"
LOG_DIR = Path.home() / ".local/state/rclone-bisync"


def executar_bisync(local_path: str, remote_path: str) -> dict:
    WORKDIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    from datetime import datetime
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = LOG_DIR / f"rclone-bisync-{data}.log"

    max_tentativas = 3

    for tentativa in range(1, max_tentativas + 1):
        resultado = _rodar_bisync(local_path, remote_path, log_file)

        if resultado["sucesso"]:
            return {"sucesso": True, "log": str(log_file), "tentativas": tentativa}

        conteudo = log_file.read_text(errors="ignore") if log_file.exists() else ""
        tipo_erro = detectar_tipo_erro(conteudo)

        if tipo_erro == "CRITICAL":
            resultado_resync = _rodar_bisync(
                local_path, remote_path, log_file, resync=True
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
    resync: bool = False
) -> dict:
    args = [
        "rclone", "bisync",
        local_path, remote_path,
        "--log-file", str(log_file),
        "--log-level", "INFO",
        "--drive-skip-gdocs",
        "--recover",
        "--resilient",
        "--workdir", str(WORKDIR),
    ]

    if resync:
        args.append("--resync")

    resultado = subprocess.run(args, capture_output=True, text=True, timeout=300)

    return {"sucesso": resultado.returncode == 0}