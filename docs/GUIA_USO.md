# Guia de uso — RcloneSync

> **Escopo deste app:** RcloneSync é uma ferramenta doméstica focada em sincronização
> com **Google Drive** via rclone bisync. Outros providers (OneDrive, Dropbox, S3 etc.)
> não são suportados. O app não possui vínculo oficial com o projeto rclone.

---

## Primeiro acesso

Após a instalação, acesse **http://localhost:8000** no navegador.
Se for o primeiro acesso, você será direcionado ao assistente de configuração.

---

## Assistente de configuração

### Passo 1 — Verificação do ambiente

O app verifica se o rclone está instalado e disponível no sistema.
Caso não esteja, instale com:

```bash
curl -fsSL https://rclone.org/install.sh | sudo bash
```

### Passo 2 — Remote Google Drive

Selecione um remote **Google Drive** já configurado no rclone.
O app filtra automaticamente e exibe apenas remotes compatíveis.

Caso ainda não tenha um remote, execute no terminal:

```bash
rclone config
```

Escolha **New remote → Google Drive** e siga o assistente de autenticação OAuth.
Após concluir, volte ao app e atualize a página.

> Remotes de outros tipos (S3, OneDrive, FTP etc.) não aparecem na lista
> pois não são suportados por esta versão do app.

### Passo 3 — Pares de sincronização

Defina quais pastas locais serão sincronizadas com o Google Drive.
Use o **seletor de pasta** (ícone de pasta ao lado do campo) para navegar
pelo sistema de arquivos, ou digite o caminho manualmente.

Exemplos:

| Pasta local | Pasta no Google Drive |
|---|---|
| /home/usuario/Documentos | / |
| /home/usuario/Projetos | /Projetos |

### Passo 4 — Filtros de exclusão

Escolha o que não deve ser sincronizado:

| Filtro | O que exclui |
|---|---|
| Arquivos temporários | *.tmp, *.temp |
| Lixeira | .Trash/** |
| Cache | **/cache/**, **/Cache/** |
| Repositórios Git | .git/** |
| Arquivos ocultos | .* |

Para filtros personalizados, use a seção **Filtros avançados** com um filtro
por linha no formato do rclone (ex: `*.log`, `/node_modules/`).

### Passo 5 — Agendamento

Escolha a frequência de sincronização automática.
O agendamento usa **systemd --user** e funciona mesmo com o app fechado.

> Recomendamos **uma vez ao dia** para evitar conflitos e consumo excessivo de banda.

### Passo 6 — Confirmação

Revise o resumo e execute o primeiro sync para validar a configuração.

---

## Navegação principal (sidebar)

Após a configuração inicial, use o sidebar para acessar:

| Item | Caminho | O que faz |
|---|---|---|
| Painel | /dashboard | Visão geral, sync manual |
| Pares | /pares | Editar e excluir pares configurados |
| Agendamento | /agendamento | Alterar frequência ou desativar |
| Configurações | /onboarding/1 | Refazer o fluxo de configuração |
| Logs | /logs | Ver logs de sincronização em tempo real |

Clique no logo **RcloneSync** no topo do sidebar para voltar à home.

---

## Gerenciando pares de sincronização

Em **Pares** você pode:

- **Editar** o caminho local ou remoto de um par existente
- **Pausar/Ativar** um par sem excluí-lo
- **Excluir** um par — a exclusão é permanente e remove o registro do agendamento vinculado

---

## Gerenciando o agendamento

Em **Agendamento** você pode:

- Alterar a frequência de sincronização a qualquer momento
- Usar horário customizado no formato systemd (ex: `*-*-* 02:00:00`)
- Desativar o agendamento sem excluir os pares configurados

---

## Logs

A tela de **Logs** exibe os arquivos gerados pelo rclone bisync, com atualização
em tempo real via WebSocket durante uma sincronização.

### Cores das linhas

| Cor | Significado |
|---|---|
| Verde | INFO — operação bem-sucedida |
| Amarelo | NOTICE / WARN — aviso |
| Vermelho | ERROR / CRITICAL — erro |
| Cinza | Informação geral |

---

## Arquivos gerados pelo app

| Caminho | Conteúdo |
|---|---|
| `~/.config/rclone-sync-app/config.json` | Configuração de pares e agendamento |
| `~/.config/systemd/user/rclone-sync-app.service` | Serviço web |
| `~/.config/systemd/user/rclone-sync-app.timer` | Timer de sync |
| `~/.local/state/rclone-bisync/` | Logs de sincronização do rclone |
| `~/.local/state/rclone-sync-app/events.log` | Log de eventos do app (criação/edição/exclusão) |

---

## Solução de problemas

### O app não abre no navegador

```bash
systemctl --user status rclone-sync-app-web.service
systemctl --user start rclone-sync-app-web.service
```

### Nenhum remote aparece na lista

Apenas remotes do tipo **Google Drive** são exibidos. Verifique com:

```bash
rclone config show
```

Se o campo `type` do seu remote não for `drive`, ele não será listado.
Crie um novo remote do tipo Google Drive com `rclone config`.

### Erro de sincronização

Acesse **Logs** e verifique o último arquivo gerado.

| Erro | Causa provável |
|---|---|
| `Overlapping paths` | Caminho local e remoto iguais |
| `bisync critical` | Conflito grave — resync automático será tentado |
| `rate limit` | Limite da API do Google Drive atingido |
| `timeout` | Problema de conexão com a internet |

### Resetar a configuração

```bash
rm ~/.config/rclone-sync-app/config.json
```

Reinicie o app e o assistente de configuração será exibido novamente.

---

## Desinstalação

```bash
systemctl --user disable --now rclone-sync-app-web.service
systemctl --user disable --now rclone-sync-app.timer
rm -rf ~/.local/share/rclone-sync-app
rm -rf ~/.config/rclone-sync-app
rm -rf ~/.config/systemd/user/rclone-sync-app*
systemctl --user daemon-reload
```
