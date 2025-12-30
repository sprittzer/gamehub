<template>
  <header class="menubar">
    <!-- LEFT: LOGO -->
    <div class="menubar-left">
      <RouterLink to="/" class="logo">
        <img src="@/assets/logo.svg" alt="GameHub" />
        <span>GAMEHUB</span>
      </RouterLink>
    </div>

    <!-- CENTER: MENU -->
    <nav class="menubar-center">
      <RouterLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="menu-item"
        :class="{ active: isActive(item.to) }"
      >
        <i :class="item.icon"></i>
        <span>{{ item.label }}</span>
        <div class="indicator" />
      </RouterLink>
    </nav>

    <!-- RIGHT: ADMIN -->
    <div class="menubar-right">
      <Button
        label="Админ"
        severity="info"
        size="small"
        class="admin-btn"
        @click="onAdmin"
      />
    </div>
  </header>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import Button from 'primevue/button'

const route = useRoute()
const router = useRouter()

const items = [
  { label: 'Игры', icon: 'pi pi-list', to: '/games' },
  { label: 'Отзывы', icon: 'pi pi-comments', to: '/reviews' }
]

const isActive = (path) => route.path.startsWith(path)

const onAdmin = () => {
  router.push('/admin')
}
</script>

<style scoped>
/* ===== ROOT ===== */
.menubar {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: #0b1220;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

/* ===== LOGO ===== */
.menubar-left {
  min-width: 180px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: white;
  font-weight: 900;
  font-size: 1.25rem;
  text-decoration: none;
}

.logo img {
  height: 36px;
}

/* ===== MENU ===== */
.menubar-center {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.menu-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  color: #9ca3af;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s ease;
}

.menu-item:hover {
  color: #ffffff;
}

/* underline indicator */
.menu-item .indicator {
  position: absolute;
  bottom: -6px;
  left: 50%;
  width: 0;
  height: 2px;
  background: #2295ec;
  border-radius: 2px;
  transform: translateX(-50%);
  transition: width 0.25s ease;
}

.menu-item.active {
  color: #ffffff;
}

.menu-item.active .indicator {
  width: 100%;
}

/* ===== ADMIN ===== */
.menubar-right {
  min-width: 180px;
  display: flex;
  justify-content: flex-end;
}

.admin-btn {
  background: #2295ec;
  border: none;
}
</style>
