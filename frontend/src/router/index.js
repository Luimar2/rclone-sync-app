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
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import Step1Ambiente from '../views/onboarding/Step1Ambiente.vue'
import Step2Remote from '../views/onboarding/Step2Remote.vue'
import Step3Pares from '../views/onboarding/Step3Pares.vue'
import Step4Filtros from '../views/onboarding/Step4Filtros.vue'
import Step5Agendamento from '../views/onboarding/Step5Agendamento.vue'
import Step6Confirmacao from '../views/onboarding/Step6Confirmacao.vue'
import LogsView from '../views/LogsView.vue'
import AgendamentoView from '../views/AgendamentoView.vue'
import ParesSyncView from '../views/ParesSyncView.vue'


const routes = [
  { path: '/', component: HomeView },
  { path: '/dashboard', component: DashboardView },
  { path: '/pares', component: ParesSyncView },
  { path: '/agendamento', component: AgendamentoView },
  { path: '/onboarding/1', component: Step1Ambiente },
  { path: '/onboarding/2', component: Step2Remote },
  { path: '/onboarding/3', component: Step3Pares },
  { path: '/onboarding/4', component: Step4Filtros },
  { path: '/onboarding/5', component: Step5Agendamento },
  { path: '/onboarding/6', component: Step6Confirmacao },
  { path: '/logs', component: LogsView },
]

export default createRouter({
  history: createWebHistory(),
  routes
})