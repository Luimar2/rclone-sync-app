import subprocess
import shutil
from pathlib import Path


def rclone_disponivel() -> bool:
    return shutil.which("rclone") is not None


def executar_comando(args: list[str]) -> dict:
    if not rclone_disponivel():
        return {"sucesso": False, "saida": "", "erro": "rclone não encontrado no sistema"}

    try:
        resultado = subprocess.run(
            ["rclone"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "sucesso": resultado.returncode == 0,
            "saida": resultado.stdout.strip(),
            "erro": resultado.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {"sucesso": False, "saida": "", "erro": "Tempo limite excedido"}
    except Exception as e:
        return {"sucesso": False, "saida": "", "erro": str(e)}


def listar_remotes() -> list[str]:
    resultado = executar_comando(["listremotes"])
    if not resultado["sucesso"] or not resultado["saida"]:
        return []
    return [r.strip() for r in resultado["saida"].splitlines()]