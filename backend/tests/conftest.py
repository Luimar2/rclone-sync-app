"""
conftest.py — fixtures compartilhadas entre todos os testes.
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient

# Garante que o backend está no path do Python
sys.path.insert(0, str(Path(__file__).parent.parent))


# --- Fixtures de filesystem isolado ---

@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    """
    Redireciona CONFIG_FILE e EVENT_LOG_FILE para diretórios temporários.
    Garante que os testes não leem nem escrevem na config real do usuário.
    """
    config_dir = tmp_path / "config"
    log_dir    = tmp_path / "logs"
    config_dir.mkdir()
    log_dir.mkdir()

    import services.app_config as app_config
    import services.event_logger as event_logger

    monkeypatch.setattr(app_config, "CONFIG_DIR",  config_dir)
    monkeypatch.setattr(app_config, "CONFIG_FILE", config_dir / "config.json")
    monkeypatch.setattr(event_logger, "LOG_DIR",         log_dir)
    monkeypatch.setattr(event_logger, "EVENT_LOG_FILE",  log_dir / "events.log")

    return {"config_dir": config_dir, "log_dir": log_dir}


# --- Fixture do TestClient da API ---

@pytest.fixture
def client(tmp_config):
    """Cliente HTTP para testes de integração das rotas FastAPI."""
    from main import app
    with TestClient(app) as c:
        yield c


# --- Fixtures de mock do rclone ---

@pytest.fixture
def mock_rclone_disponivel():
    with patch("routes.config.rclone_disponivel", return_value=True):
        yield


@pytest.fixture
def mock_rclone_indisponivel():
    with patch("routes.config.rclone_disponivel", return_value=False):
        yield


@pytest.fixture
def mock_executar_comando():
    """Mock configurável do executar_comando — padrão retorna sucesso."""
    with patch("services.rclone.executar_comando") as mock:
        mock.return_value = {"sucesso": True, "saida": "", "erro": ""}
        yield mock
