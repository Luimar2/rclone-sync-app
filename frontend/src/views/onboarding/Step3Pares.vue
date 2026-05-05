<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'
import DirPicker from '../../components/DirPicker.vue'

const router = useRouter()
const store = useConfigStore()
const localPath = ref('')
const remotePath = ref('/')
const erro = ref('')
const adicionando = ref(false)
const pares = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/config/pares')
    pares.value = res.data.pares
  } catch {
    erro.value = 'Não foi possível carregar os pares.'
  }
})

async function adicionarPar() {
  if (!localPath.value || !remotePath.value) {
    erro.value = 'Preencha os dois campos.'
    return
  }

  adicionando.value = true
  erro.value = ''

  try {
    const res = await api.post('/config/pares', {
      local_path: localPath.value,
      remote_name: store.remoteName,
      remote_path: remotePath.value,
      filtros: store.filtros
    })
    pares.value.push(res.data.par)
    store.pares = pares.value
    localPath.value = ''
    remotePath.value = '/'
  } catch {
    erro.value = 'Erro ao adicionar par. Verifique os caminhos informados.'
  } finally {
    adicionando.value = false
  }
}

async function removerPar(id) {
  try {
    await api.delete(`/config/pares/${id}`)
    pares.value = pares.value.filter(p => p.id !== id)
    store.pares = pares.value
  } catch {
    erro.value = 'Erro ao remover par.'
  }
}
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">3 de 6</span>
      <h2 class="step-title">Pares de sincronização</h2>
      <p class="step-desc">
        Defina quais pastas locais serão sincronizadas com o Google Drive.
        Remote selecionado: <strong class="accent">{{ store.remoteName }}</strong>
      </p>
    </div>

    <!-- Formulário -->
    <div class="card">
      <div class="card-section-title">
        <span class="pi pi-plus-circle accent" />
        Adicionar par
      </div>

      <div class="form-grid">
        <div class="input-group">
          <label class="input-label">
            <span class="pi pi-folder" /> Pasta local
          </label>
          <DirPicker v-model="localPath" />
        </div>

        <div class="input-group">
          <label class="input-label">
            <span class="pi pi-cloud" /> Pasta no Google Drive
          </label>
          <input
            v-model="remotePath"
            class="input"
            placeholder="/"
          />
        </div>
      </div>

      <p v-if="erro" class="erro">
        <span class="pi pi-exclamation-triangle" /> {{ erro }}
      </p>

      <button
        class="btn-primary"
        :disabled="adicionando"
        @click="adicionarPar"
      >
        <span :class="adicionando ? 'pi pi-spin pi-spinner' : 'pi pi-plus'" />
        {{ adicionando ? 'Adicionando...' : 'Adicionar par' }}
      </button>
    </div>

    <!-- Lista de pares -->
    <div v-if="pares.length > 0" class="card">
      <div class="card-section-title">
        <span class="pi pi-list accent" />
        Pares configurados
      </div>

      <ul class="pares-list">
        <li v-for="par in pares" :key="par.id" class="par-item">
          <div class="par-info">
            <span class="pi pi-folder par-icon" />
            <div>
              <p class="par-local">{{ par.local_path }}</p>
              <p class="par-remote">
                {{ par.remote_name }}:{{ par.remote_path }}
              </p>
            </div>
          </div>
          <button class="btn-danger" @click="removerPar(par.id)">
            <span class="pi pi-trash" />
          </button>
        </li>
      </ul>
    </div>

    <div class="step-actions">
      <button class="btn-secondary" @click="router.push('/onboarding/2')">
        <span class="pi pi-arrow-left" /> Voltar
      </button>
      <button
        class="btn-primary"
        :disabled="pares.length === 0"
        @click="router.push('/onboarding/4')"
      >
        Próximo <span class="pi pi-arrow-right" />
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.pares-list {
  list-style: none;
  display: flex;
  flex-direction: column;
}

.par-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
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

.par-icon { color: #6366f1; }

.par-local {
  font-size: 0.88rem;
  font-weight: 500;
  color: #e2e8f0;
}

.par-remote {
  font-size: 0.78rem;
  color: #64748b;
}

.btn-danger {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  background: transparent;
  color: #fca5a5;
  border: 1px solid #7f1d1d;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-danger:hover {
  background: #7f1d1d;
  color: #fff;
}
</style>