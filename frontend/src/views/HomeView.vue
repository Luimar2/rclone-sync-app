<script setup>
import { useRouter } from 'vue-router'
import api from '../services/api'
import { ref, onMounted } from 'vue'

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
  <main>
    <h1>RcloneSync</h1>
    <p>Gerencie seus backups com Google Drive de forma simples.</p>

    <div v-if="carregando">Verificando configuração...</div>

    <div v-else>
      <button v-if="temPares" @click="router.push('/dashboard')">
        Abrir painel
      </button>
      <button v-else @click="router.push('/onboarding/1')">
        Configurar agora
      </button>
    </div>
  </main>
</template>