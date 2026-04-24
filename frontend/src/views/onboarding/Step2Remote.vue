<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'

const router = useRouter()
const store = useConfigStore()
const remotes = ref([])
const nomeRemote = ref('')
const erro = ref('')
const carregando = ref(false)

async function carregarRemotes() {
  const res = await api.get('/config/remotes')
  remotes.value = res.data.remotes
}

async function usarRemote(nome) {
  try {
    await api.get(`/config/remotes/${nome}/verificar`)
    store.remoteName = nome
    router.push('/onboarding/3')
  } catch {
    erro.value = `Não foi possível verificar o remote "${nome}".`
  }
}

carregarRemotes()
</script>

<template>
  <main>
    <h2>Passo 2 — Remote Google Drive</h2>

    <div v-if="remotes.length > 0">
      <p>Remotes disponíveis — selecione um para usar:</p>
      <ul>
        <li v-for="remote in remotes" :key="remote">
          {{ remote }}
          <button @click="usarRemote(remote.replace(':', ''))">Usar</button>
        </li>
      </ul>
    </div>

    <div v-else>
      <p>Nenhum remote configurado ainda.</p>
    </div>

    <p v-if="erro" style="color: red">{{ erro }}</p>

    <hr />
    <p>Para criar um novo remote, execute no terminal:</p>
    <code>rclone config</code>
    <p>E siga o assistente para adicionar um remote do tipo <strong>Google Drive</strong>.</p>

    <button @click="router.push('/onboarding/1')">Voltar</button>
  </main>
</template>