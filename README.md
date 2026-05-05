# RcloneSync

Interface gráfica para gerenciar backups com **Google Drive** no Linux,
construída com FastAPI e Vue.js.

![versão](https://img.shields.io/badge/versão-0.1.1-blue)
![plataforma](https://img.shields.io/badge/plataforma-Linux-blue)
![licença](https://img.shields.io/badge/licença-MIT-green)

---

> ⚠️ **Projeto doméstico** — RcloneSync é uma ferramenta pessoal de uso doméstico,
> focada exclusivamente em sincronização com **Google Drive**.
> Não é um produto oficial do projeto rclone nem possui vínculo com ele.
> Funcional mas em desenvolvimento ativo — bugs são esperados.

---

## Sobre o projeto

RcloneSync nasceu de um shell script pessoal de sincronização com rclone bisync
e evoluiu para uma aplicação web com o objetivo de tornar o gerenciamento
de backups acessível para usuários Linux sem necessidade de usar o terminal no dia a dia.

### O que este projeto faz

- Gerencia sincronização bidirecional entre pastas locais e o **Google Drive**
- Fornece interface gráfica para configurar pares de sincronização
- Agenda sincronizações automáticas via **systemd --user**
- Exibe logs de sincronização em tempo real

### O que este projeto **não** faz

- Não suporta outros providers (OneDrive, Dropbox, S3 etc.) — apenas Google Drive
- Não é um cliente rclone completo — cobre apenas o fluxo de bisync com Drive
- Não possui vínculo oficial com o projeto [rclone](https://rclone.org)
- Não foi testado em ambientes corporativos ou de produção

### Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| Frontend | Vue.js 3, Vite, PrimeIcons |
| Sincronização | rclone bisync |
| Agendamento | systemd --user |

---

## Pré-requisitos

- Linux (testado no Ubuntu/Pop!_OS)
- Python 3.10 ou superior
- Node.js 18 ou superior — **instale via nvm, não via apt**
- rclone instalado e configurado com um remote Google Drive

### Instalando o Python venv

```bash
sudo apt install python3-venv
```

### Instalando o Node.js via nvm

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20 && nvm use 20 && nvm alias default 20
```

### Instalando o rclone

```bash
curl -fsSL https://rclone.org/install.sh | sudo bash
```

Versão mínima necessária: **1.65**

### Configurando um remote Google Drive

O app lista apenas remotes do tipo **Google Drive** já configurados no rclone.
Para criar um:

```bash
rclone config
```

Siga o assistente: novo remote → nome → Google Drive → escopo 1 → auto config (browser) → confirmar.

---

## Instalação

```bash
git clone https://github.com/Luimar2/rclone-sync-app.git
cd rclone-sync-app
chmod +x install.sh
./install.sh
```

Após a instalação, acesse **http://localhost:8000** no navegador.

---

## Uso em desenvolvimento

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn main:app --reload --port 8000

# Frontend (outro terminal)
cd frontend && npm run dev
```

API: **http://localhost:8000** · Frontend: **http://localhost:5173** · Swagger: **http://localhost:8000/docs**

---

## Estrutura do projeto

```
rclone-sync-app/
├── backend/
│   ├── main.py
│   ├── routes/          # agendamento, config, logs, sync
│   └── services/        # rclone, systemd, event_logger, snapshot...
├── frontend/
│   └── src/
│       ├── components/  # DirPicker, RemotesList
│       ├── layouts/     # DefaultLayout (sidebar)
│       ├── views/       # Dashboard, Pares, Agendamento, Logs, Onboarding
│       └── router/
└── docs/
    └── GUIA_USO.md
```

---

## Licença

MIT
