import subprocess
import time
from pathlib import Path
from services.log_parser import detectar_tipo_erro


WORKDIR = Path.home() / ".local/share/rclone/bisync"
LOG_DIR = Path.home() / ".local/state/rclone-bisync"
RESYNC_FLAG_DIR = Path.home() / ".local/share/rclone-sync-app/resync-flags"


def precisa_resync(local_path: str) -> bool:
    flag = RESYNC_FLAG_DIR / (local_path.replace("/", "_") + ".initialized")
    return not flag.exists()


def marcar_inicializado(local_path: str):
    RESYNC_FLAG_DIR.mkdir(parents=True, exist_ok=True)
    flag = RESYNC_FLAG_DIR / (local_path.replace("/", "_") + ".initialized")
    flag.touch()


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
    # Cria o diretório local se não existir
    Path(local_path).mkdir(parents=True, exist_ok=True)

    args = [
        "rclone", "bisync",
        local_path, remote_path,
        "--log-file", str(log_file),
        "--log-level", "INFO",
        "--drive-skip-gdocs",
        "--recover",
        "--resilient",
        "--workdir", str(WORKDIR),
    ] + filtros_extras

    if resync:
        args.append("--resync")

    resultado = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return {"sucesso": resultado.returncode == 0}