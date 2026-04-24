<script setup>
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'

const router = useRouter()
const store = useConfigStore()
</script>

<template>
  <main>
    <h2>Passo 4 — Filtros de exclusão</h2>

    <h3>Exclusões comuns</h3>

    <label>
      <input type="checkbox" v-model="store.filtros.arquivos_temporarios" />
      Arquivos temporários (*.tmp, *.temp)
    </label><br />

    <label>
      <input type="checkbox" v-model="store.filtros.lixeira" />
      Lixeira (.Trash)
    </label><br />

    <label>
      <input type="checkbox" v-model="store.filtros.cache" />
      Cache (**/cache/**)
    </label><br />

    <label>
      <input type="checkbox" v-model="store.filtros.git" />
      Repositórios Git (.git/**)
    </label><br />

    <label>
      <input type="checkbox" v-model="store.filtros.arquivos_ocultos" />
      Arquivos ocultos (.*)
    </label>

    <h3>Filtros avançados</h3>
    <p>Um filtro por linha, no formato do rclone:</p>
    <textarea
      v-model="store.filtros.avancado"
      placeholder="- *.log&#10;- **/node_modules/**"
      rows="5"
    />

    <div>
      <button @click="router.push('/onboarding/3')">Voltar</button>
      <button @click="router.push('/onboarding/5')">Próximo</button>
    </div>
  </main>
</template>