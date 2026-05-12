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
tests/test_routes.py
Testes de integração das rotas FastAPI.
Usa TestClient — sem servidor real, sem rclone, sem systemd.
"""

import pytest
from unittest.mock import patch


# ─────────────────────────────────────────────
# GET /config/status
# ─────────────────────────────────────────────

class TestStatusRclone:
    def test_rclone_disponivel(self, client):
        with patch("routes.config.rclone_disponivel", return_value=True):
            res = client.get("/config/status")
            assert res.status_code == 200
            assert res.json()["rclone_disponivel"] is True

    def test_rclone_indisponivel(self, client):
        with patch("routes.config.rclone_disponivel", return_value=False):
            res = client.get("/config/status")
            assert res.status_code == 200
            assert res.json()["rclone_disponivel"] is False


# ─────────────────────────────────────────────
# GET /config/providers
# ─────────────────────────────────────────────

class TestProviders:
    def test_lista_providers(self, client):
        res = client.get("/config/providers")
        assert res.status_code == 200
        providers = res.json()["providers"]
        assert isinstance(providers, list)
        assert len(providers) >= 1

    def test_gdrive_esta_na_lista(self, client):
        res = client.get("/config/providers")
        ids = [p["id"] for p in res.json()["providers"]]
        assert "gdrive" in ids

    def test_onedrive_aparece_como_indisponivel(self, client):
        res = client.get("/config/providers")
        onedrive = next(p for p in res.json()["providers"] if p["id"] == "onedrive")
        assert onedrive["disponivel"] is False
        assert onedrive["indisponivel_motivo"] != ""


# ─────────────────────────────────────────────
# GET /config/remotes
# ─────────────────────────────────────────────

class TestRemotes:
    def test_lista_remotes_gdrive(self, client):
        with patch("routes.config.listar_remotes", return_value=["Drive:"]):
            res = client.get("/config/remotes?provider=gdrive")
            assert res.status_code == 200
            assert "Drive:" in res.json()["remotes"]
            assert res.json()["provider"] == "gdrive"

    def test_lista_vazia_quando_sem_remotes(self, client):
        with patch("routes.config.listar_remotes", return_value=[]):
            res = client.get("/config/remotes")
            assert res.status_code == 200
            assert res.json()["remotes"] == []
            assert res.json()["total"] == 0

    def test_provider_indisponivel_retorna_400(self, client):
        res = client.get("/config/remotes?provider=onedrive")
        assert res.status_code == 400

    def test_provider_desconhecido_retorna_400(self, client):
        res = client.get("/config/remotes?provider=dropbox")
        assert res.status_code == 400


# ─────────────────────────────────────────────
# GET /config/remotes/{nome}/verificar
# ─────────────────────────────────────────────

class TestVerificarRemote:
    def test_remote_valido_retorna_sucesso(self, client):
        with patch("routes.config.verificar_remote",
                   return_value={"sucesso": True, "info": "Total: 15G", "erro": ""}):
            res = client.get("/config/remotes/Drive/verificar?provider=gdrive")
            assert res.status_code == 200
            assert res.json()["sucesso"] is True

    def test_remote_invalido_retorna_400(self, client):
        with patch("routes.config.verificar_remote",
                   return_value={"sucesso": False, "info": "", "erro": "403 Forbidden"}):
            res = client.get("/config/remotes/Drive/verificar?provider=gdrive")
            assert res.status_code == 400
            assert "403" in res.json()["detail"]

    def test_provider_indisponivel_retorna_400(self, client):
        res = client.get("/config/remotes/Drive/verificar?provider=onedrive")
        assert res.status_code == 400


# ─────────────────────────────────────────────
# CRUD /config/pares
# ─────────────────────────────────────────────

class TestPares:
    def _payload(self, **kwargs):
        base = {
            "local_path": "/home/user/docs",
            "remote_name": "Drive",
            "remote_path": "/",
            "provider": "gdrive"
        }
        return {**base, **kwargs}

    def test_listar_pares_vazio(self, client):
        res = client.get("/config/pares")
        assert res.status_code == 200
        assert res.json()["pares"] == []

    def test_adicionar_par(self, client):
        res = client.post("/config/pares", json=self._payload())
        assert res.status_code == 200
        par = res.json()["par"]
        assert par["local_path"] == "/home/user/docs"
        assert par["provider"] == "gdrive"
        assert "id" in par

    def test_adicionar_par_persiste(self, client):
        client.post("/config/pares", json=self._payload())
        res = client.get("/config/pares")
        assert len(res.json()["pares"]) == 1

    def test_adicionar_multiplos_pares(self, client):
        client.post("/config/pares", json=self._payload(local_path="/docs"))
        client.post("/config/pares", json=self._payload(local_path="/fotos"))
        res = client.get("/config/pares")
        assert len(res.json()["pares"]) == 2

    def test_editar_par_local_path(self, client):
        add = client.post("/config/pares", json=self._payload())
        par_id = add.json()["par"]["id"]
        res = client.patch(f"/config/pares/{par_id}", json={"local_path": "/novo/path"})
        assert res.status_code == 200
        assert res.json()["par"]["local_path"] == "/novo/path"

    def test_editar_par_remote_path(self, client):
        add = client.post("/config/pares", json=self._payload())
        par_id = add.json()["par"]["id"]
        res = client.patch(f"/config/pares/{par_id}", json={"remote_path": "/backup"})
        assert res.status_code == 200
        assert res.json()["par"]["remote_path"] == "/backup"

    def test_editar_par_inexistente_retorna_404(self, client):
        res = client.patch("/config/pares/nao-existe", json={"local_path": "/x"})
        assert res.status_code == 404

    def test_excluir_par(self, client):
        add = client.post("/config/pares", json=self._payload())
        par_id = add.json()["par"]["id"]
        res = client.delete(f"/config/pares/{par_id}")
        assert res.status_code == 200
        lista = client.get("/config/pares")
        assert lista.json()["pares"] == []

    def test_excluir_par_inexistente_retorna_404(self, client):
        res = client.delete("/config/pares/nao-existe")
        assert res.status_code == 404

    def test_toggle_ativo_par(self, client):
        add = client.post("/config/pares", json=self._payload())
        par_id = add.json()["par"]["id"]
        res = client.patch(f"/config/pares/{par_id}/ativo?ativo=false")
        assert res.status_code == 200
        lista = client.get("/config/pares")
        par = lista.json()["pares"][0]
        assert par["ativo"] is False

    def test_toggle_ativo_par_inexistente_retorna_404(self, client):
        res = client.patch("/config/pares/nao-existe/ativo?ativo=true")
        assert res.status_code == 404


# ─────────────────────────────────────────────
# GET /config/dirs
# ─────────────────────────────────────────────

class TestDirs:
    def test_lista_subdiretorios(self, client, tmp_path):
        (tmp_path / "pasta_a").mkdir()
        (tmp_path / "pasta_b").mkdir()
        res = client.get(f"/config/dirs?path={tmp_path}")
        assert res.status_code == 200
        nomes = [d["name"] for d in res.json()["dirs"]]
        assert "pasta_a" in nomes
        assert "pasta_b" in nomes

    def test_caminho_invalido_retorna_400(self, client):
        res = client.get("/config/dirs?path=/caminho/que/nao/existe/nunca")
        assert res.status_code == 400

    def test_retorna_caminho_atual_e_parent(self, client, tmp_path):
        res = client.get(f"/config/dirs?path={tmp_path}")
        assert res.status_code == 200
        data = res.json()
        assert "current" in data
        assert "parent" in data
        assert "dirs" in data

    def test_pastas_ocultas_nao_aparecem(self, client, tmp_path):
        (tmp_path / ".oculta").mkdir()
        (tmp_path / "visivel").mkdir()
        res = client.get(f"/config/dirs?path={tmp_path}")
        nomes = [d["name"] for d in res.json()["dirs"]]
        assert ".oculta" not in nomes
        assert "visivel" in nomes


# ─────────────────────────────────────────────
# POST /agendamento/instalar
# ─────────────────────────────────────────────

class TestAgendamento:
    def test_instalar_intervalo_valido(self, client):
        with patch("routes.agendamento.instalar_systemd",
                   return_value={"sucesso": True, "mensagem": "Timer instalado e ativo"}):
            res = client.post("/agendamento/instalar", json={"intervalo": "daily"})
            assert res.status_code == 200

    def test_instalar_intervalo_invalido_retorna_400(self, client):
        res = client.post("/agendamento/instalar", json={"intervalo": "semanal"})
        assert res.status_code == 400
        assert "Intervalo inválido" in res.json()["detail"]

    def test_custom_sem_horario_retorna_400(self, client):
        res = client.post("/agendamento/instalar",
                          json={"intervalo": "custom", "horario_customizado": ""})
        assert res.status_code == 400
        assert "customizado" in res.json()["detail"].lower()

    def test_custom_com_horario_valido(self, client):
        with patch("routes.agendamento.instalar_systemd",
                   return_value={"sucesso": True, "mensagem": "Timer instalado e ativo"}):
            res = client.post("/agendamento/instalar",
                              json={"intervalo": "custom",
                                    "horario_customizado": "*-*-* 02:00:00"})
            assert res.status_code == 200

    def test_desativar_agendamento(self, client):
        with patch("routes.agendamento.desativar_systemd",
                   return_value={"sucesso": True, "mensagem": "Timer desativado"}):
            res = client.post("/agendamento/desativar")
            assert res.status_code == 200

    def test_falha_no_systemd_retorna_500(self, client):
        with patch("routes.agendamento.instalar_systemd",
                   return_value={"sucesso": False, "erro": "systemd não disponível"}):
            res = client.post("/agendamento/instalar", json={"intervalo": "daily"})
            assert res.status_code == 500


# ─────────────────────────────────────────────
# GET /logs/eventos
# ─────────────────────────────────────────────

class TestLogsEventos:
    def test_lista_eventos_vazio(self, client):
        res = client.get("/logs/eventos")
        assert res.status_code == 200
        assert res.json()["eventos"] == []

    def test_lista_eventos_apos_criacao_de_par(self, client):
        client.post("/config/pares", json={
            "local_path": "/docs",
            "remote_name": "Drive",
            "remote_path": "/",
            "provider": "gdrive"
        })
        res = client.get("/logs/eventos")
        assert res.status_code == 200
        tipos = [e["tipo"] for e in res.json()["eventos"]]
        assert "PAR_CRIADO" in tipos
