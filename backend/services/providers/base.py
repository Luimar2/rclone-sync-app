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
providers/base.py
Contrato base que todo provider de cloud storage deve implementar.
Adicionar um novo provider = criar um arquivo que herda de CloudProvider.
"""

from abc import ABC, abstractmethod


class CloudProvider(ABC):

    # Identificador interno (ex: "gdrive", "onedrive")
    id: str

    # Nome exibido na interface
    label: str

    # Ícone PrimeIcons exibido na interface
    icon: str

    # Indica se o provider está disponível nesta versão
    disponivel: bool = False

    # Mensagem exibida quando disponivel=False
    indisponivel_motivo: str = ""

    # Tipo rclone esperado no campo "type" do config
    rclone_type: str

    @classmethod
    @abstractmethod
    def filtrar_remotes(cls, todos: list[str], executar_comando) -> list[str]:
        """
        Recebe a lista completa de remotes e retorna apenas os compatíveis
        com este provider.
        executar_comando é injetado para evitar importação circular.
        """
        ...

    @classmethod
    @abstractmethod
    def validar_remote(cls, nome: str, executar_comando) -> dict:
        """
        Verifica se o remote está acessível e retorna
        {"sucesso": bool, "info": str, "erro": str}
        """
        ...

    @classmethod
    def to_dict(cls) -> dict:
        return {
            "id":                 cls.id,
            "label":              cls.label,
            "icon":               cls.icon,
            "disponivel":         cls.disponivel,
            "indisponivel_motivo": cls.indisponivel_motivo,
            "rclone_type":        cls.rclone_type,
        }
