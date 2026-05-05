<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import api from '../services/api'

const logs = ref([])
const logSelecionado = ref(null)
const conteudo = ref([])
const carregando = ref(true)
const conectado = ref(false)
const autoScroll = ref(true)
const logContainer = ref(null)

let ws = null

onMounted(async () => {
  await carregarLogs()
  conectarWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})

async function carregarLogs() {
  try {
    const res = await api.get('/logs/listar')
    logs.value = res.data.logs
    if (logs.value.length > 0) {
      await selecionarLog(logs.value[0])
    }
  } finally {
    carregando.value = false
  }
}

async function selecionarLog(log) {
  logSelecionado.value = log
  try {
    const res = await api.get(`/logs/ler/${log.nome}`)
    conteudo.value = res.data.conteudo.split('\n').filter(l => l.trim())
  } catch {
    conteudo.value = []
  }
  await rolarParaBaixo()
}

function conectarWebSocket() {
  ws = new WebSocket('ws://localhost:8000/logs/ws')

  ws.onopen = () => { conectado.value = true }
  ws.onclose = () => { conectado.value = false }

  ws.onmessage = async (event) => {
    const novas = event.data.split('\n').filter(l => l.trim())
    conteudo.value.push(...novas)
    if (autoScroll.value) await rolarParaBaixo()
  }
}

async function rolarParaBaixo() {
  await nextTick()
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

function corDaLinha(linha) {
  if (linha.includes('ERROR') || linha.includes('CRITICAL')) return 'linha-erro'
  if (linha.includes('NOTICE') || linha.includes('WARN'))    return 'linha-aviso'
  if (linha.includes('Sucesso') || linha.includes('INFO'))   return 'linha-info'
  return 'linha-normal'
}

function formatarTamanho(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
</script>

<template>
  <div class="logs-page">
    <div class="logs-header">
      <div class="logs-title-row">
        <h2 class="page-title">Logs</h2>
        <div class="status-ws">
          <span class="ws-dot" :class="conectado ? 'ws-on' : 'ws-off'" />
          {{ conectado ? 'Ao vivo' : 'Desconectado' }}
        </div>
      </div>
      <label class="autoscroll-toggle">
        <input type="checkbox" v-model="autoScroll" />
        Auto scroll
      </label>
    </div>

    <div class="logs-layout">

      <!-- Lista de arquivos -->
      <div class="logs-sidebar">
        <div class="logs-sidebar-title">
          <span class="pi pi-file accent" />
          Arquivos
        </div>

        <div v-if="carregando" class="loading">
          <span class="pi pi-spin pi-spinner" style="color: #6366f1" />
        </div>

        <ul v-else class="logs-list">
          <li
            v-for="log in logs"
            :key="log.nome"
            class="log-item"
            :class="{ 'log-selected': logSelecionado?.nome === log.nome }"
            @click="selecionarLog(log)"
          >
            <p class="log-nome">{{ log.nome }}</p>
            <p class="log-tamanho">{{ formatarTamanho(log.tamanho) }}</p>
          </li>
        </ul>
      </div>

      <!-- Conteúdo do log -->
      <div class="logs-viewer">
        <div v-if="!logSelecionado" class="logs-empty">
          <span class="pi pi-file logs-empty-icon" />
          <p>Selecione um arquivo de log</p>
        </div>

        <div v-else ref="logContainer" class="logs-content">
          <div
            v-for="(linha, i) in conteudo"
            :key="i"
            class="log-linha"
            :class="corDaLinha(linha)"
          >
            <span class="linha-num">{{ i + 1 }}</span>
            <span class="linha-texto">{{ linha }}</span>
          </div>

          <div v-if="conteudo.length === 0" class="logs-empty">
            <p>Arquivo vazio.</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.logs-page {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logs-title-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--app-text);
  margin: 0;
}

.status-ws {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  color: var(--app-text-muted);
}

.ws-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  flex-shrink: 0;
}

.ws-on  { background: #86efac; box-shadow: 0 0 6px #86efac; }
.ws-off { background: #fca5a5; }

.autoscroll-toggle {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  color: var(--app-text-muted);
  cursor: pointer;
}

/* Layout */
.logs-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 1rem;
  flex: 1;
  min-height: 0;
  height: calc(100vh - 140px);
}

/* Sidebar */
.logs-sidebar {
  background: var(--app-surface-card);
  border: 1px solid var(--app-border);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
}

.logs-sidebar-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--app-text-muted);
}

.accent { color: #6366f1; }

.logs-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.log-item {
  padding: 0.65rem 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  border: 1px solid transparent;
}

.log-item:hover {
  background: var(--app-surface-alt);
}

.log-selected {
  background: var(--app-surface-alt);
  border-color: #6366f1;
}

.log-nome {
  font-size: 0.78rem;
  color: var(--app-text);
  word-break: break-all;
  line-height: 1.4;
}

.log-tamanho {
  font-size: 0.72rem;
  color: var(--app-text-muted);
  margin-top: 0.15rem;
}

/* Viewer */
.logs-viewer {
  background: var(--app-surface-input);
  border: 1px solid var(--app-border);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.logs-content {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem 0;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.78rem;
  line-height: 1.6;
}

.log-linha {
  display: flex;
  gap: 1rem;
  padding: 0.1rem 1rem;
  transition: background 0.1s;
}

.log-linha:hover {
  background: var(--app-surface-card);
}

.linha-num {
  color: var(--app-log-line-number);
  min-width: 2.5rem;
  text-align: right;
  user-select: none;
  flex-shrink: 0;
}

.linha-texto {
  color: var(--app-log-text);
  word-break: break-all;
}

.linha-erro  .linha-texto { color: var(--app-log-error); }
.linha-aviso .linha-texto { color: var(--app-log-warning); }
.linha-info  .linha-texto { color: var(--app-log-info); }
.linha-normal .linha-texto { color: var(--app-log-text); }

.logs-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  height: 100%;
  color: var(--app-log-line-number);
  font-size: 0.9rem;
}

.logs-empty-icon {
  font-size: 2.5rem;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 1rem;
}
</style>