<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const temPares = ref(false)
const carregando = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/config/pares')
    temPares.value = res.data.pares.length > 0
  } catch {
    temPares.value = false
  } finally {
    carregando.value = false
  }
})
</script>

<template>
  <div class="home">
    <div class="home-content">

      <!-- Logo e título -->
      <div class="hero">
        <div class="hero-icon">
          <span class="pi pi-refresh" />
        </div>
        <h1 class="hero-title">RcloneSync</h1>
        <p class="hero-sub">
          Gerencie seus backups com Google Drive de forma simples,
          segura e automatizada no Linux.
        </p>
      </div>

      <!-- Features -->
      <div class="features">
        <div class="feature-item">
          <span class="pi pi-shield feature-icon" />
          <div>
            <p class="feature-label">Seguro</p>
            <p class="feature-desc">Snapshot local antes de cada sync</p>
          </div>
        </div>
        <div class="feature-item">
          <span class="pi pi-clock feature-icon" />
          <div>
            <p class="feature-label">Automatizado</p>
            <p class="feature-desc">Agendamento via systemd --user</p>
          </div>
        </div>
        <div class="feature-item">
          <span class="pi pi-sliders-h feature-icon" />
          <div>
            <p class="feature-label">Flexível</p>
            <p class="feature-desc">Múltiplos pares e filtros de exclusão</p>
          </div>
        </div>
      </div>

      <!-- Ação principal -->
      <div class="actions">
        <div v-if="carregando" class="loading">
          <span class="pi pi-spin pi-spinner loading-icon" />
        </div>

        <div v-else class="action-buttons">
          <button
            v-if="temPares"
            class="btn-primary"
            @click="router.push('/dashboard')"
          >
            <span class="pi pi-home" />
            Abrir painel
          </button>

          <button
            v-else
            class="btn-primary"
            @click="router.push('/onboarding/1')"
          >
            <span class="pi pi-play" />
            Começar configuração
          </button>

          <button
            v-if="temPares"
            class="btn-secondary"
            @click="router.push('/onboarding/1')"
          >
            <span class="pi pi-cog" />
            Configurações
          </button>
        </div>
      </div>

      <!-- Rodapé -->
      <div class="home-footer">
        
        <a href="https://github.com/Luimar2/rclone-sync-app#"
          target="_blank"
          class="footer-link"
        >
          <span class="pi pi-github">GitHub</span>
        </a>
        <span class="footer-sep">·</span>
        <span class="footer-version">v0.1.1</span>
      </div>

    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: var(--bg-page);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.home-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2.5rem;
  max-width: 480px;
  width: 100%;
  text-align: center;
}

/* Hero */
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.hero-icon {
  width: 72px;
  height: 72px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-icon .pi {
  font-size: 2rem;
  color: #6366f1;
}

.hero-title {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin: 0;
}

.hero-sub {
  font-size: 0.95rem;
  color: var(--text-muted);
  line-height: 1.6;
  margin: 0;
}

/* Features */
.features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  text-align: left;
}

.feature-icon {
  color: #6366f1;
  font-size: 1.2rem;
  width: 1.5rem;
  text-align: center;
  flex-shrink: 0;
}

.feature-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
}

.feature-desc {
  font-size: 0.8rem;
  color: var(--text-muted);
}

/* Actions */
.actions {
  width: 100%;
}

.loading {
  display: flex;
  justify-content: center;
}

.loading-icon {
  font-size: 1.5rem;
  color: #6366f1;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.85rem 1.5rem;
  background: #6366f1;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  width: 100%;
}

.btn-primary:hover { background: #4f46e5; }

.btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.85rem 1.5rem;
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}

.btn-secondary:hover {
  background: var(--bg-card);
  color: var(--text-primary);
}

/* Footer */
.home-footer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: var(--text-muted);
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover { color: var(--text-primary); }

.footer-sep { color: var(--border); }
</style>