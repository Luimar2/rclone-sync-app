#!/usr/bin/env bash
set -euo pipefail

###################################
# RcloneSync — Script de instalação
###################################

VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
RESET='\033[0m'

ok()   { echo -e "${VERDE}✅ $1${RESET}"; }
info() { echo -e "${AMARELO}➡️  $1${RESET}"; }
erro() { echo -e "${VERMELHO}❌ $1${RESET}"; exit 1; }

echo ""
echo "================================"
echo "   RcloneSync — Instalação"
echo "================================"
echo ""

# --- Verificações ---

info "Verificando dependências..."

command -v python3 >/dev/null 2>&1 || erro "Python3 não encontrado. Instale antes de continuar."
command -v node    >/dev/null 2>&1 || erro "Node.js não encontrado. Instale antes de continuar."
command -v npm     >/dev/null 2>&1 || erro "npm não encontrado."
command -v rclone  >/dev/null 2>&1 || erro "rclone não encontrado. Instale com: sudo apt install rclone"

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_VERSION" -lt 10 ]; then
  erro "Python 3.10 ou superior é necessário."
fi

NODE_VERSION=$(node -e 'console.log(process.versions.node.split(".")[0])')
if [ "$NODE_VERSION" -lt 18 ]; then
  erro "Node.js 18 ou superior é necessário."
fi

ok "Dependências verificadas."

# --- Backend ---

info "Configurando backend Python..."

cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet -r requirements.txt
deactivate
cd ..

ok "Backend configurado."

# --- Frontend ---

info "Configurando frontend Vue..."

cd frontend
npm install --silent
npm run build
cd ..

ok "Frontend compilado."

# --- Serviço systemd ---

info "Instalando serviço systemd..."

INSTALL_DIR="$HOME/.local/share/rclone-sync-app"
mkdir -p "$INSTALL_DIR"
cp -r backend "$INSTALL_DIR/"
cp -r frontend/dist "$INSTALL_DIR/frontend"

SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"

cat > "$SERVICE_DIR/rclone-sync-app-web.service" << EOF
[Unit]
Description=RcloneSync App — servidor web
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR/backend
ExecStart=$INSTALL_DIR/backend/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now rclone-sync-app-web.service

ok "Serviço web instalado e iniciado."

# --- Finalização ---

echo ""
echo "================================"
ok "Instalação concluída!"
echo ""
echo "  Acesse: http://localhost:8000"
echo "  ou abra o navegador em:"
echo "  http://localhost:5173 (desenvolvimento)"
echo "================================"
echo ""