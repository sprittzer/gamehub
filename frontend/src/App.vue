<!-- src/App.vue -->
<template>
  <Layout>
    <router-view />
  </Layout>
  <Toast position="top-right" />
</template>

<script setup>
import Layout from '@/components/layout/Layout.vue'
import { RouterView } from 'vue-router'
</script>
