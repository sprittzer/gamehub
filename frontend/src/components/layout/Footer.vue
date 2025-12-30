<template>
  <footer class="footer">
    <div class="footer-inner">

      <!-- LEFT: BRAND -->
      <div class="footer-brand">
        <RouterLink to="/" class="brand">
          <img src="@/assets/logo.svg" alt="GameHub" />
          <span>GameHub</span>
        </RouterLink>

        <p class="brand-description">
          Каталог видеоигр с отзывами игроков.
          Открывайте новые игры и делитесь впечатлениями.
        </p>
      </div>

      <!-- CENTER: NAV -->
      <nav class="footer-nav">
        <div class="nav-column">
          <h4>Разделы</h4>
          <RouterLink to="/">Главная</RouterLink>
          <RouterLink to="/games">Игры</RouterLink>
          <RouterLink to="/reviews">Отзывы</RouterLink>
        </div>

        <div class="nav-column">
          <h4>Аккаунт</h4>
          <RouterLink to="/admin">Админка</RouterLink>
        </div>
      </nav>

      <!-- RIGHT: META -->
      <div class="footer-meta">
        <p class="copyright">
          © {{ year }} GameHub
        </p>
        <p class="tech">
          Учебный проект · Vue 3 + PrimeVue
        </p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const year = new Date().getFullYear()
</script>

<style scoped>
/* ===== FOOTER ROOT ===== */
.footer {
  background-color: #0b1220;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding: 3rem 1.5rem;
  margin-top: auto;
}

/* ===== LAYOUT ===== */
.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.5fr 2fr 1fr;
  gap: 3rem;
}

/* ===== BRAND ===== */
.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 900;
  font-size: 1.25rem;
  color: white;
  text-decoration: none;
}

.brand img {
  height: 36px;
}

.brand-description {
  font-size: 0.9rem;
  color: #9ca3af;
  line-height: 1.5;
  max-width: 320px;
}

/* ===== NAV ===== */
.footer-nav {
  display: flex;
  gap: 4rem;
}

.nav-column {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-column h4 {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #e5e7eb;
  margin-bottom: 0.75rem;
}

.nav-column a {
  font-size: 0.9rem;
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.15s ease;
}

.nav-column a:hover {
  color: white;
}

/* ===== META ===== */
.footer-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  text-align: right;
}

.footer-meta p {
  font-size: 0.8rem;
  color: #9ca3af;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 900px) {
  .footer-inner {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer-meta {
    align-items: flex-start;
    text-align: left;
  }
}
</style>
