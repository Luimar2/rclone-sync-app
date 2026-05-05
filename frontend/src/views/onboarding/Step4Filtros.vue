<script setup>
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'

const router = useRouter()
const store = useConfigStore()

const filtrosComuns = [
  {
    key: 'arquivos_temporarios',
    label: 'Arquivos temporários',
    desc: '*.tmp, *.temp',
    icon: 'pi pi-file'
  },
  {
    key: 'lixeira',
    label: 'Lixeira',
    desc: '.Trash/**',
    icon: 'pi pi-trash'
  },
  {
    key: 'cache',
    label: 'Cache',
    desc: '**/cache/**, **/Cache/**',
    icon: 'pi pi-database'
  },
  {
    key: 'git',
    label: 'Repositórios Git',
    desc: '.git/**',
    icon: 'pi pi-code'
  },
  {
    key: 'arquivos_ocultos',
    label: 'Arquivos ocultos',
    desc: '.*',
    icon: 'pi pi-eye-slash'
  },
]
</script>

<template>
  <div class="step">
    <div class="step-header">
      <span class="step-number">4 de 6</span>
      <h2 class="step-title">Filtros de exclusão</h2>
      <p class="step-desc">
        Defina o que não deve ser sincronizado com o Google Drive.
      </p>
    </div>

    <!-- Filtros comuns -->
    <div class="card">
      <div class="card-section-title">
        <span class="pi pi-sliders-h accent" />
        Exclusões comuns
      </div>

      <ul class="filtros-list">
        <li
          v-for="filtro in filtrosComuns"
          :key="filtro.key"
          class="filtro-item"
          @click="store.filtros[filtro.key] = !store.filtros[filtro.key]"
        >
          <div class="filtro-info">
            <span :class="filtro.icon + ' filtro-icon'" />
            <div>
              <p class="filtro-label">{{ filtro.label }}</p>
              <p class="filtro-desc">{{ filtro.desc }}</p>
            </div>
          </div>
          <div
            class="toggle"
            :class="{ 'toggle-on': store.filtros[filtro.key] }"
          >
            <div class="toggle-thumb" />
          </div>
        </li>
      </ul>
    </div>

    <!-- Filtros avançados -->
    <div class="card">
      <div class="card-section-title">
        <span class="pi pi-code accent" />
        Filtros avançados
        <span class="badge-opcional">opcional</span>
      </div>
      <p class="filtro-desc">
        Um filtro por linha no formato do rclone. Exemplo:
      </p>
      <div class="code-block">
        <code>- *.log</code><br />
        <code>- **/node_modules/**</code>
      </div>
      <textarea
        v-model="store.filtros.avancado"
        class="textarea"
        placeholder="- *.log&#10;- **/node_modules/**"
        rows="4"
      />
    </div>

    <div class="step-actions">
      <button class="btn-secondary" @click="router.push('/onboarding/3')">
        <span class="pi pi-arrow-left" /> Voltar
      </button>
      <button class="btn-primary" @click="router.push('/onboarding/5')">
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
  color: var(--app-text-muted-2);
  margin-bottom: 0.25rem;
}

.badge-opcional {
  font-size: 0.7rem;
  font-weight: 500;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: var(--app-border);
  color: var(--app-text-muted);
  margin-left: 0.25rem;
}

.filtros-list {
  list-style: none;
  display: flex;
  flex-direction: column;
}

.filtro-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 0;
  border-bottom: 1px solid var(--app-border);
  cursor: pointer;
  transition: background 0.15s;
  border-radius: 6px;
}

.filtro-item:last-child {
  border-bottom: none;
}

.filtro-item:hover {
  background: var(--app-surface-alt);
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}

.filtro-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.filtro-icon {
  color: #6366f1;
  font-size: 1rem;
  width: 1.2rem;
  text-align: center;
}

.filtro-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--app-text);
}

.filtro-desc {
  font-size: 0.78rem;
  color: var(--app-text-muted);
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Toggle switch */
.toggle {
  width: 40px;
  height: 22px;
  background: var(--app-border);
  border-radius: 999px;
  padding: 2px;
  transition: background 0.2s;
  flex-shrink: 0;
}

.toggle-on {
  background: #6366f1;
}

.toggle-thumb {
  width: 18px;
  height: 18px;
  background: var(--app-text-inverse);
  border-radius: 999px;
  transition: transform 0.2s;
}

.toggle-on .toggle-thumb {
  transform: translateX(18px);
}

.code-block {
  background: var(--app-surface-input);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
}

code {
  font-size: 0.82rem;
  color: #86efac;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

.textarea {
  background: var(--app-surface-input);
  border: 1px solid var(--app-border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: var(--app-text);
  font-size: 0.85rem;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  outline: none;
  resize: vertical;
  width: 100%;
  transition: border 0.2s;
  line-height: 1.6;
}

.textarea:focus {
  border-color: #6366f1;
}
</style>