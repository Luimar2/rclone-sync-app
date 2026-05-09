"""
tests/test_services.py
Testes unitários dos serviços core: rclone, app_config e event_logger.
Nenhum teste depende de rclone instalado ou systemd.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


# ─────────────────────────────────────────────
# services/rclone.py
# ─────────────────────────────────────────────

class TestRcloneDisponivel:
    def test_retorna_true_quando_rclone_existe(self):
        with patch("shutil.which", return_value="/usr/bin/rclone"):
            from services.rclone import rclone_disponivel
            assert rclone_disponivel() is True

    def test_retorna_false_quando_rclone_ausente(self):
        with patch("shutil.which", return_value=None):
            from services.rclone import rclone_disponivel
            assert rclone_disponivel() is False


class TestExecutarComando:
    def test_retorna_erro_quando_rclone_indisponivel(self):
        with patch("services.rclone.rclone_disponivel", return_value=False):
            from services.rclone import executar_comando
            resultado = executar_comando(["listremotes"])
            assert resultado["sucesso"] is False
            assert "rclone" in resultado["erro"].lower()

    def test_retorna_saida_em_sucesso(self):
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.stdout = "GoogleDrive:\n"
        mock_proc.stderr = ""
        with patch("services.rclone.rclone_disponivel", return_value=True), \
             patch("subprocess.run", return_value=mock_proc):
            from services.rclone import executar_comando
            resultado = executar_comando(["listremotes"])
            assert resultado["sucesso"] is True
            assert "GoogleDrive" in resultado["saida"]

    def test_retorna_erro_em_timeout(self):
        import subprocess
        with patch("services.rclone.rclone_disponivel", return_value=True), \
             patch("subprocess.run", side_effect=subprocess.TimeoutExpired("rclone", 30)):
            from services.rclone import executar_comando
            resultado = executar_comando(["listremotes"])
            assert resultado["sucesso"] is False
            assert "limite" in resultado["erro"].lower()

    def test_retorna_erro_em_excecao_generica(self):
        with patch("services.rclone.rclone_disponivel", return_value=True), \
             patch("subprocess.run", side_effect=OSError("Permissão negada")):
            from services.rclone import executar_comando
            resultado = executar_comando(["listremotes"])
            assert resultado["sucesso"] is False
            assert resultado["erro"] != ""


class TestListarRemotesBrutos:
    def test_retorna_lista_de_remotes(self):
        with patch("services.rclone.executar_comando",
                   return_value={"sucesso": True, "saida": "Drive:\nOneDrive:\n", "erro": ""}):
            from services.rclone import listar_remotes_brutos
            resultado = listar_remotes_brutos()
            assert "Drive:" in resultado
            assert "OneDrive:" in resultado

    def test_retorna_lista_vazia_quando_sem_remotes(self):
        with patch("services.rclone.executar_comando",
                   return_value={"sucesso": True, "saida": "", "erro": ""}):
            from services.rclone import listar_remotes_brutos
            assert listar_remotes_brutos() == []

    def test_retorna_lista_vazia_quando_falha(self):
        with patch("services.rclone.executar_comando",
                   return_value={"sucesso": False, "saida": "", "erro": "erro"}):
            from services.rclone import listar_remotes_brutos
            assert listar_remotes_brutos() == []


class TestListarRemotesPorProvider:
    def test_provider_inexistente_levanta_value_error(self):
        from services.rclone import listar_remotes_por_provider
        with pytest.raises(ValueError, match="não encontrado"):
            listar_remotes_por_provider("dropbox")

    def test_provider_indisponivel_levanta_value_error(self):
        from services.rclone import listar_remotes_por_provider
        with pytest.raises(ValueError):
            listar_remotes_por_provider("onedrive")

    def test_gdrive_filtra_apenas_remotes_drive(self):
        def fake_executar(args):
            if args[0] == "listremotes":
                return {"sucesso": True, "saida": "Drive:\nFTP:\n", "erro": ""}
            if args[0] == "config" and args[1] == "show":
                nome = args[2]
                if nome == "Drive":
                    return {"sucesso": True, "saida": "type = drive\n", "erro": ""}
                return {"sucesso": True, "saida": "type = ftp\n", "erro": ""}
            return {"sucesso": True, "saida": "", "erro": ""}

        with patch("services.rclone.executar_comando", side_effect=fake_executar):
            from services.rclone import listar_remotes_por_provider
            resultado = listar_remotes_por_provider("gdrive")
            assert "Drive:" in resultado
            assert "FTP:" not in resultado


# ─────────────────────────────────────────────
# services/app_config.py
# ─────────────────────────────────────────────

class TestAppConfig:
    def test_config_inicial_criada_com_defaults(self, tmp_config):
        from services.app_config import carregar_config
        config = carregar_config()
        assert config.pares == []
        assert config.agendamento.ativo is False
        assert config.agendamento.intervalo == "daily"

    def test_salvar_e_carregar_config(self, tmp_config):
        from services.app_config import (
            carregar_config, salvar_config,
            ParSincronizacao, AppConfig
        )
        config = AppConfig(pares=[
            ParSincronizacao(
                id="abc-123",
                local_path="/home/user/docs",
                remote_name="Drive",
                remote_path="/",
                provider="gdrive"
            )
        ])
        salvar_config(config)
        carregada = carregar_config()
        assert len(carregada.pares) == 1
        assert carregada.pares[0].id == "abc-123"
        assert carregada.pares[0].provider == "gdrive"

    def test_par_sem_provider_usa_gdrive_como_padrao(self, tmp_config):
        """Retrocompatibilidade: config antiga sem campo provider."""
        from services import app_config
        config_json = json.dumps({
            "pares": [{
                "id": "xyz",
                "local_path": "/tmp",
                "remote_name": "Drive",
                "remote_path": "/",
                "filtros": {},
                "ativo": True
                # sem campo "provider"
            }],
            "agendamento": {"intervalo": "daily", "horario_customizado": "", "ativo": False}
        })
        app_config.CONFIG_FILE.write_text(config_json)
        config = app_config.carregar_config()
        assert config.pares[0].provider == "gdrive"

    def test_config_persiste_em_disco(self, tmp_config):
        from services.app_config import carregar_config, salvar_config
        config = carregar_config()
        config.agendamento.intervalo = "6h"
        config.agendamento.ativo = True
        salvar_config(config)

        from services import app_config
        raw = json.loads(app_config.CONFIG_FILE.read_text())
        assert raw["agendamento"]["intervalo"] == "6h"
        assert raw["agendamento"]["ativo"] is True


# ─────────────────────────────────────────────
# services/event_logger.py
# ─────────────────────────────────────────────

class TestEventLogger:
    def test_log_par_criado_grava_evento(self, tmp_config):
        from services.event_logger import log_par_criado, listar_eventos
        log_par_criado("id-1", "/home/docs", "Drive", "/")
        eventos = listar_eventos()
        assert len(eventos) == 1
        assert eventos[0]["tipo"] == "PAR_CRIADO"
        assert eventos[0]["dados"]["par_id"] == "id-1"

    def test_log_par_editado_grava_evento(self, tmp_config):
        from services.event_logger import log_par_editado, listar_eventos
        log_par_editado("id-2", {"local_path": {"antes": "/a", "depois": "/b"}})
        eventos = listar_eventos()
        assert eventos[0]["tipo"] == "PAR_EDITADO"

    def test_log_par_excluido_grava_evento(self, tmp_config):
        from services.event_logger import log_par_excluido, listar_eventos
        log_par_excluido("id-3", "/home/docs", "Drive", "/")
        eventos = listar_eventos()
        assert eventos[0]["tipo"] == "PAR_EXCLUIDO"

    def test_log_agendamento_instalado(self, tmp_config):
        from services.event_logger import log_agendamento_alterado, listar_eventos
        log_agendamento_alterado("instalado", "daily")
        eventos = listar_eventos()
        assert eventos[0]["tipo"] == "AGENDAMENTO_INSTALADO"

    def test_listar_eventos_sem_arquivo_retorna_vazio(self, tmp_config):
        from services.event_logger import listar_eventos
        eventos = listar_eventos()
        assert eventos == []

    def test_listar_eventos_respeita_limite(self, tmp_config):
        from services.event_logger import log_par_criado, listar_eventos
        for i in range(10):
            log_par_criado(f"id-{i}", f"/path/{i}", "Drive", "/")
        eventos = listar_eventos(limite=5)
        assert len(eventos) == 5

    def test_linha_corrompida_no_log_e_ignorada(self, tmp_config):
        from services import event_logger
        from services.event_logger import log_par_criado, listar_eventos
        log_par_criado("id-ok", "/docs", "Drive", "/")
        # Injeta linha corrompida
        with event_logger.EVENT_LOG_FILE.open("a") as f:
            f.write("LINHA CORROMPIDA NÃO É JSON\n")
        eventos = listar_eventos()
        assert len(eventos) == 1
        assert eventos[0]["dados"]["par_id"] == "id-ok"
