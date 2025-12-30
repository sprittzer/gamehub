<!-- src/components/layout/Layout.vue -->
<template>
  <div class="layout">
    <Header />

    <main class="main">
      <slot />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Header from './Header.vue'
import Footer from './Footer.vue'
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  width: 100%;
}
</style>
