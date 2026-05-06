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
