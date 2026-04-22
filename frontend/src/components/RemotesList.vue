<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const remotes = ref([])
const carregando = ref(true)
const erro = ref(null)

onMounted(async () => {
  try {
    const resposta = await api.get('/config/remotes')
    remotes.value = resposta.data.remotes
  } catch (e) {
    erro.value = 'Não foi possível conectar ao backend.'
  } finally {
    carregando.value = false
  }
})
</script>

<template>
  <div>
    <h2>Remotes configurados</h2>

    <p v-if="carregando">Carregando...</p>
    <p v-else-if="erro">{{ erro }}</p>

    <ul v-else>
      <li v-for="remote in remotes" :key="remote">
        {{ remote }}
      </li>
    </ul>
  </div>
</template>