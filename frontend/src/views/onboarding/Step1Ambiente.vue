<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()
const rcloneOk = ref(null)
const carregando = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/config/status')
    rcloneOk.value = res.data.rclone_disponivel
  } catch {
    rcloneOk.value = false
  } finally {
    carregando.value = false
  }
})
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">1 de 6</span>
      <h2 class="step-title">Verificação do ambiente</h2>
      <p class="step-desc">Verificando se o rclone está instalado e disponível no sistema.</p>
    </div>

    <div class="card">
      <div v-if="carregando" class="check-row">
        <span class="pi pi-spin pi-spinner check-icon" />
        <span>Verificando...</span>
      </div>

      <div v-else>
        <div class="check-row">
          <span
            :class="rcloneOk
              ? 'pi pi-check-circle check-icon success'
              : 'pi pi-times-circle check-icon danger'"
          />
          <div>
            <p class="check-label">rclone</p>
            <p class="check-sub">
              {{ rcloneOk
                ? 'Encontrado e disponível no sistema.'
                : 'Não encontrado. Instale antes de continuar.' }}
            </p>
          </div>
        </div>

        <div v-if="!rcloneOk" class="code-block">
          <span class="code-label">Instale com:</span>
          <code>sudo apt install rclone</code>
        </div>
      </div>
    </div>

    <div class="step-actions">
      <button
        class="btn-primary"
        :disabled="!rcloneOk"
        @click="router.push('/onboarding/2')"
      >
        Próximo <span class="pi pi-arrow-right" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.step {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 600px;
}

.step-header {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.step-number {
  font-size: 0.8rem;
  color: #6366f1;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.step-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--app-text);
}

.step-desc {
  font-size: 0.9rem;
  color: var(--app-text-muted);
}

.card {
  background: var(--app-surface-card);
  border: 1px solid var(--app-border);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.check-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.check-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.success { color: #86efac; }
.danger  { color: #fca5a5; }

.check-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--app-text);
}

.check-sub {
  font-size: 0.85rem;
  color: var(--app-text-muted);
}

.code-block {
  background: var(--app-surface-input);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.code-label {
  font-size: 0.75rem;
  color: var(--app-text-muted);
}

code {
  font-size: 0.9rem;
  color: #86efac;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.step-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.1rem;
  background: #6366f1;
  color: var(--app-text-inverse);
  border: none;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover { background: #4f46e5; }
.btn-primary:disabled {
  background: var(--app-border);
  color: var(--app-text-muted);
  cursor: not-allowed;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.1rem;
  background: transparent;
  color: var(--app-text-muted-2);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: var(--app-border);
  color: var(--app-text);
}
</style>