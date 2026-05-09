"""
tests/test_providers.py
Testes unitários do sistema de providers (Issue #12).
Cobre: registro, filtro, validação e contrato da classe base.
"""

import pytest
from unittest.mock import patch, MagicMock


# ─────────────────────────────────────────────
# Registro central de providers
# ─────────────────────────────────────────────

class TestRegistroProviders:
    def test_gdrive_esta_registrado(self):
        from services.providers import PROVIDERS
        ids = [p.id for p in PROVIDERS]
        assert "gdrive" in ids

    def test_onedrive_esta_registrado(self):
        from services.providers import PROVIDERS
        ids = [p.id for p in PROVIDERS]
        assert "onedrive" in ids

    def test_get_provider_retorna_gdrive(self):
        from services.providers import get_provider
        p = get_provider("gdrive")
        assert p is not None
        assert p.id == "gdrive"

    def test_get_provider_retorna_none_para_desconhecido(self):
        from services.providers import get_provider
        assert get_provider("dropbox") is None

    def test_get_provider_disponivel_retorna_gdrive(self):
        from services.providers import get_provider_disponivel
        p = get_provider_disponivel("gdrive")
        assert p.disponivel is True

    def test_get_provider_disponivel_levanta_para_onedrive(self):
        from services.providers import get_provider_disponivel
        with pytest.raises(ValueError, match="v1.0"):
            get_provider_disponivel("onedrive")

    def test_get_provider_disponivel_levanta_para_desconhecido(self):
        from services.providers import get_provider_disponivel
        with pytest.raises(ValueError, match="não encontrado"):
            get_provider_disponivel("s3")


# ─────────────────────────────────────────────
# GoogleDriveProvider
# ─────────────────────────────────────────────

class TestGoogleDriveProvider:
    def test_atributos_basicos(self):
        from services.providers.gdrive import GoogleDriveProvider
        assert GoogleDriveProvider.id == "gdrive"
        assert GoogleDriveProvider.disponivel is True
        assert GoogleDriveProvider.rclone_type == "drive"

    def test_to_dict_retorna_campos_esperados(self):
        from services.providers.gdrive import GoogleDriveProvider
        d = GoogleDriveProvider.to_dict()
        assert d["id"] == "gdrive"
        assert d["label"] == "Google Drive"
        assert d["disponivel"] is True
        assert "icon" in d

    def test_filtrar_remotes_retorna_apenas_drive(self):
        from services.providers.gdrive import GoogleDriveProvider

        def fake_executar(args):
            nome = args[2] if len(args) > 2 else ""
            if nome == "GDrive":
                return {"sucesso": True, "saida": "type = drive\nscope = drive\n", "erro": ""}
            return {"sucesso": True, "saida": "type = ftp\n", "erro": ""}

        todos = ["GDrive:", "FTPServer:"]
        resultado = GoogleDriveProvider.filtrar_remotes(todos, fake_executar)
        assert "GDrive:" in resultado
        assert "FTPServer:" not in resultado

    def test_filtrar_remotes_lista_vazia(self):
        from services.providers.gdrive import GoogleDriveProvider
        resultado = GoogleDriveProvider.filtrar_remotes([], lambda args: {})
        assert resultado == []

    def test_filtrar_remotes_sem_drive_retorna_vazio(self):
        from services.providers.gdrive import GoogleDriveProvider

        def fake_executar(args):
            return {"sucesso": True, "saida": "type = s3\n", "erro": ""}

        resultado = GoogleDriveProvider.filtrar_remotes(["S3Bucket:"], fake_executar)
        assert resultado == []

    def test_validar_remote_sucesso(self):
        from services.providers.gdrive import GoogleDriveProvider

        def fake_executar(args):
            return {"sucesso": True, "saida": "Total: 15G\nUsed: 5G\n", "erro": ""}

        resultado = GoogleDriveProvider.validar_remote("Drive", fake_executar)
        assert resultado["sucesso"] is True
        assert "Total" in resultado["info"]

    def test_validar_remote_falha(self):
        from services.providers.gdrive import GoogleDriveProvider

        def fake_executar(args):
            return {"sucesso": False, "saida": "", "erro": "403 Forbidden"}

        resultado = GoogleDriveProvider.validar_remote("Drive", fake_executar)
        assert resultado["sucesso"] is False
        assert "403" in resultado["erro"]


# ─────────────────────────────────────────────
# OneDriveProvider (esqueleto)
# ─────────────────────────────────────────────

class TestOneDriveProvider:
    def test_atributos_basicos(self):
        from services.providers.onedrive import OneDriveProvider
        assert OneDriveProvider.id == "onedrive"
        assert OneDriveProvider.disponivel is False
        assert OneDriveProvider.rclone_type == "onedrive"

    def test_indisponivel_motivo_preenchido(self):
        from services.providers.onedrive import OneDriveProvider
        assert OneDriveProvider.indisponivel_motivo != ""

    def test_to_dict_expoe_disponivel_false(self):
        from services.providers.onedrive import OneDriveProvider
        d = OneDriveProvider.to_dict()
        assert d["disponivel"] is False
        assert d["indisponivel_motivo"] != ""

    def test_filtrar_remotes_levanta_not_implemented(self):
        from services.providers.onedrive import OneDriveProvider
        with pytest.raises(NotImplementedError):
            OneDriveProvider.filtrar_remotes(["OneDrive:"], lambda x: {})

    def test_validar_remote_levanta_not_implemented(self):
        from services.providers.onedrive import OneDriveProvider
        with pytest.raises(NotImplementedError):
            OneDriveProvider.validar_remote("OneDrive", lambda x: {})
