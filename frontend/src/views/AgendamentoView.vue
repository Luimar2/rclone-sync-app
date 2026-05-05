<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const status = ref(null)
const carregando = ref(true)
const salvando = ref(false)
const desativando = ref(false)
const erro = ref('')
const sucesso = ref('')

const intervaloSelecionado = ref('daily')
const horarioCustomizado = ref('')

const opcoes = [
  { valor: '1h',     label: 'A cada 1 hora',     desc: 'Recomendado para uso intenso',              icon: 'pi pi-bolt' },
  { valor: '6h',     label: 'A cada 6 horas',    desc: 'Equilíbrio entre frequência e consumo',     icon: 'pi pi-chart-line' },
  { valor: '12h',    label: 'A cada 12 horas',   desc: 'Conservador, ideal para conexões limitadas', icon: 'pi pi-shield' },
  { valor: 'daily',  label: 'Uma vez ao dia',    desc: 'Recomendado — menor risco de conflitos',    icon: 'pi pi-calendar' },
  { valor: 'custom', label: 'Horário customizado', desc: 'Defina um horário específico no formato systemd', icon: 'pi pi-cog' },
]

onMounted(async () => {
  await carregarStatus()
})

async function carregarStatus() {
  carregando.value = true
  try {
    const res = await api.get('/agendamento/status')
    status.value = res.data
  } catch {
    erro.value = 'Não foi possível carregar o status do agendamento.'
  } finally {
    carregando.value = false
  }
}

async function salvarAgendamento() {
  if (intervaloSelecionado.value === 'custom' && !horarioCustomizado.value) {
    erro.value = 'Informe o horário customizado.'
    return
  }

  salvando.value = true
  erro.value = ''
  sucesso.value = ''

  try {
    await api.post('/agendamento/instalar', {
      intervalo: intervaloSelecionado.value,
      horario_customizado: horarioCustomizado.value
    })
    sucesso.value = 'Agendamento atualizado com sucesso.'
    await carregarStatus()
  } catch {
    erro.value = 'Erro ao salvar agendamento. Tente novamente.'
  } finally {
    salvando.value = false
  }
}

async function desativarAgendamento() {
  desativando.value = true
  erro.value = ''
  sucesso.value = ''
  try {
    await api.post('/agendamento/desativar')
    sucesso.value = 'Agendamento desativado.'
    await carregarStatus()
  } catch {
    erro.value = 'Erro ao desativar agendamento.'
  } finally {
    desativando.value = false
  }
}
</script>

<template>
  <div class="page">
    <h2 class="page-title">Agendamento</h2>
    <p class="page-desc">Gerencie a frequência de sincronização automática.</p>

    <!-- Status atual -->
    <div class="card" v-if="!carregando && status">
      <div class="card-header">
        <span class="pi pi-clock card-icon" />
        <span>Status atual</span>
        <span class="badge ml-auto" :class="status.ativo ? 'badge-success' : 'badge-danger'">
          {{ status.ativo ? 'Ativo' : 'Inativo' }}
        </span>
      </div>
    </div>

    <!-- Seleção de frequência -->
    <div class="card">
      <div class="card-header">
        <span class="pi pi-sliders-h card-icon" />
        <span>Frequência de sincronização</span>
      </div>
      <div class="card-body">
        <ul class="opcoes-list">
          <li
            v-for="opcao in opcoes"
            :key="opcao.valor"
            class="opcao-item"
            :class="{ 'opcao-selected': intervaloSelecionado === opcao.valor }"
            @click="intervaloSelecionado = opcao.valor"
          >
            <div class="opcao-info">
              <span :class="opcao.icon + ' opcao-icon'" />
              <div>
                <p class="opcao-label">{{ opcao.label }}</p>
                <p class="opcao-desc">{{ opcao.desc }}</p>
              </div>
            </div>
            <div class="radio">
              <div v-if="intervaloSelecionado === opcao.valor" class="radio-dot" />
            </div>
          </li>
        </ul>

        <!-- Horário customizado -->
        <div v-if="intervaloSelecionado === 'custom'" class="custom-block">
          <div class="code-block">
            <code>*-*-* 02:00:00</code>
            <span class="code-comment"> # todo dia às 02:00</span><br />
            <code>Mon *-*-* 08:00:00</code>
            <span class="code-comment"> # toda segunda às 08:00</span>
          </div>
          <div class="input-group">
            <label class="input-label">Expressão systemd</label>
            <input
              v-model="horarioCustomizado"
              class="input"
              placeholder="*-*-* 02:00:00"
            />
          </div>
        </div>

        <!-- Info -->
        <div class="info-card">
          <span class="pi pi-info-circle info-icon" />
          <p class="opcao-desc">
            O agendamento usa <strong>systemd --user</strong> e funciona mesmo com o app fechado.
            Intervalos abaixo de 1 hora podem causar conflitos.
          </p>
        </div>

        <!-- Feedback -->
        <p v-if="erro" class="erro"><span class="pi pi-exclamation-triangle" /> {{ erro }}</p>
        <p v-if="sucesso" class="success-msg"><span class="pi pi-check-circle" /> {{ sucesso }}</p>

        <!-- Ações -->
        <div class="actions">
          <button class="btn-primary" :disabled="salvando" @click="salvarAgendamento">
            <span :class="salvando ? 'pi pi-spin pi-spinner' : 'pi pi-check'" />
            {{ salvando ? 'Salvando...' : 'Salvar agendamento' }}
          </button>
          <button
            v-if="status?.ativo"
            class="btn-danger"
            :disabled="desativando"
            @click="desativarAgendamento"
          >
            <span :class="desativando ? 'pi pi-spin pi-spinner' : 'pi pi-times'" />
            {{ desativando ? 'Desativando...' : 'Desativar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-title { font-size: 1.3rem; font-weight: 700; color: var(--app-text); }
.page-desc  { font-size: 0.88rem; color: var(--app-text-muted); margin-top: -1rem; }

.card {
  background: var(--app-surface-card);
  border: 1px solid var(--app-border);
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--app-border);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--app-text);
}

.card-icon { color: #6366f1; }
.ml-auto { margin-left: auto; }

.card-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.opcoes-list { list-style: none; display: flex; flex-direction: column; gap: 0.25rem; }

.opcao-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1rem;
  border: 1px solid var(--app-border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.opcao-item:hover { background: var(--app-surface-alt); border-color: #6366f1; }
.opcao-selected   { background: var(--app-surface-alt); border-color: #6366f1; }

.opcao-info { display: flex; align-items: center; gap: 0.75rem; }
.opcao-icon { color: #6366f1; font-size: 1.1rem; width: 1.2rem; text-align: center; }
.opcao-label { font-size: 0.9rem; font-weight: 500; color: var(--app-text); }
.opcao-desc  { font-size: 0.78rem; color: var(--app-text-muted); line-height: 1.5; }

.radio {
  width: 18px; height: 18px;
  border: 2px solid var(--app-border);
  border-radius: 999px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.opcao-selected .radio { border-color: #6366f1; }
.radio-dot { width: 8px; height: 8px; background: #6366f1; border-radius: 999px; }

.custom-block { display: flex; flex-direction: column; gap: 0.75rem; }

.code-block {
  background: var(--app-surface-input);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  line-height: 2;
}
code { font-size: 0.82rem; color: #86efac; font-family: 'JetBrains Mono', monospace; }
.code-comment { font-size: 0.78rem; color: var(--app-text-muted); margin-left: 0.5rem; font-family: monospace; }

.input-group { display: flex; flex-direction: column; gap: 0.4rem; }
.input-label { font-size: 0.8rem; color: var(--app-text-muted-2); font-weight: 500; }
.input {
  background: var(--app-surface-input);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  padding: 0.6rem 0.85rem;
  color: var(--app-text);
  font-size: 0.88rem;
  outline: none;
  transition: border 0.2s;
}
.input:focus { border-color: #6366f1; }

.info-card {
  display: flex; align-items: flex-start; gap: 0.75rem;
  background: var(--app-surface-alt); border: 1px solid #3730a3;
  border-radius: 10px; padding: 1rem;
}
.info-icon { color: #6366f1; font-size: 1rem; flex-shrink: 0; margin-top: 0.1rem; }

.actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }

.btn-primary {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.6rem 1.1rem; background: #6366f1; color: var(--app-text-inverse);
  border: none; border-radius: 8px; font-size: 0.88rem;
  font-weight: 500; cursor: pointer; transition: background 0.2s;
}
.btn-primary:hover { background: #4f46e5; }
.btn-primary:disabled { background: var(--app-border); color: var(--app-text-muted); cursor: not-allowed; }

.btn-danger {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.6rem 1.1rem; background: transparent; color: #fca5a5;
  border: 1px solid #7f1d1d; border-radius: 8px; font-size: 0.88rem;
  font-weight: 500; cursor: pointer; transition: all 0.2s;
}
.btn-danger:hover { background: #7f1d1d; color: var(--app-text-inverse); }
.btn-danger:disabled { opacity: 0.5; cursor: not-allowed; }

.badge {
  font-size: 0.75rem; font-weight: 600;
  padding: 0.25rem 0.65rem; border-radius: 999px;
}
.badge-success { background: #14532d; color: #86efac; }
.badge-danger  { background: #7f1d1d; color: #fca5a5; }

.erro        { font-size: 0.85rem; color: #fca5a5; display: flex; align-items: center; gap: 0.4rem; }
.success-msg { font-size: 0.85rem; color: #86efac; display: flex; align-items: center; gap: 0.4rem; }
</style>
