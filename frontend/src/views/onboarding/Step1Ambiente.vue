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
  <main>
    <h2>Passo 1 — Verificação do ambiente</h2>

    <div v-if="carregando">Verificando...</div>

    <div v-else>
      <p v-if="rcloneOk">✅ rclone encontrado e disponível.</p>
      <div v-else>
        <p>❌ rclone não encontrado.</p>
        <p>Instale com: <code>sudo apt install rclone</code></p>
      </div>

      <button :disabled="!rcloneOk" @click="router.push('/onboarding/2')">
        Próximo
      </button>
    </div>
  </main>
</template>