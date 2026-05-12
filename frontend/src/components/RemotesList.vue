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