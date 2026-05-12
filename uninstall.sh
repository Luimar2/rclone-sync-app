#!/usr/bin/env bash
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


VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
RESET='\033[0m'

ok()   { echo -e "${VERDE}✅ $1${RESET}"; }
info() { echo -e "${AMARELO}➡️  $1${RESET}"; }

echo ""
echo "================================"
echo "   RcloneSync — Desinstalação"
echo "================================"
echo ""

# Confirmação
read -r -p "Tem certeza que deseja desinstalar o RcloneSync? [s/N] " confirm
if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
  echo "Desinstalação cancelada."
  exit 0
fi

# Para e desativa os serviços
info "Parando serviços..."
systemctl --user disable --now rclone-sync-app-web.service 2>/dev/null || true
systemctl --user disable --now rclone-sync-app.timer 2>/dev/null || true
systemctl --user daemon-reload
ok "Serviços parados."

# Remove arquivos do app
info "Removendo arquivos do app..."
rm -rf "$HOME/.local/share/rclone-sync-app"
ok "Arquivos removidos."

# Remove arquivos systemd
info "Removendo serviços systemd..."
rm -f "$HOME/.config/systemd/user/rclone-sync-app-web.service"
rm -f "$HOME/.config/systemd/user/rclone-sync-app.timer"
rm -f "$HOME/.config/systemd/user/rclone-sync-app.service"
systemctl --user daemon-reload
ok "Serviços systemd removidos."

# Pergunta se quer remover configurações
echo ""
read -r -p "Deseja remover também as configurações e logs? [s/N] " confirm_config
if [[ "$confirm_config" =~ ^[Ss]$ ]]; then
  rm -rf "$HOME/.config/rclone-sync-app"
  rm -rf "$HOME/.local/state/rclone-bisync"
  ok "Configurações e logs removidos."
else
  info "Configurações mantidas em ~/.config/rclone-sync-app"
  info "Logs mantidos em ~/.local/state/rclone-bisync"
fi

echo ""
echo "================================"
ok "RcloneSync desinstalado com sucesso!"
echo "================================"
echo ""