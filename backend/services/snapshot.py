import subprocess
from pathlib import Path
from datetime import datetime


SNAPSHOT_BASE = Path("/var/tmp")


def criar_snapshot(local_path: str) -> dict:
    origem = Path(local_path)

    # Não cria snapshot de diretório vazio ou inexistente
    if not origem.exists() or not any(origem.iterdir()):
        return {
            "sucesso": True,
            "destino": None,
            "aviso": "Diretório vazio ou inexistente — snapshot ignorado"
        }

    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destino = SNAPSHOT_BASE / "rclone-bisync-snapshot" / data / origem.name
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