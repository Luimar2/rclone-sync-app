# Guia de uso — RcloneSync

## Primeiro acesso

Após a instalação, acesse **http://localhost:8000** no navegador.
Se for o primeiro acesso, você será direcionado automaticamente
para o assistente de configuração.

---

## Assistente de configuração

### Passo 1 — Verificação do ambiente

O app verifica se o rclone está instalado e disponível.
Caso não esteja, siga as instruções na tela para instalá-lo.

### Passo 2 — Remote Google Drive

Selecione um remote Google Drive já configurado no rclone.
Caso ainda não tenha um remote configurado, execute no terminal:

```bash
rclone config
```

Escolha **New remote**, selecione **Google Drive** e siga o assistente
de autenticação OAuth. Após concluir, volte ao app e atualize a página.

### Passo 3 — Pares de sincronização

Defina quais pastas locais serão sincronizadas com o Google Drive.
Você pode adicionar múltiplos pares — por exemplo:

| Pasta local | Pasta no Google Drive |
|---|---|
| /home/usuario/Documentos | / |
| /home/usuario/Projetos | /Projetos |

### Passo 4 — Filtros de exclusão

Escolha o que não deve ser sincronizado.
As exclusões comuns disponíveis são:

| Filtro | O que exclui |
|---|---|
| Arquivos temporários | *.tmp, *.temp |
| Lixeira | .Trash/** |
| Cache | **/cache/**, **/Cache/** |
| Repositórios Git | .git/** |
| Arquivos ocultos | .* |

Para filtros personalizados, use a seção **Filtros avançados**
com um filtro por linha no formato do rclone:

*.log
/node_modules/

### Passo 5 — Agendamento

Escolha a frequência de sincronização automática.
O agendamento é gerenciado pelo **systemd --user** e funciona
mesmo com o app fechado.

> Recomendamos o intervalo de **uma vez ao dia** para evitar
> conflitos de sincronização e consumo excessivo de banda.

### Passo 6 — Confirmação

Revise o resumo da configuração e execute o primeiro sync
para validar que tudo está funcionando corretamente.

---

## Painel principal

O painel exibe:

- **Pares de sincronização** — lista de pares ativos e pausados
- **Agendamento** — status do timer systemd
- **Sincronização manual** — botão para executar o sync imediatamente

---

## Logs

A tela de logs exibe os arquivos de log gerados pelo rclone bisync.
A visualização é atualizada em tempo real via WebSocket enquanto
uma sincronização está em andamento.

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
| `~/.config/rclone-sync-app/config.json` | Configuração do app |
| `~/.config/systemd/user/rclone-sync-app.service` | Serviço web |
| `~/.config/systemd/user/rclone-sync-app.timer` | Timer de sync |
| `~/.local/state/rclone-bisync/` | Logs de sincronização |

---

## Solução de problemas

### O app não abre no navegador

Verifique se o serviço está rodando:

```bash
systemctl --user status rclone-sync-app-web.service
```

Se não estiver, inicie com:

```bash
systemctl --user start rclone-sync-app-web.service
```

### Erro de sincronização

Acesse a tela de **Logs** e verifique o último arquivo gerado.
Erros comuns e suas causas:

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