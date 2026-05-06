<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'

const router = useRouter()
const store = useConfigStore()
const erro = ref('')
const instalando = ref(false)

const opcoes = [
  {
    valor: '1h',
    label: 'A cada 1 hora',
    desc: 'Recomendado para uso intenso',
    icon: 'pi pi-bolt'
  },
  {
    valor: '6h',
    label: 'A cada 6 horas',
    desc: 'Equilíbrio entre frequência e consumo',
    icon: 'pi pi-chart-line'
  },
  {
    valor: '12h',
    label: 'A cada 12 horas',
    desc: 'Conservador, ideal para conexões limitadas',
    icon: 'pi pi-shield'
  },
  {
    valor: 'daily',
    label: 'Uma vez ao dia',
    desc: 'Recomendado — menor risco de conflitos',
    icon: 'pi pi-calendar'
  },
  {
    valor: 'custom',
    label: 'Horário customizado',
    desc: 'Defina um horário específico no formato systemd',
    icon: 'pi pi-cog'
  },
]

async function instalarTimer() {
  if (store.agendamento.intervalo === 'custom' &&
      !store.agendamento.horario_customizado) {
    erro.value = 'Informe o horário customizado.'
    return
  }

  instalando.value = true
  erro.value = ''

  try {
    await api.post('/agendamento/instalar', {
      intervalo: store.agendamento.intervalo,
      horario_customizado: store.agendamento.horario_customizado
    })
    router.push('/onboarding/6')
  } catch {
    erro.value = 'Erro ao instalar o agendamento. Tente novamente.'
  } finally {
    instalando.value = false
  }
}
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">5 de 6</span>
      <h2 class="step-title">Agendamento</h2>
      <p class="step-desc">
        Defina com qual frequência a sincronização será executada automaticamente.
      </p>
    </div>

    <!-- Opções -->
    <div class="card">
      <div class="card-section-title">
        <span class="pi pi-clock accent" />
        Frequência de sincronização
      </div>

      <ul class="opcoes-list">
        <li
          v-for="opcao in opcoes"
          :key="opcao.valor"
          class="opcao-item"
          :class="{ 'opcao-selected': store.agendamento.intervalo === opcao.valor }"
          @click="store.agendamento.intervalo = opcao.valor"
        >
          <div class="opcao-info">
            <span :class="opcao.icon + ' opcao-icon'" />
            <div>
              <p class="opcao-label">{{ opcao.label }}</p>
              <p class="opcao-desc">{{ opcao.desc }}</p>
            </div>
          </div>
          <div class="radio">
            <div
              v-if="store.agendamento.intervalo === opcao.valor"
              class="radio-dot"
            />
          </div>
        </li>
      </ul>
    </div>

    <!-- Horário customizado -->
    <div v-if="store.agendamento.intervalo === 'custom'" class="card">
      <div class="card-section-title">
        <span class="pi pi-pencil accent" />
        Horário customizado
      </div>
      <p class="opcao-desc">
        Use o formato do systemd. Exemplos:
      </p>
      <div class="code-block">
        <code>*-*-* 02:00:00</code>
        <span class="code-comment"># todo dia às 02:00</span><br />
        <code>Mon *-*-* 08:00:00</code>
        <span class="code-comment"># toda segunda às 08:00</span>
      </div>
      <div class="input-group">
        <label class="input-label">Expressão systemd</label>
        <input
          v-model="store.agendamento.horario_customizado"
          class="input"
          placeholder="*-*-* 02:00:00"
        />
      </div>
    </div>

    <!-- Aviso -->
    <div class="info-card">
      <span class="pi pi-info-circle info-icon" />
      <p class="opcao-desc">
        O agendamento usa <strong>systemd --user</strong> e funciona mesmo com o app fechado.
        Intervalos abaixo de 1 hora podem causar conflitos de sincronização.
      </p>
    </div>

    <p v-if="erro" class="erro">
      <span class="pi pi-exclamation-triangle" /> {{ erro }}
    </p>

    <div class="step-actions">
      <button
        class="btn-primary"
        :disabled="instalando"
        @click="instalarTimer"
      >
        <span :class="instalando ? 'pi pi-spin pi-spinner' : 'pi pi-check'" />
        {{ instalando ? 'Instalando...' : 'Instalar agendamento' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.accent { color: #6366f1; }

.card-section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.opcoes-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.opcao-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1rem;
  border: 1px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.opcao-item:hover {
  background: var(--bg-card-alt);
  border-color: var(--accent);
}

.opcao-selected {
  background: var(--bg-card-alt);
  border-color: var(--accent);
}

.opcao-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.opcao-icon {
  color: #6366f1;
  font-size: 1.1rem;
  width: 1.2rem;
  text-align: center;
}

.opcao-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-primary);
}

.opcao-desc {
  font-size: 0.78rem;
  color: var(--text-muted);
  line-height: 1.5;
}

/* Radio button */
.radio {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border);
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: border 0.2s;
}

.opcao-selected .radio {
  border-color: var(--accent);
}

.radio-dot {
  width: 8px;
  height: 8px;
  background: #6366f1;
  border-radius: 999px;
}

/* Code block */
.code-block {
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.75rem;
  line-height: 2;
}

code {
  font-size: 0.82rem;
  color: var(--success-text);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.code-comment {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-left: 0.75rem;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Info card */
.info-card {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: var(--bg-card-alt);
  border: 1px solid var(--accent-border);
  border-radius: 10px;
  padding: 1rem;
}

.info-icon {
  color: #6366f1;
  font-size: 1rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
}
</style>