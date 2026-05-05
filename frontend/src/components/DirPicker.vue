<script setup>
/**
 * DirPicker — seletor de diretório local via API + input manual como fallback.
 * Uso: <DirPicker v-model="localPath" />
 */
import { ref, watch } from 'vue'
import api from '../services/api'

const props = defineProps({
  modelValue: { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue'])

const aberto = ref(false)
const carregando = ref(false)
const erro = ref('')
const atual = ref('')
const parent = ref(null)
const dirs = ref([])
const inputManual = ref(props.modelValue)

watch(() => props.modelValue, v => { inputManual.value = v })

async function abrirPicker() {
  aberto.value = true
  await navegar(inputManual.value || '/home')
}

function fecharPicker() {
  aberto.value = false
  erro.value = ''
}

async function navegar(path) {
  carregando.value = true
  erro.value = ''
  try {
    const res = await api.get('/config/dirs', { params: { path } })
    atual.value = res.data.current
    parent.value = res.data.parent
    dirs.value = res.data.dirs
  } catch {
    erro.value = 'Não foi possível acessar este diretório.'
  } finally {
    carregando.value = false
  }
}

function selecionar(path) {
  inputManual.value = path
  emit('update:modelValue', path)
  fecharPicker()
}

function confirmarManual() {
  emit('update:modelValue', inputManual.value)
}
</script>

<template>
  <div class="dir-picker">
    <!-- Input + botão picker -->
    <div class="input-row">
      <input
        v-model="inputManual"
        class="input"
        placeholder="/home/usuario/Documentos"
        @blur="confirmarManual"
        @keydown.enter="confirmarManual"
      />
      <button class="btn-picker" title="Selecionar pasta" @click="abrirPicker">
        <span class="pi pi-folder-open" />
      </button>
    </div>

    <!-- Modal do picker -->
    <div v-if="aberto" class="picker-overlay" @click.self="fecharPicker">
      <div class="picker-modal">

        <!-- Cabeçalho -->
        <div class="picker-header">
          <span class="pi pi-folder-open picker-header-icon" />
          <span class="picker-title">Selecionar pasta</span>
          <button class="btn-close" @click="fecharPicker">
            <span class="pi pi-times" />
          </button>
        </div>

        <!-- Caminho atual -->
        <div class="picker-path">
          <span class="pi pi-map-marker path-icon" />
          <span class="path-text">{{ atual || '...' }}</span>
        </div>

        <!-- Conteúdo -->
        <div class="picker-body">
          <div v-if="carregando" class="picker-loading">
            <span class="pi pi-spin pi-spinner" />
          </div>

          <div v-else-if="erro" class="picker-erro">
            <span class="pi pi-exclamation-triangle" /> {{ erro }}
          </div>

          <ul v-else class="dir-list">
            <!-- Voltar ao pai -->
            <li
              v-if="parent"
              class="dir-item dir-item-up"
              @click="navegar(parent)"
            >
              <span class="pi pi-arrow-up dir-icon" />
              <span class="dir-name">.. (voltar)</span>
            </li>

            <li
              v-for="dir in dirs"
              :key="dir.path"
              class="dir-item"
              :class="{ 'dir-disabled': !dir.readable }"
              @click="dir.readable && navegar(dir.path)"
            >
              <span class="pi pi-folder dir-icon" />
              <span class="dir-name">{{ dir.name }}</span>
              <span class="pi pi-chevron-right dir-arrow" />
            </li>

            <li v-if="dirs.length === 0" class="dir-empty">
              Nenhuma subpasta encontrada.
            </li>
          </ul>
        </div>

        <!-- Rodapé: selecionar pasta atual -->
        <div class="picker-footer">
          <span class="footer-path">{{ atual }}</span>
          <button class="btn-select" @click="selecionar(atual)">
            <span class="pi pi-check" /> Usar esta pasta
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.dir-picker { position: relative; width: 100%; }

/* Input row */
.input-row { display: flex; gap: 0.4rem; }

.input {
  flex: 1;
  background: #0f0f1a;
  border: 1px solid #2d2d44;
  border-radius: 8px;
  padding: 0.6rem 0.85rem;
  color: #e2e8f0;
  font-size: 0.88rem;
  outline: none;
  transition: border 0.2s;
}
.input:focus { border-color: #6366f1; }

.btn-picker {
  display: flex; align-items: center; justify-content: center;
  width: 38px; height: 38px; flex-shrink: 0;
  background: #1a1a2e; color: #6366f1;
  border: 1px solid #2d2d44; border-radius: 8px;
  cursor: pointer; transition: all 0.2s;
}
.btn-picker:hover { background: #2d2d44; border-color: #6366f1; }

/* Overlay */
.picker-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0, 0, 0, 0.6);
  display: flex; align-items: center; justify-content: center;
}

/* Modal */
.picker-modal {
  background: #1a1a2e;
  border: 1px solid #2d2d44;
  border-radius: 14px;
  width: 440px; max-width: 95vw;
  max-height: 80vh;
  display: flex; flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6);
}

/* Header */
.picker-header {
  display: flex; align-items: center; gap: 0.6rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #2d2d44;
}
.picker-header-icon { color: #6366f1; font-size: 1rem; }
.picker-title { font-size: 0.95rem; font-weight: 600; color: #e2e8f0; flex: 1; }

.btn-close {
  display: flex; align-items: center; justify-content: center;
  width: 28px; height: 28px;
  background: transparent; color: #64748b;
  border: none; border-radius: 6px; cursor: pointer;
  transition: all 0.2s;
}
.btn-close:hover { background: #2d2d44; color: #e2e8f0; }

/* Path bar */
.picker-path {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  background: #0f0f1a;
  border-bottom: 1px solid #2d2d44;
}
.path-icon { color: #6366f1; font-size: 0.8rem; }
.path-text { font-size: 0.78rem; color: #94a3b8; font-family: monospace; word-break: break-all; }

/* Body */
.picker-body { flex: 1; overflow-y: auto; padding: 0.5rem 0; }

.picker-loading {
  display: flex; justify-content: center; padding: 2rem;
  color: #6366f1; font-size: 1.2rem;
}
.picker-erro {
  padding: 1rem 1.25rem;
  font-size: 0.85rem; color: #fca5a5;
  display: flex; align-items: center; gap: 0.4rem;
}

/* Dir list */
.dir-list { list-style: none; }

.dir-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.6rem 1.25rem;
  cursor: pointer;
  transition: background 0.15s;
}
.dir-item:hover { background: #12122a; }

.dir-item-up .dir-icon { color: #94a3b8; }
.dir-icon { color: #6366f1; font-size: 0.95rem; flex-shrink: 0; }

.dir-name { flex: 1; font-size: 0.88rem; color: #e2e8f0; }

.dir-arrow { color: #2d2d44; font-size: 0.7rem; margin-left: auto; }
.dir-item:hover .dir-arrow { color: #6366f1; }

.dir-disabled { opacity: 0.4; cursor: not-allowed; }
.dir-disabled:hover { background: transparent; }

.dir-empty { padding: 1.5rem 1.25rem; font-size: 0.85rem; color: #64748b; text-align: center; }

/* Footer */
.picker-footer {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.85rem 1.25rem;
  border-top: 1px solid #2d2d44;
  background: #0f0f1a;
}
.footer-path {
  flex: 1; font-size: 0.78rem; color: #64748b;
  font-family: monospace; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap;
}

.btn-select {
  display: flex; align-items: center; gap: 0.4rem;
  padding: 0.5rem 1rem;
  background: #6366f1; color: #fff;
  border: none; border-radius: 8px;
  font-size: 0.85rem; font-weight: 500;
  cursor: pointer; transition: background 0.2s;
  white-space: nowrap; flex-shrink: 0;
}
.btn-select:hover { background: #4f46e5; }
</style>
