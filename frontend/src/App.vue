<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from './layouts/DefaultLayout.vue'

const route = useRoute()
const usarLayout = computed(() =>
  !route.path.startsWith('/onboarding') && route.path !== '/'
)
</script>

<template>
  <DefaultLayout v-if="usarLayout">
    <RouterView />
  </DefaultLayout>
  <RouterView v-else />
</template>