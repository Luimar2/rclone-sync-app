"""
services/rclone.py
Camada de execução do rclone. Lógica específica de provider
foi movida para services/providers/.
"""

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
            "saida":   resultado.stdout.strip(),
            "erro":    resultado.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {"sucesso": False, "saida": "", "erro": "Tempo limite excedido"}
    except Exception as e:
        return {"sucesso": False, "saida": "", "erro": str(e)}


def listar_remotes_brutos() -> list[str]:
    """Retorna todos os remotes configurados no rclone, sem filtro de provider."""
    resultado = executar_comando(["listremotes"])
    if not resultado["sucesso"] or not resultado["saida"]:
        return []
    return [r.strip() for r in resultado["saida"].splitlines()]


def listar_remotes_por_provider(provider_id: str) -> list[str]:
    """
    Retorna remotes filtrados pelo provider informado.
    Substitui o antigo listar_remotes() — agora ciente de provider.
    """
    from services.providers import get_provider_disponivel
    provider = get_provider_disponivel(provider_id)
    todos = listar_remotes_brutos()
    return provider.filtrar_remotes(todos, executar_comando)


def listar_remotes(provider_id: str = "gdrive") -> list[str]:
    """
    Compatibilidade com código legado.
    Chama listar_remotes_por_provider com gdrive como padrão.
    """
    return listar_remotes_por_provider(provider_id)


def verificar_remote(nome: str, provider_id: str = "gdrive") -> dict:
    """Valida o remote usando o provider correto."""
    from services.providers import get_provider_disponivel
    provider = get_provider_disponivel(provider_id)
    return provider.validar_remote(nome, executar_comando)


def criar_remote_gdrive(nome: str) -> dict:
    resultado = executar_comando([
        "config", "create", nome, "drive",
        "scope", "drive",
        "--auto-confirm"
    ])
    return resultado


def deletar_remote(nome: str) -> dict:
    return executar_comando(["config", "delete", nome])
