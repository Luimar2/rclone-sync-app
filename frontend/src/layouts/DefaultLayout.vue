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
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const temaEscuro = ref(false)

function aplicarTema(escuro) {
  temaEscuro.value = escuro
  document.documentElement.classList.toggle('dark-mode', escuro)
  // Remover do body — só o html precisa ser ancestral dos tokens
  document.documentElement.setAttribute('data-theme', escuro ? 'dark' : 'light')
  localStorage.setItem('tema', escuro ? 'dark' : 'light')
}

onMounted(() => {
  // Preferência salva tem prioridade; se não, usa a do sistema
  const salvo = localStorage.getItem('tema')
  const prefereEscuro = salvo
    ? salvo === 'dark'
    : window.matchMedia('(prefers-color-scheme: dark)').matches

  aplicarTema(prefereEscuro)

  // Acompanha mudança do sistema apenas se o usuário não salvou preferência
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('tema')) {
      aplicarTema(e.matches)
    }
  })
})

function toggleTema() {
  aplicarTema(!temaEscuro.value)
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
  <div class="app-layout">

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
          <span :class="temaEscuro ? 'pi pi-moon' : 'pi pi-sun'" />
          {{ temaEscuro ? 'Tema escuro' : 'Tema claro' }}
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
  background: var(--bg-page);
  color: var(--text-primary);
  transition: background 0.3s, color 0.3s;
}

.sidebar {
  width: 220px;
  min-height: 100vh;
  background: var(--bg-sidebar);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  gap: 0.5rem;
  transition: background 0.3s, color 0.3s, border-color 0.3s;
  border-right: 1px solid var(--border);
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.sidebar-logo {
  font-size: 1.5rem;
  color: var(--accent);
}

.sidebar-header h1 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--sidebar-header-text);
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
  color: var(--nav-item-text);
  font-size: 0.9rem;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  width: 100%;
}

.nav-item:hover {
  background: var(--nav-item-hover-bg);
  color: var(--nav-item-hover-text);
}

.nav-item.active {
  background: var(--nav-item-active-bg);
  color: var(--nav-item-active-text);
}

.sidebar-footer {
  border-top: 1px solid var(--sidebar-footer-border);
  padding-top: 1rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  height: 100vh;
  background: var(--bg-page);
  color: var(--text-primary);
  transition: background 0.2s, color 0.2s;
}
</style>