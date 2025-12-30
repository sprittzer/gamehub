<!-- src/App.vue -->
<template>
  <AppLayout>
    <router-view />
  </AppLayout>
  <AppToast position="top-right" />
</template>

<script setup>
import AppLayout from '@/components/layout/AppLayout.vue';
import { RouterView } from 'vue-router';
</script>
