<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'

const router = useRouter()
const store = useConfigStore()
const remotes = ref([])
const erro = ref('')
const verificando = ref(null)
const carregando = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/config/remotes')
    remotes.value = res.data.remotes
  } catch {
    erro.value = 'Não foi possível carregar os remotes.'
  } finally {
    carregando.value = false
  }
})

async function usarRemote(nome) {
  verificando.value = nome
  erro.value = ''
  try {
    await api.get(`/config/remotes/${nome}/verificar`)
    store.remoteName = nome
    router.push('/onboarding/3')
  } catch {
    erro.value = `Não foi possível verificar o remote "${nome}".`
  } finally {
    verificando.value = null
  }
}
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">2 de 6</span>
      <h2 class="step-title">Remote Google Drive</h2>
      <p class="step-desc">Selecione o remote do Google Drive que deseja usar para sincronização.</p>
    </div>

    <div class="card">
      <div v-if="carregando" class="check-row">
        <span class="pi pi-spin pi-spinner check-icon accent" />
        <span class="check-sub">Carregando remotes...</span>
      </div>

      <div v-else-if="remotes.length === 0" class="empty-state">
        <span class="pi pi-cloud-upload empty-icon" />
        <p class="check-label">Nenhum remote encontrado</p>
        <p class="check-sub">Execute o comando abaixo no terminal para configurar um remote do Google Drive:</p>
        <div class="code-block">
          <code>rclone config</code>
        </div>
        <p class="check-sub">Escolha a opção <strong>New remote</strong>, selecione <strong>Google Drive</strong> e siga o assistente.</p>
      </div>

      <ul v-else class="remotes-list">
        <li
          v-for="remote in remotes"
          :key="remote"
          class="remote-item"
        >
          <div class="remote-info">
            <span class="pi pi-cloud remote-icon" />
            <span class="check-label">{{ remote }}</span>
          </div>
          <button
            class="btn-primary"
            :disabled="verificando === remote"
            @click="usarRemote(remote.replace(':', ''))"
          >
            <span :class="verificando === remote
              ? 'pi pi-spin pi-spinner'
              : 'pi pi-check'" />
            {{ verificando === remote ? 'Verificando...' : 'Usar este' }}
          </button>
        </li>
      </ul>

      <p v-if="erro" class="erro">
        <span class="pi pi-exclamation-triangle" /> {{ erro }}
      </p>
    </div>

    <div class="card info-card">
      <div class="check-row">
        <span class="pi pi-info-circle accent" />
        <p class="check-sub">
          Para criar um novo remote, execute <code class="inline-code">rclone config</code> no terminal e siga o assistente para adicionar um remote do tipo <strong>Google Drive</strong>.
        </p>
      </div>
    </div>

    <div class="step-actions">
      <button class="btn-secondary" @click="router.push('/onboarding/1')">
        <span class="pi pi-arrow-left" /> Voltar
      </button>
    </div>
  </div>
</template>

<style scoped>
.check-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.check-icon { font-size: 1.4rem; }
.accent { color: #6366f1; }

.check-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
}

.check-sub {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.5;
}

.empty-state {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: flex-start;
}

.empty-icon {
  font-size: 2rem;
  color: #2d2d44;
}

.remotes-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.remote-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #2d2d44;
}

.remote-item:last-child {
  border-bottom: none;
}

.remote-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.remote-icon {
  color: #6366f1;
  font-size: 1.1rem;
}

.code-block {
  background: #0f0f1a;
  border: 1px solid #2d2d44;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  width: 100%;
}

code {
  font-size: 0.9rem;
  color: #86efac;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.inline-code {
  background: #0f0f1a;
  border: 1px solid #2d2d44;
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  font-size: 0.82rem;
  color: #86efac;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.info-card {
  background: #12122a;
  border-color: #3730a3;
}
</style>