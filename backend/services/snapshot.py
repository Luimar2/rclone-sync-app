import subprocess
from pathlib import Path
from datetime import datetime


SNAPSHOT_BASE = Path("/var/tmp")


def criar_snapshot(local_path: str) -> dict:
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    origem = Path(local_path)
    destino = SNAPSHOT_BASE / f"rclone-bisync-snapshot" / data / origem.name

    destino.mkdir(parents=True, exist_ok=True)

    resultado = subprocess.run(
        ["rsync", "-a", f"{local_path}/", str(destino) + "/"],
        capture_output=True,
        text=True
    )

    return {
        "sucesso": resultado.returncode == 0,
        "destino": str(destino),
        "erro": resultado.stderr.strip()
    }