# RcloneSync

Interface gráfica para gerenciar backups com Google Drive no Linux,
construída com FastAPI e Vue.js.

![versão](https://img.shields.io/badge/versão-0.1.0-6366f1)
![plataforma](https://img.shields.io/badge/plataforma-Linux-blue)
![licença](https://img.shields.io/badge/licença-MIT-green)

---

## Sobre o projeto

RcloneSync nasceu de um shell script pessoal de sincronização com rclone bisync
e evoluiu para uma aplicação web completa com o objetivo de tornar o gerenciamento
de backups acessível para usuários Linux sem necessidade de usar o terminal no dia a dia.

### Funcionalidades

- Configuração de remotes e pares de sincronização via interface gráfica
- Sincronização bidirecional com Google Drive usando rclone bisync
- Snapshot local antes de cada sincronização para proteção de dados
- Agendamento automático via systemd --user
- Filtros de exclusão por categorias ou regras personalizadas
- Visualização de logs em tempo real via WebSocket
- Retry automático com detecção de tipo de erro
- Interface com tema escuro seguindo a preferência do sistema

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
- rclone instalado e configurado

### Instalando o Python venv

Em sistemas Debian/Ubuntu o pacote `python3-venv` pode não vir instalado:

```bash
sudo apt install python3-venv
```

### Instalando o Node.js via nvm

**Não instale o Node via `apt`** — a versão dos repositórios Ubuntu é antiga
e instala centenas de pacotes desnecessários.

```bash
# Instala o nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Recarrega o terminal
source ~/.bashrc

# Instala o Node 20 LTS
nvm install 20
nvm use 20
nvm alias default 20
```

### Instalando o rclone

```bash
sudo apt install rclone
```

### Configurando um remote Google Drive

```bash
rclone config
```

Siga o assistente:
1. Escolha **n** para novo remote
2. Dê um nome — ex: `GoogleDrive`
3. Escolha o número correspondente ao **Google Drive**
4. Deixe `client_id` e `client_secret` em branco
5. Escolha escopo **1** (acesso completo)
6. Deixe `service_account_file` em branco
7. Não edite configurações avançadas
8. Use auto config — o browser abrirá para autenticação
9. Não configure como Shared Drive
10. Confirme e saia

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/Luimar2/rclone-sync-app.git
cd rclone-sync-app

# Execute o instalador
chmod +x install.sh
./install.sh
```

O instalador irá:

1. Verificar todas as dependências
2. Criar o ambiente virtual Python e instalar os pacotes
3. Compilar o frontend Vue para produção
4. Instalar e ativar o servidor como serviço systemd --user

Após a instalação, acesse **http://localhost:8000** no navegador.

---

## Uso em desenvolvimento

```bash
# Backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000

# Frontend (outro terminal)
cd frontend
npm run dev
```

A API estará disponível em **http://localhost:8000**
e o frontend em **http://localhost:5173**.

A documentação interativa da API (Swagger) estará disponível em
**http://localhost:8000/docs**.

---

## Estrutura do projeto