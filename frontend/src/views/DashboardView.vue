<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Divider from 'primevue/divider'
import ProgressSpinner from 'primevue/progressspinner'

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
      <ProgressSpinner />
    </div>

    <div v-else class="grid">

      <!-- Card de pares -->
      <Card class="card">
        <template #title>
          <span class="pi pi-sync card-icon" />
          Pares de sincronização
        </template>
        <template #content>
          <div v-if="pares.length === 0" class="empty">
            Nenhum par configurado.
            <Button
              label="Configurar agora"
              icon="pi pi-plus"
              size="small"
              class="mt"
              @click="router.push('/onboarding/1')"
            />
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
              <Tag
                :value="par.ativo ? 'Ativo' : 'Pausado'"
                :severity="par.ativo ? 'success' : 'warning'"
              />
            </li>
          </ul>
        </template>
      </Card>

      <!-- Card de agendamento -->
      <div v-if="agendamento">
    <div class="agend-status">
      <span>Status</span>
      <Tag
        :value="agendamento.ativo ? 'Ativo' : 'Inativo'"
        :severity="agendamento.ativo ? 'success' : 'danger'"
      />
    </div>
    <Divider />
    <div class="agend-info">
      <span class="pi pi-calendar" />
      <span>Sincronização agendada via systemd</span>
    </div>
    <Button
      label="Gerenciar agendamento"
      icon="pi pi-cog"
      severity="secondary"
      size="small"
      class="mt"
      @click="router.push('/onboarding/5')"
    />
  </div>

      <!-- Card de ação -->
      <Card class="card card-full">
        <template #title>
          <span class="pi pi-play card-icon" />
          Sincronização manual
        </template>
        <template #content>
          <Button
            label="Sincronizar agora"
            icon="pi pi-refresh"
            :loading="sincronizando"
            :disabled="pares.length === 0"
            @click="sincronizarAgora"
          />

          <div v-if="resultado" class="resultado">
            <Divider />
            <div
              v-for="r in resultado.resultados"
              :key="r.par"
              class="resultado-item"
            >
              <Tag
                :value="r.sucesso ? 'Sucesso' : 'Falhou'"
                :severity="r.sucesso ? 'success' : 'danger'"
              />
              <span class="resultado-par">{{ r.par }}</span>
            </div>
          </div>
        </template>
      </Card>

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
  font-size: 1.4rem;
  font-weight: 700;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

.card-full {
  grid-column: 1 / -1;
}

.card-icon {
  margin-right: 0.5rem;
  color: #6366f1;
}

.empty {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: #94a3b8;
}

.mt {
  margin-top: 1rem;
  width: fit-content;
}

.pares-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.par-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.par-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.par-icon {
  color: #6366f1;
  font-size: 1.2rem;
}

.par-local {
  font-weight: 500;
  font-size: 0.9rem;
}

.par-remote {
  font-size: 0.8rem;
  color: #94a3b8;
}

.agend-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.agend-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #94a3b8;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.resultado {
  margin-top: 0.5rem;
}

.resultado-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0;
}

.resultado-par {
  font-size: 0.85rem;
  color: #64748b;
}
</style>