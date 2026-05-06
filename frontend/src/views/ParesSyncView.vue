<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import DirPicker from '../components/DirPicker.vue'

const pares = ref([])
const carregando = ref(true)
const erro = ref('')
const sucesso = ref('')

// Modal de edição
const editando = ref(null)       // par sendo editado
const editLocalPath = ref('')
const editRemotePath = ref('')
const salvandoEdicao = ref(false)

// Exclusão
const excluindo = ref(null)

onMounted(async () => {
  await carregarPares()
})

async function carregarPares() {
  carregando.value = true
  try {
    const res = await api.get('/config/pares')
    pares.value = res.data.pares
  } catch {
    erro.value = 'Não foi possível carregar os pares.'
  } finally {
    carregando.value = false
  }
}

function abrirEdicao(par) {
  editando.value = par.id
  editLocalPath.value = par.local_path
  editRemotePath.value = par.remote_path
  erro.value = ''
  sucesso.value = ''
}

function cancelarEdicao() {
  editando.value = null
  editLocalPath.value = ''
  editRemotePath.value = ''
}

async function salvarEdicao(par) {
  if (!editLocalPath.value || !editRemotePath.value) {
    erro.value = 'Preencha os dois campos.'
    return
  }

  salvandoEdicao.value = true
  erro.value = ''
  sucesso.value = ''

  try {
    const res = await api.patch(`/config/pares/${par.id}`, {
      local_path: editLocalPath.value,
      remote_path: editRemotePath.value,
    })
    const idx = pares.value.findIndex(p => p.id === par.id)
    if (idx !== -1) pares.value[idx] = res.data.par
    sucesso.value = 'Par atualizado com sucesso.'
    cancelarEdicao()
  } catch {
    erro.value = 'Erro ao salvar. Tente novamente.'
  } finally {
    salvandoEdicao.value = false
  }
}

async function excluirPar(par) {
  excluindo.value = par.id
  erro.value = ''
  sucesso.value = ''
  try {
    await api.delete(`/config/pares/${par.id}`)
    pares.value = pares.value.filter(p => p.id !== par.id)
    sucesso.value = 'Par excluído com sucesso.'
  } catch {
    erro.value = 'Erro ao excluir par.'
  } finally {
    excluindo.value = null
  }
}

async function toggleAtivo(par) {
  try {
    await api.patch(`/config/pares/${par.id}/ativo`, null, {
      params: { ativo: !par.ativo }
    })
    par.ativo = !par.ativo
  } catch {
    erro.value = 'Erro ao alterar status do par.'
  }
}
</script>

<template>
  <div class="page">
    <h2 class="page-title">Pares de Sincronização</h2>
    <p class="page-desc">Gerencie os pares de pastas locais e remotas configurados.</p>

    <!-- Feedback -->
    <p v-if="erro"    class="erro">     <span class="pi pi-exclamation-triangle" /> {{ erro }} </p>
    <p v-if="sucesso" class="success-msg"><span class="pi pi-check-circle" /> {{ sucesso }} </p>

    <!-- Carregando -->
    <div v-if="carregando" class="loading">
      <span class="pi pi-spin pi-spinner loading-icon" />
    </div>

    <!-- Nenhum par -->
    <div v-else-if="pares.length === 0" class="card empty-card">
      <span class="pi pi-inbox empty-icon" />
      <p class="empty-label">Nenhum par configurado.</p>
      <p class="empty-desc">Adicione pares pelo fluxo de Configurações.</p>
    </div>

    <!-- Lista de pares -->
    <div v-else class="pares-list">
      <div
        v-for="par in pares"
        :key="par.id"
        class="par-card"
        :class="{ 'par-editando': editando === par.id }"
      >
        <!-- Cabeçalho do par -->
        <div class="par-header">
          <span class="pi pi-folder par-icon" />
          <div class="par-paths">
            <p class="par-local">{{ par.local_path }}</p>
            <p class="par-remote">{{ par.remote_name }}:{{ par.remote_path }}</p>
          </div>
          <span class="badge ml-auto" :class="par.ativo ? 'badge-success' : 'badge-warning'">
            {{ par.ativo ? 'Ativo' : 'Pausado' }}
          </span>
        </div>

        <!-- Formulário de edição inline -->
        <div v-if="editando === par.id" class="edit-form">
          <div class="form-grid">
            <div class="input-group">
              <label class="input-label"><span class="pi pi-folder" /> Pasta local</label>
              <DirPicker v-model="editLocalPath" />
            </div>
            <div class="input-group">
              <label class="input-label"><span class="pi pi-cloud" /> Pasta no Google Drive</label>
              <input v-model="editRemotePath" class="input" placeholder="/" />
            </div>
          </div>
          <div class="edit-actions">
            <button class="btn-secondary" @click="cancelarEdicao">
              <span class="pi pi-times" /> Cancelar
            </button>
            <button class="btn-primary" :disabled="salvandoEdicao" @click="salvarEdicao(par)">
              <span :class="salvandoEdicao ? 'pi pi-spin pi-spinner' : 'pi pi-check'" />
              {{ salvandoEdicao ? 'Salvando...' : 'Salvar' }}
            </button>
          </div>
        </div>

        <!-- Ações -->
        <div v-else class="par-actions">
          <button class="btn-icon" title="Pausar/Ativar" @click="toggleAtivo(par)">
            <span :class="par.ativo ? 'pi pi-pause' : 'pi pi-play'" />
          </button>
          <button class="btn-icon" title="Editar" @click="abrirEdicao(par)">
            <span class="pi pi-pencil" />
          </button>
          <button
            class="btn-icon btn-icon-danger"
            title="Excluir"
            :disabled="excluindo === par.id"
            @click="excluirPar(par)"
          >
            <span :class="excluindo === par.id ? 'pi pi-spin pi-spinner' : 'pi pi-trash'" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { display: flex; flex-direction: column; gap: 1.25rem; }

.page-title { font-size: 1.3rem; font-weight: 700; color: var(--text-primary); }
.page-desc  { font-size: 0.88rem; color: var(--text-muted); margin-top: -0.75rem; }

.loading { display: flex; justify-content: center; padding: 3rem; }
.loading-icon { font-size: 2rem; color: #6366f1; }

/* Empty */
.empty-card {
  display: flex; flex-direction: column; align-items: center;
  gap: 0.5rem; padding: 2.5rem; text-align: center;
  background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px;
}
.empty-icon  { font-size: 2rem; color: var(--border); }
.empty-label { font-size: 0.95rem; font-weight: 600; color: var(--text-secondary); }
.empty-desc  { font-size: 0.82rem; color: var(--text-muted); }

/* Par card */
.pares-list { display: flex; flex-direction: column; gap: 0.75rem; }

.par-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: border-color 0.2s;
}
.par-editando { border-color: var(--accent); }

.par-header {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 1rem 1.25rem;
}

.par-icon { color: #6366f1; font-size: 1.1rem; flex-shrink: 0; }

.par-paths { display: flex; flex-direction: column; gap: 0.15rem; min-width: 0; }
.par-local  { font-size: 0.88rem; font-weight: 500; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.par-remote { font-size: 0.78rem; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.ml-auto { margin-left: auto; flex-shrink: 0; }

/* Edit form */
.edit-form {
  border-top: 1px solid var(--border);
  padding: 1rem 1.25rem;
  display: flex; flex-direction: column; gap: 0.75rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.input-group { display: flex; flex-direction: column; gap: 0.35rem; }
.input-label { font-size: 0.78rem; color: var(--text-secondary); font-weight: 500; display: flex; align-items: center; gap: 0.3rem; }

.input {
  background: var(--bg-input); border: 1px solid var(--border);
  border-radius: 8px; padding: 0.55rem 0.85rem;
  color: var(--text-primary); font-size: 0.85rem; outline: none;
  transition: border 0.2s;
}
.input:focus { border-color: var(--accent); }

.edit-actions { display: flex; justify-content: flex-end; gap: 0.5rem; }

/* Par actions */
.par-actions {
  display: flex; justify-content: flex-end; gap: 0.4rem;
  padding: 0.6rem 1rem;
  border-top: 1px solid var(--border);
}

.btn-icon {
  display: flex; align-items: center; justify-content: center;
  width: 32px; height: 32px;
  background: transparent; color: var(--text-secondary);
  border: 1px solid var(--border); border-radius: 8px;
  cursor: pointer; transition: all 0.2s;
}
.btn-icon:hover { background: var(--nav-item-hover-bg); color: var(--text-primary); }

.btn-icon-danger { color: var(--danger-text); border-color: var(--danger-bg); }
.btn-icon-danger:hover { background: var(--danger-bg); color: #fff; }
.btn-icon:disabled { opacity: 0.5; cursor: not-allowed; }

/* Buttons */
.btn-primary {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.55rem 1rem; background: #6366f1; color: #fff;
  border: none; border-radius: 8px; font-size: 0.85rem;
  font-weight: 500; cursor: pointer; transition: background 0.2s;
}
.btn-primary:hover { background: #4f46e5; }
.btn-primary:disabled { background: var(--nav-item-hover-bg); color: var(--text-muted); cursor: not-allowed; }

.btn-secondary {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.55rem 1rem; background: transparent; color: var(--text-secondary);
  border: 1px solid var(--border); border-radius: 8px; font-size: 0.85rem;
  font-weight: 500; cursor: pointer; transition: all 0.2s;
}
.btn-secondary:hover { background: var(--nav-item-hover-bg); color: var(--text-primary); }

/* Badges */
.badge { font-size: 0.72rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 999px; }
.badge-success { background: var(--success-bg); color: var(--success-text); }
.badge-warning { background: var(--warning-bg); color: var(--warning-text); }

/* Feedback */
.erro        { font-size: 0.85rem; color: var(--danger-text); display: flex; align-items: center; gap: 0.4rem; }
.success-msg { font-size: 0.85rem; color: var(--success-text); display: flex; align-items: center; gap: 0.4rem; }
</style>
