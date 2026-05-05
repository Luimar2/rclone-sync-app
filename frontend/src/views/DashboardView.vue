<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const pares = ref([])
const agendamento = ref(null)
const sincronizando = ref(false)
const resultado = ref(null)
const carregando = ref(true)

onMounted(async () => {
  try {
    const [paresRes, agendRes] = await Promise.all([
      api.get('/config/pares'),
      api.get('/agendamento/status')
    ])
    pares.value = paresRes.data.pares
    agendamento.value = agendRes.data
  } finally {
    carregando.value = false
  }
})

async function sincronizarAgora() {
  sincronizando.value = true
  resultado.value = null
  try {
    const res = await api.post('/sync/executar-todos')
    resultado.value = res.data
  } finally {
    sincronizando.value = false
  }
}
</script>

<template>
  <div class="dashboard">
    <h2 class="page-title">Painel</h2>

    <div v-if="carregando" class="loading">
      <span class="pi pi-spin pi-spinner loading-icon" />
    </div>

    <div v-else class="grid">

      <!-- Pares de sincronização -->
      <div class="card">
        <div class="card-header">
          <span class="pi pi-sync card-icon" />
          <span>Pares de sincronização</span>
        </div>
        <div class="card-body">
          <div v-if="pares.length === 0" class="empty">
            <span>Nenhum par configurado.</span>
            <button class="btn-primary" @click="router.push('/onboarding/3')">
              <span class="pi pi-plus" /> Configurar agora
            </button>
          </div>
          <ul v-else class="pares-list">
            <li v-for="par in pares" :key="par.id" class="par-item">
              <div class="par-info">
                <span class="pi pi-folder par-icon" />
                <div>
                  <p class="par-local">{{ par.local_path }}</p>
                  <p class="par-remote">{{ par.remote_name }}:{{ par.remote_path }}</p>
                </div>
              </div>
              <span class="badge" :class="par.ativo ? 'badge-success' : 'badge-warning'">
                {{ par.ativo ? 'Ativo' : 'Pausado' }}
              </span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Agendamento -->
      <div class="card">
        <div class="card-header">
          <span class="pi pi-clock card-icon" />
          <span>Agendamento</span>
        </div>
        <div class="card-body">
          <div class="agend-row">
            <span class="label">Status</span>
            <span class="badge" :class="agendamento?.ativo ? 'badge-success' : 'badge-danger'">
              {{ agendamento?.ativo ? 'Ativo' : 'Inativo' }}
            </span>
          </div>
          <div class="agend-row">
            <span class="pi pi-calendar label-icon" />
            <span class="label">Sincronização agendada via systemd</span>
          </div>
          <button class="btn-secondary" disabled title="Gestão de agendamento em breve">
            <span class="pi pi-cog" /> Gerenciar agendamento
          </button>
        </div>
      </div>

      <!-- Sincronização manual -->
      <div class="card card-full">
        <div class="card-header">
          <span class="pi pi-play card-icon" />
          <span>Sincronização manual</span>
        </div>
        <div class="card-body">
          <button
            class="btn-primary"
            :disabled="sincronizando || pares.length === 0"
            @click="sincronizarAgora"
          >
            <span :class="sincronizando ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'" />
            {{ sincronizando ? 'Sincronizando...' : 'Sincronizar agora' }}
          </button>

          <div v-if="resultado" class="resultado">
            <div
              v-for="r in resultado.resultados"
              :key="r.par"
              class="resultado-item"
            >
              <span class="badge" :class="r.sucesso ? 'badge-success' : 'badge-danger'">
                {{ r.sucesso ? 'Sucesso' : 'Falhou' }}
              </span>
              <span class="resultado-par">{{ r.par }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e2e8f0;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.loading-icon {
  font-size: 2rem;
  color: #6366f1;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.card-full {
  grid-column: 1 / -1;
}

/* Card */
.card {
  background: #1a1a2e;
  border: 1px solid #2d2d44;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #2d2d44;
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
}

.card-icon {
  color: #6366f1;
}

.card-body {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Pares */
.empty {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  color: #64748b;
  font-size: 0.9rem;
}

.pares-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.par-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid #2d2d44;
}

.par-item:last-child {
  border-bottom: none;
}

.par-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.par-icon {
  color: #6366f1;
}

.par-local {
  font-size: 0.88rem;
  font-weight: 500;
  color: #e2e8f0;
}

.par-remote {
  font-size: 0.78rem;
  color: #64748b;
}

/* Agendamento */
.agend-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.88rem;
  color: #94a3b8;
}

.label {
  color: #94a3b8;
  font-size: 0.88rem;
}

.label-icon {
  color: #6366f1;
  font-size: 0.9rem;
}

/* Resultado */
.resultado {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #2d2d44;
}

.resultado-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.resultado-par {
  font-size: 0.85rem;
  color: #64748b;
}

/* Badges */
.badge {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
}

.badge-success { background: #14532d; color: #86efac; }
.badge-warning { background: #78350f; color: #fcd34d; }
.badge-danger  { background: #7f1d1d; color: #fca5a5; }

/* Botões */
.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.1rem;
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  width: fit-content;
}

.btn-primary:hover { background: #4f46e5; }
.btn-primary:disabled {
  background: #2d2d44;
  color: #64748b;
  cursor: not-allowed;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.1rem;
  background: transparent;
  color: #94a3b8;
  border: 1px solid #2d2d44;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  width: fit-content;
}

.btn-secondary:hover {
  background: #2d2d44;
  color: #e2e8f0;
}
</style>