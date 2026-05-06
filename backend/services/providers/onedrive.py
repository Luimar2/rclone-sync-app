"""
providers/onedrive.py
Provider Microsoft OneDrive — esqueleto para implementação futura (v1.0).

Para ativar:
  1. Implementar filtrar_remotes e validar_remote
  2. Definir disponivel = True
  3. Registrar em providers/__init__.py

Notas de implementação futura:
  - rclone_type = "onedrive"
  - OAuth requer client_id e client_secret próprios (diferente do Drive)
  - Suporte a SharePoint e OneDrive for Business via flag --onedrive-drive-type
  - Considerar migração para Tauri antes de implementar (OAuth interativo)
"""

from .base import CloudProvider


class OneDriveProvider(CloudProvider):
    id                  = "onedrive"
    label               = "OneDrive"
    icon                = "pi pi-microsoft"
    disponivel          = False
    indisponivel_motivo = "Suporte a OneDrive está previsto para a v1.0."
    rclone_type         = "onedrive"

    @classmethod
    def filtrar_remotes(cls, todos: list[str], executar_comando) -> list[str]:
        # TODO v1.0: implementar filtro por type = onedrive
        raise NotImplementedError("OneDrive não disponível nesta versão.")

    @classmethod
    def validar_remote(cls, nome: str, executar_comando) -> dict:
        # TODO v1.0: implementar validação via rclone about
        raise NotImplementedError("OneDrive não disponível nesta versão.")
