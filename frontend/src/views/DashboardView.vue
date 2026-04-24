<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const pares = ref([])
const agendamento = ref(null)
const sincronizando = ref(false)
const resultado = ref(null)

onMounted(async () => {
  const [paresRes, agendRes] = await Promise.all([
    api.get('/config/pares'),
    api.get('/agendamento/status')
  ])
  pares.value = paresRes.data.pares
  agendamento.value = agendRes.data
})

async function sincronizarAgora() {
  sincronizando.value = true
  resultado.value = null
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
    <h1>RcloneSync — Painel</h1>

    <section>
      <h2>Pares de sincronização</h2>
      <ul>
        <li v-for="par in pares" :key="par.id">
          {{ par.local_path }} → {{ par.remote_name }}:{{ par.remote_path }}
          <span v-if="par.ativo">✅</span>
          <span v-else>⏸️</span>
        </li>
      </ul>
    </section>

    <section>
      <h2>Agendamento</h2>
      <p v-if="agendamento">
        Status: {{ agendamento.ativo ? '✅ Ativo' : '❌ Inativo' }}
      </p>
    </section>

    <section>
      <button :disabled="sincronizando" @click="sincronizarAgora">
        {{ sincronizando ? 'Sincronizando...' : 'Sincronizar agora' }}
      </button>

      <div v-if="resultado">
        <p v-for="r in resultado.resultados" :key="r.par">
          {{ r.par }} — {{ r.sucesso ? '✅ Sucesso' : '❌ Falhou' }}
        </p>
      </div>
    </section>

    <button @click="router.push('/onboarding/1')">
      Reconfigurar
    </button>
  </main>
</template>