import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import Step1Ambiente from '../views/onboarding/Step1Ambiente.vue'
import Step2Remote from '../views/onboarding/Step2Remote.vue'
import Step3Pares from '../views/onboarding/Step3Pares.vue'
import Step4Filtros from '../views/onboarding/Step4Filtros.vue'
import Step5Agendamento from '../views/onboarding/Step5Agendamento.vue'
import Step6Confirmacao from '../views/onboarding/Step6Confirmacao.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/dashboard', component: DashboardView },
  { path: '/onboarding/1', component: Step1Ambiente },
  { path: '/onboarding/2', component: Step2Remote },
  { path: '/onboarding/3', component: Step3Pares },
  { path: '/onboarding/4', component: Step4Filtros },
  { path: '/onboarding/5', component: Step5Agendamento },
  { path: '/onboarding/6', component: Step6Confirmacao },
]

export default createRouter({
  history: createWebHistory(),
  routes
})