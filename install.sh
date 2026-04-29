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

# --- Dependências básicas do sistema ---

info "Verificando dependências do sistema..."

PKGS_NEEDED=()

command -v curl   >/dev/null 2>&1 || PKGS_NEEDED+=("curl")
command -v git    >/dev/null 2>&1 || PKGS_NEEDED+=("git")
command -v rsync  >/dev/null 2>&1 || PKGS_NEEDED+=("rsync")
command -v rclone >/dev/null 2>&1 || PKGS_NEEDED+=("rclone")

if ! python3 -m venv --help >/dev/null 2>&1; then
  PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  PKGS_NEEDED+=("python${PY_VER}-venv")
fi

if [ ${#PKGS_NEEDED[@]} -gt 0 ]; then
  info "Instalando pacotes necessários: ${PKGS_NEEDED[*]}"
  sudo apt update -qq
  sudo apt install -y "${PKGS_NEEDED[@]}"
  ok "Pacotes instalados."
fi

# --- Verifica Python ---

command -v python3 >/dev/null 2>&1 || erro "Python3 não encontrado."

PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_MINOR" -lt 10 ]; then
  erro "Python 3.10+ necessário. Versão encontrada: 3.${PYTHON_MINOR}"
fi

# --- Verifica e instala Node via nvm ---

if ! command -v node >/dev/null 2>&1; then
  info "Node.js não encontrado. Instalando via nvm..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  source "$NVM_DIR/nvm.sh"
  nvm install 20
  nvm use 20
  nvm alias default 20
  ok "Node.js instalado via nvm."
else
  NODE_VERSION=$(node -e 'console.log(process.versions.node.split(".")[0])')
  if [ "$NODE_VERSION" -lt 18 ]; then
    info "Node.js desatualizado (v${NODE_VERSION}). Atualizando via nvm..."
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
    nvm install 20
    nvm use 20
    nvm alias default 20
    ok "Node.js atualizado."
  fi
fi

# Garante que npm está disponível
command -v npm >/dev/null 2>&1 || erro "npm não encontrado após instalação do Node."

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
rm -rf "$INSTALL_DIR/backend"
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
for i in {1..15}; do
  if curl -s http://localhost:8000 >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

# --- Abre o browser ---

xdg-open http://localhost:8000 >/dev/null 2>&1 || true

echo ""
echo "================================"
ok "Instalação concluída!"
echo ""
echo "  Acesse: http://localhost:8000"
echo "================================"
echo ""