// RcloneSync - Interface gráfica para rclone com Google Drive no Linux
// Copyright (C) 2026 Luimar2
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useConfigStore = defineStore('config', () => {
  const remoteName = ref('')
  const provider   = ref('gdrive')   // provider selecionado no Step2
  const pares = ref([])
  const filtros = ref({
    arquivos_temporarios: true,
    lixeira: true,
    cache: true,
    git: true,
    arquivos_ocultos: false,
    avancado: ''
  })
  const agendamento = ref({
    intervalo: 'daily',
    horario_customizado: ''
  })

  function resetar() {
    remoteName.value = ''
    provider.value   = 'gdrive'
    pares.value = []
    filtros.value = {
      arquivos_temporarios: true,
      lixeira: true,
      cache: true,
      git: true,
      arquivos_ocultos: false,
      avancado: ''
    }
    agendamento.value = { intervalo: 'daily', horario_customizado: '' }
  }

  return { remoteName, provider, pares, filtros, agendamento, resetar }
})