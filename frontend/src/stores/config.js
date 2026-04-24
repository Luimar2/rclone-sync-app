import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useConfigStore = defineStore('config', () => {
  const remoteName = ref('')
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

  return { remoteName, pares, filtros, agendamento, resetar }
})