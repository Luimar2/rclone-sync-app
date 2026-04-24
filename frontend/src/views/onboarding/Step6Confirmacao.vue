<script setup>
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'
import { ref } from 'vue'

const router = useRouter()
const store = useConfigStore()
const sincronizando = ref(false)
const resultado = ref(null)

async function sincronizarAgora() {
  sincronizando.value = true
  try {
    const res = await api.post('/sync/executar-todos')
    resultado.value = res.data
  } finally {
    sincronizando.value = false
  }
}
</script>

<template>
  <main>
    <h2>✅ Configuração concluída!</h2>

    <p>Remote: <strong>{{ store.remoteName }}</strong></p>
    <p>Pares configurados: <strong>{{ store.pares.length }}</strong></p>
    <p>Agendamento: <strong>{{ store.agendamento.intervalo }}</strong></p>

    <hr />

    <button :disabled="sincronizando" @click="sincronizarAgora">
      {{ sincronizando ? 'Sincronizando...' : 'Executar primeiro sync agora' }}
    </button>

    <div v-if="resultado">
      <p v-for="r in resultado.resultados" :key="r.par">
        {{ r.par }} — {{ r.sucesso ? '✅ Sucesso' : '❌ Falhou' }}
      </p>
    </div>

    <br />
    <button @click="router.push('/dashboard')">Ir para o painel</button>
  </main>
</template>