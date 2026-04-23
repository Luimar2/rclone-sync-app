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


def criar_remote_gdrive(nome: str) -> dict:
    resultado = executar_comando([
        "config", "create", nome, "drive",
        "scope", "drive",
        "--auto-confirm"
    ])
    return resultado


def verificar_remote(nome: str) -> dict:
    resultado = executar_comando(["about", f"{nome}:"])
    return {
        "sucesso": resultado["sucesso"],
        "info": resultado["saida"],
        "erro": resultado["erro"]
    }


def deletar_remote(nome: str) -> dict:
    resultado = executar_comando(["config", "delete", nome])
    return resultado