#!/usr/bin/env bash
set -euo pipefail

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

command -v python3 >/dev/null 2>&1 || erro "Python3 não encontrado."
command -v rclone  >/dev/null 2>&1 || erro "rclone não encontrado. Instale com: sudo apt install rclone"

# Verifica Node via nvm ou sistema
if ! command -v node >/dev/null 2>&1; then
  erro "Node.js não encontrado. Instale via nvm: https://github.com/nvm-sh/nvm"
fi

NODE_VERSION=$(node -e 'console.log(process.versions.node.split(".")[0])')
if [ "$NODE_VERSION" -lt 18 ]; then
  erro "Node.js 18+ necessário. Versão encontrada: $NODE_VERSION. Instale via nvm."
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_VERSION" -lt 10 ]; then
  erro "Python 3.10+ necessário."
fi

# Verifica e instala python3-venv se necessário
if ! python3 -m venv --help >/dev/null 2>&1; then
  info "Instalando python3-venv..."
  PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
  PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
  sudo apt install -y "python${PY_MAJOR}.${PY_MINOR}-venv" || \
    erro "Não foi possível instalar python3-venv. Execute: sudo apt install python3-venv"
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

# --- Instalação ---

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

# --- Aguarda o servidor subir ---

info "Aguardando o servidor iniciar..."
for i in {1..10}; do
  if curl -s http://localhost:8000 >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

# --- Abre o browser ---

info "Abrindo no navegador..."
xdg-open http://localhost:8000 >/dev/null 2>&1 || true

echo ""
echo "================================"
ok "Instalação concluída!"
echo ""
echo "  Acesse: http://localhost:8000"
echo "================================"
echo ""