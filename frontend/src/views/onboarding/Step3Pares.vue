<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'

const router = useRouter()
const store = useConfigStore()
const localPath = ref('')
const remotePath = ref('/')
const erro = ref('')
const pares = ref([...store.pares])

async function adicionarPar() {
  if (!localPath.value || !remotePath.value) {
    erro.value = 'Preencha os dois campos.'
    return
  }

  try {
    const res = await api.post('/config/pares', {
      local_path: localPath.value,
      remote_name: store.remoteName,
      remote_path: remotePath.value,
      filtros: store.filtros
    })

    pares.value.push(res.data.par)
    store.pares = pares.value
    localPath.value = ''
    remotePath.value = '/'
    erro.value = ''
  } catch {
    erro.value = 'Erro ao adicionar par.'
  }
}
</script>

<template>
  <main>
    <h2>Passo 3 — Pares de sincronização</h2>
    <p>Remote selecionado: <strong>{{ store.remoteName }}</strong></p>

    <div>
      <label>Pasta local</label>
      <input v-model="localPath" placeholder="/home/usuario/Documentos" />

      <label>Pasta no Google Drive</label>
      <input v-model="remotePath" placeholder="/" />

      <button @click="adicionarPar">Adicionar par</button>
    </div>

    <p v-if="erro" style="color: red">{{ erro }}</p>

    <ul v-if="pares.length > 0">
      <li v-for="par in pares" :key="par.id">
        {{ par.local_path }} → {{ par.remote_name }}:{{ par.remote_path }}
      </li>
    </ul>

    <div>
      <button @click="router.push('/onboarding/2')">Voltar</button>
      <button :disabled="pares.length === 0"
              @click="router.push('/onboarding/4')">Próximo</button>
    </div>
  </main>
</template>