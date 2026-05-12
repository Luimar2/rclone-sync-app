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
providers/__init__.py
Registro central de providers disponíveis.
Para adicionar um novo provider: importar e inserir em PROVIDERS.
A ordem define a exibição na interface.
"""

from .gdrive   import GoogleDriveProvider
from .onedrive import OneDriveProvider

PROVIDERS: list = [
    GoogleDriveProvider,
    OneDriveProvider,
]

def get_provider(provider_id: str):
    """Retorna o provider pelo id ou None se não encontrado."""
    return next((p for p in PROVIDERS if p.id == provider_id), None)

def get_provider_disponivel(provider_id: str):
    """Retorna o provider se disponível, ou levanta ValueError."""
    provider = get_provider(provider_id)
    if provider is None:
        raise ValueError(f"Provider '{provider_id}' não encontrado.")
    if not provider.disponivel:
        raise ValueError(provider.indisponivel_motivo)
    return provider
