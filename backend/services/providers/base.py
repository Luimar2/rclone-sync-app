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
