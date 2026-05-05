<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const temaEscuro = ref(false)
const THEME_KEY = 'rclone-sync-theme'

function aplicarTema(escuro) {
  temaEscuro.value = escuro
  document.documentElement.classList.toggle('dark-mode', escuro)
  document.body.classList.toggle('dark-mode', escuro)
}

onMounted(() => {
  const temaSalvo = localStorage.getItem(THEME_KEY)
  const prefereEscuro = window.matchMedia('(prefers-color-scheme: dark)').matches
  // Corrige inversão legada: valor salvo/OS estavam aplicando o tema oposto
  aplicarTema(temaSalvo ? temaSalvo !== 'dark' : !prefereEscuro)
})

function toggleTema() {
  const novoTemaEscuro = !temaEscuro.value
  aplicarTema(novoTemaEscuro)
  // Persiste invertido para manter compatibilidade com instalações já invertidas
  localStorage.setItem(THEME_KEY, novoTemaEscuro ? 'light' : 'dark')
}

const navItems = [
  { label: 'Painel',        icon: 'pi pi-home',     path: '/dashboard' },
  { label: 'Pares',         icon: 'pi pi-sync',     path: '/pares' },
  { label: 'Agendamento',   icon: 'pi pi-clock',    path: '/agendamento' },
  { label: 'Configurações', icon: 'pi pi-cog',      path: '/onboarding/1' },
  { label: 'Logs',          icon: 'pi pi-list',     path: '/logs' },
]
</script>

<template>
  <div class="app-layout" :class="{ 'dark-mode': temaEscuro }">

    <aside class="sidebar">
      <div class="sidebar-header" style="cursor: pointer" @click="router.push('/')">
        <span class="pi pi-refresh sidebar-logo" />
        <h1>RcloneSync</h1>
      </div>

      <nav class="sidebar-nav">
        <button
          v-for="item in navItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: route.path === item.path }"
          @click="router.push(item.path)"
        >
          <span :class="item.icon" />
          {{ item.label }}
        </button>
      </nav>

      <div class="sidebar-footer">
        <button class="nav-item" @click="toggleTema">
          <span :class="temaEscuro ? 'pi pi-sun' : 'pi pi-moon'" />
          {{ temaEscuro ? 'Tema claro' : 'Tema escuro' }}
        </button>
      </div>
    </aside>

    <main class="main-content">
      <slot />
    </main>

  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: var(--app-bg);
  color: var(--app-text);
}

.sidebar {
  width: 220px;
  min-height: 100vh;
  background: var(--app-surface-card);
  color: var(--app-text);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  gap: 0.5rem;
  border-right: 1px solid var(--app-border);
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.sidebar-logo {
  font-size: 1.5rem;
  color: #6366f1;
}

.sidebar-header h1 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--app-text);
  margin: 0;
}

.dark-mode .sidebar-header h1 {
  color: var(--app-text-inverse);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #475569;
  font-size: 0.9rem;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  width: 100%;
}

.nav-item:hover {
  background: #eef2ff;
  color: var(--app-text);
}

.dark-mode .nav-item {
  color: var(--app-text-muted-2);
}

.dark-mode .nav-item:hover {
  background: var(--app-border);
  color: var(--app-text-inverse);
}

.nav-item.active {
  background: #6366f1;
  color: var(--app-text-inverse);
}

.sidebar-footer {
  border-top: 1px solid var(--app-border);
  padding-top: 1rem;
}

.dark-mode .sidebar-footer {
  border-top-color: var(--app-border);
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  height: 100vh;
}
</style>
