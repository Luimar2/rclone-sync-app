<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const temaEscuro = ref(false)

onMounted(() => {
  // Detecta preferência do sistema
  const prefereEscuro = window.matchMedia('(prefers-color-scheme: dark)').matches
  temaEscuro.value = prefereEscuro
  document.body.classList.toggle('dark-mode', prefereEscuro)

  // Fica escutando mudanças em tempo real
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    temaEscuro.value = e.matches
    document.body.classList.toggle('dark-mode', e.matches)
  })
})

function toggleTema() {
  temaEscuro.value = !temaEscuro.value
  document.body.classList.toggle('dark-mode', temaEscuro.value)
}

const navItems = [
  { label: 'Painel',       icon: 'pi pi-home',  path: '/dashboard' },
  { label: 'Configuração', icon: 'pi pi-cog',   path: '/onboarding/1' },
  { label: 'Logs',         icon: 'pi pi-list',  path: '/logs' },
]
</script>

<template>
  <div class="app-layout" :class="{ 'dark-mode': temaEscuro }">

    <aside class="sidebar">
      <div class="sidebar-header">
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
  background: #f4f6f9;
  color: #1a1a2e;
}

.dark-mode .app-layout,
.dark-mode {
  background: #0f0f1a;
  color: #e2e8f0;
}

.sidebar {
  width: 220px;
  min-height: 100vh;
  background: #1a1a2e;
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  gap: 0.5rem;
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
  color: #fff;
  margin: 0;
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
  color: #94a3b8;
  font-size: 0.9rem;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  width: 100%;
}

.nav-item:hover {
  background: #2d2d44;
  color: #fff;
}

.nav-item.active {
  background: #6366f1;
  color: #fff;
}

.sidebar-footer {
  border-top: 1px solid #2d2d44;
  padding-top: 1rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  height: 100vh;
}
</style>