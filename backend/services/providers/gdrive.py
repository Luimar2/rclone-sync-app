"""
providers/gdrive.py
Provider Google Drive — único provider funcional na v0.1/v0.2.
"""

from .base import CloudProvider


class GoogleDriveProvider(CloudProvider):
    id            = "gdrive"
    label         = "Google Drive"
    icon          = "pi pi-google"
    disponivel    = True
    rclone_type   = "drive"

    @classmethod
    def filtrar_remotes(cls, todos: list[str], executar_comando) -> list[str]:
        """Retorna apenas remotes do tipo 'drive' configurados no rclone."""
        compatíveis = []
        for remote in todos:
            nome = remote.rstrip(":")
            check = executar_comando(["config", "show", nome])
            if check["sucesso"] and f"type = {cls.rclone_type}" in check["saida"]:
                compatíveis.append(remote)
        return compatíveis

    @classmethod
    def validar_remote(cls, nome: str, executar_comando) -> dict:
        """Verifica conectividade com o Google Drive via rclone about."""
        resultado = executar_comando(["about", f"{nome}:"])
        return {
            "sucesso": resultado["sucesso"],
            "info":    resultado["saida"],
            "erro":    resultado["erro"],
        }
