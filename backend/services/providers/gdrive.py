# RcloneSync - Interface gráfica para rclone com Google Drive no Linux
# Copyright (C) 2026 Luimar2
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
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
