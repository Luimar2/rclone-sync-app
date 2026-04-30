import subprocess
from pathlib import Path
from datetime import datetime

SNAPSHOT_BASE = Path("/var/tmp")
MAX_SNAPSHOTS = 3


def limpar_snapshots_antigos(nome_pasta: str):
    base = SNAPSHOT_BASE / "rclone-bisync-snapshot"
    if not base.exists():
        return
    snapshots = sorted(
        [d for d in base.iterdir() if (d / nome_pasta).exists()],
        key=lambda d: d.stat().st_mtime
    )
    while len(snapshots) > MAX_SNAPSHOTS - 1:
        import shutil
        shutil.rmtree(snapshots.pop(0))


def criar_snapshot(local_path: str) -> dict:
    origem = Path(local_path)

    if not origem.exists() or not any(origem.iterdir()):
        return {
            "sucesso": True,
            "destino": None,
            "aviso": "Diretório vazio ou inexistente — snapshot ignorado"
        }

    limpar_snapshots_antigos(origem.name)

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