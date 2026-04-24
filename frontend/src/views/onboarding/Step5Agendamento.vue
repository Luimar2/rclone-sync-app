<script setup>
import { useRouter } from 'vue-router'
import { useConfigStore } from '../../stores/config'
import api from '../../services/api'
import { ref } from 'vue'

const router = useRouter()
const store = useConfigStore()
const erro = ref('')
const carregando = ref(false)

const opcoes = [
  { valor: '1h',    label: 'A cada 1 hora' },
  { valor: '6h',    label: 'A cada 6 horas' },
  { valor: '12h',   label: 'A cada 12 horas' },
  { valor: 'daily', label: 'Uma vez ao dia' },
  { valor: 'custom', label: 'Horário customizado' },
]

async function instalarTimer() {
  carregando.value = true
  try {
    await api.post('/agendamento/instalar', {
      intervalo: store.agendamento.intervalo,
      horario_customizado: store.agendamento.horario_customizado
    })
    router.push('/onboarding/6')
  } catch (e) {
    erro.value = 'Erro ao instalar o agendamento.'
  } finally {
    carregando.value = false
  }
}
</script>

<template>
  <main>
    <h2>Passo 5 — Agendamento</h2>

    <div v-for="opcao in opcoes" :key="opcao.valor">
      <label>
        <input
          type="radio"
          :value="opcao.valor"
          v-model="store.agendamento.intervalo"
        />
        {{ opcao.label }}
      </label>
    </div>

    <div v-if="store.agendamento.intervalo === 'custom'">
      <label>Horário (formato systemd, ex: *-*-* 02:00:00)</label>
      <input v-model="store.agendamento.horario_customizado" />
    </div>

    <p v-if="erro" style="color: red">{{ erro }}</p>

    <div>
      <button @click="router.push('/onboarding/4')">Voltar</button>
      <button :disabled="carregando" @click="instalarTimer">
        {{ carregando ? 'Instalando...' : 'Instalar agendamento' }}
      </button>
    </div>
  </main>
</template>