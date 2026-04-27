<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'

const router = useRouter()
const store = useConfigStore()
const sincronizando = ref(false)
const resultado = ref(null)
const erro = ref('')

const intervalos = {
  '1h':    'A cada 1 hora',
  '6h':    'A cada 6 horas',
  '12h':   'A cada 12 horas',
  'daily': 'Uma vez ao dia',
  'custom': store.agendamento.horario_customizado
}

async function sincronizarAgora() {
  sincronizando.value = true
  erro.value = ''
  resultado.value = null
  try {
    const res = await api.post('/sync/executar-todos')
    resultado.value = res.data
  } catch {
    erro.value = 'Erro ao executar a sincronização.'
  } finally {
    sincronizando.value = false
  }
}
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">6 de 6</span>
      <h2 class="step-title">Tudo configurado!</h2>
      <p class="step-desc">
        Confira o resumo da configuração antes de começar.
      </p>
    </div>

    <!-- Resumo -->
    <div class="card">
      <div class="card-section-title">
        <span class="pi pi-list-check accent" />
        Resumo
      </div>

      <ul class="resumo-list">
        <li class="resumo-item">
          <div class="resumo-info">
            <span class="pi pi-cloud resumo-icon" />
            <div>
              <p class="resumo-label">Remote</p>
              <p class="resumo-value">{{ store.remoteName }}</p>
            </div>
          </div>
          <span class="badge badge-success">Verificado</span>
        </li>

        <li class="resumo-item">
          <div class="resumo-info">
            <span class="pi pi-sync resumo-icon" />
            <div>
              <p class="resumo-label">Pares de sincronização</p>
              <p class="resumo-value">{{ store.pares.length }} par(es) configurado(s)</p>
            </div>
          </div>
          <span class="badge badge-success">Ativo</span>
        </li>

        <li class="resumo-item">
          <div class="resumo-info">
            <span class="pi pi-sliders-h resumo-icon" />
            <div>
              <p class="resumo-label">Filtros ativos</p>
              <p class="resumo-value">
                {{
                  Object.entries(store.filtros)
                    .filter(([k, v]) => k !== 'avancado' && v)
                    .length
                }} exclusão(ões) configurada(s)
              </p>
            </div>
          </div>
          <span class="badge badge-success">Configurado</span>
        </li>

        <li class="resumo-item">
          <div class="resumo-info">
            <span class="pi pi-clock resumo-icon" />
            <div>
              <p class="resumo-label">Agendamento</p>
              <p class="resumo-value">
                {{ intervalos[store.agendamento.intervalo] }}
              </p>
            </div>
          </div>
          <span class="badge badge-success">Instalado</span>
        </li>
      </ul>
    </div>

    <!-- Primeiro sync -->
    <div class="card">
      <div class="card-section-title">
        <span class="pi pi-play accent" />
        Executar primeiro sync
      </div>
      <p class="opcao-desc">
        Recomendamos executar a primeira sincronização agora para validar a configuração.
      </p>

      <button
        class="btn-primary"
        :disabled="sincronizando"
        @click="sincronizarAgora"
      >
        <span :class="sincronizando
          ? 'pi pi-spin pi-spinner'
          : 'pi pi-refresh'" />
        {{ sincronizando ? 'Sincronizando...' : 'Sincronizar agora' }}
      </button>

      <div v-if="resultado" class="resultado">
        <div
          v-for="r in resultado.resultados"
          :key="r.par"
          class="resultado-item"
        >
          <span
            class="badge"
            :class="r.sucesso ? 'badge-success' : 'badge-danger'"
          >
            {{ r.sucesso ? 'Sucesso' : 'Falhou' }}
          </span>
          <span class="resultado-par">{{ r.par }}</span>
        </div>
      </div>

      <p v-if="erro" class="erro">
        <span class="pi pi-exclamation-triangle" /> {{ erro }}
      </p>
    </div>

    <!-- Info -->
    <div class="info-card">
      <span class="pi pi-info-circle info-icon" />
      <p class="opcao-desc">
        A sincronização será executada automaticamente conforme o agendamento configurado.
        Você pode acompanhar o status e executar syncs manuais pelo <strong>Painel</strong>.
      </p>
    </div>

    <div class="step-actions">
      <button class="btn-secondary" @click="router.push('/onboarding/5')">
        <span class="pi pi-arrow-left" /> Voltar
      </button>
      <button class="btn-primary" @click="router.push('/dashboard')">
        <span class="pi pi-home" /> Ir para o painel
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
  color: #94a3b8;
  margin-bottom: 0.25rem;
}

.resumo-list {
  list-style: none;
  display: flex;
  flex-direction: column;
}

.resumo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 0;
  border-bottom: 1px solid #2d2d44;
}

.resumo-item:last-child {
  border-bottom: none;
}

.resumo-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.resumo-icon {
  color: #6366f1;
  font-size: 1rem;
  width: 1.2rem;
  text-align: center;
}

.resumo-label {
  font-size: 0.78rem;
  color: #64748b;
}

.resumo-value {
  font-size: 0.9rem;
  font-weight: 500;
  color: #e2e8f0;
}

.opcao-desc {
  font-size: 0.82rem;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 0.75rem;
}

.resultado {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #2d2d44;
}

.resultado-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.resultado-par {
  font-size: 0.82rem;
  color: #64748b;
}

.info-card {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  background: #12122a;
  border: 1px solid #3730a3;
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