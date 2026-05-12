<!--
  RcloneSync - Interface gráfica para rclone com Google Drive no Linux
  Copyright (C) 2026 Luimar2

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program. If not, see <https://www.gnu.org/licenses/>.
-->
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'

const router = useRouter()
const store = useConfigStore()

const providers    = ref([])
const providerAtivo = ref('gdrive')
const remotes      = ref([])
const verificando  = ref(null)
const carregando   = ref(true)
const carregandoRemotes = ref(false)
const erro         = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/config/providers')
    providers.value = res.data.providers
  } catch {
    erro.value = 'Não foi possível carregar os providers.'
  } finally {
    carregando.value = false
  }
  await carregarRemotes()
})

watch(providerAtivo, () => carregarRemotes())

async function carregarRemotes() {
  carregandoRemotes.value = true
  erro.value = ''
  remotes.value = []
  try {
    const res = await api.get('/config/remotes', {
      params: { provider: providerAtivo.value }
    })
    remotes.value = res.data.remotes
  } catch (e) {
    erro.value = e.response?.data?.detail || 'Erro ao carregar remotes.'
  } finally {
    carregandoRemotes.value = false
  }
}

async function usarRemote(nome) {
  verificando.value = nome
  erro.value = ''
  try {
    await api.get(`/config/remotes/${nome}/verificar`, {
      params: { provider: providerAtivo.value }
    })
    store.remoteName = nome
    store.provider   = providerAtivo.value
    router.push('/onboarding/3')
  } catch {
    erro.value = `Não foi possível verificar o remote "${nome}".`
  } finally {
    verificando.value = null
  }
}

const providerSelecionado = () =>
  providers.value.find(p => p.id === providerAtivo.value)
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">2 de 6</span>
      <h2 class="step-title">Remote de sincronização</h2>
      <p class="step-desc">Escolha o serviço de cloud e selecione o remote configurado.</p>
    </div>

    <!-- Seleção de provider -->
    <div class="card">
      <p class="section-label">Serviço de cloud</p>
      <div v-if="carregando" class="check-row">
        <span class="pi pi-spin pi-spinner accent" />
        <span class="check-sub">Carregando...</span>
      </div>
      <div v-else class="providers-grid">
        <button
          v-for="p in providers"
          :key="p.id"
          class="provider-btn"
          :class="{
            'provider-active':    providerAtivo === p.id,
            'provider-disabled':  !p.disponivel
          }"
          :title="!p.disponivel ? p.indisponivel_motivo : ''"
          @click="p.disponivel && (providerAtivo = p.id)"
        >
          <span :class="p.icon + ' provider-icon'" />
          <span class="provider-label">{{ p.label }}</span>
          <span v-if="!p.disponivel" class="badge-soon">Em breve</span>
        </button>
      </div>
    </div>

    <!-- Lista de remotes do provider -->
    <div class="card">
      <p class="section-label">
        Remotes configurados
        <span v-if="providerSelecionado()" class="section-provider">
          — {{ providerSelecionado().label }}
        </span>
      </p>

      <div v-if="carregandoRemotes" class="check-row">
        <span class="pi pi-spin pi-spinner accent" />
        <span class="check-sub">Carregando remotes...</span>
      </div>

      <div v-else-if="remotes.length === 0" class="empty-state">
        <span class="pi pi-cloud-upload empty-icon" />
        <p class="check-label">Nenhum remote encontrado</p>
        <p class="check-sub">
          Execute o comando abaixo no terminal para configurar um remote do
          {{ providerSelecionado()?.label }}:
        </p>
        <div class="code-block">
          <code>rclone config</code>
        </div>
        <p class="check-sub">
          Escolha <strong>New remote</strong>, selecione
          <strong>{{ providerSelecionado()?.label }}</strong>
          e siga o assistente de autenticação.
        </p>
      </div>

      <ul v-else class="remotes-list">
        <li v-for="remote in remotes" :key="remote" class="remote-item">
          <div class="remote-info">
            <span :class="providerSelecionado()?.icon + ' remote-icon'" />
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

    <!-- Info -->
    <div class="card info-card">
      <div class="check-row">
        <span class="pi pi-info-circle accent" />
        <p class="check-sub">
          Para criar um novo remote, execute
          <code class="inline-code">rclone config</code>
          no terminal e siga o assistente para o serviço desejado.
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
.section-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.section-provider { color: var(--accent); font-weight: 600; }

/* Provider grid */
.providers-grid {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.provider-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  padding: 0.85rem 1.25rem;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  min-width: 110px;
}
.provider-btn:hover:not(.provider-disabled) {
  border-color: var(--accent);
  background: var(--bg-card-alt);
}
.provider-active {
  border-color: var(--accent) !important;
  background: var(--bg-card-alt) !important;
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent);
}
.provider-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.provider-icon { font-size: 1.4rem; color: var(--accent); }
.provider-label { font-size: 0.82rem; font-weight: 500; color: var(--text-primary); }

.badge-soon {
  font-size: 0.65rem;
  font-weight: 600;
  background: var(--warning-bg);
  color: var(--warning-text);
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
}

/* Remotes */
.check-row  { display: flex; align-items: center; gap: 0.75rem; }
.accent     { color: var(--accent); }
.check-label { font-size: 0.95rem; font-weight: 600; color: var(--text-primary); }
.check-sub  { font-size: 0.85rem; color: var(--text-muted); line-height: 1.5; }

.empty-state {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: flex-start;
}
.empty-icon { font-size: 2rem; color: var(--border); }

.remotes-list { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
.remote-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
}
.remote-item:last-child { border-bottom: none; }
.remote-info { display: flex; align-items: center; gap: 0.75rem; }
.remote-icon { color: var(--accent); font-size: 1.1rem; }

.code-block {
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  width: 100%;
}
code {
  font-size: 0.9rem;
  color: var(--success-text);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}
.inline-code {
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  font-size: 0.82rem;
  color: var(--success-text);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.info-card {
  background: var(--bg-card-alt);
  border-color: var(--accent-border);
}
</style>
