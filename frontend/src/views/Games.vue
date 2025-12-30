<template>
  <div class="games-page">
    <div class="games-header">
      <h1 class="games-title">
        Игры
        <span class="games-count">{{ totalGames }}</span>
      </h1>

      <div class="filters-row">
        <InputText
          v-model="filters.q"
          placeholder="Поиск по названию игры..."
          class="search-input full-width"
        />
      </div>
    </div>

    <div class="games-section">
      <div class="games-grid">
        <GameCard v-for="game in filteredGames" :key="game.id" :game="game" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import InputText from 'primevue/inputtext'
import GameCard from '@/components/GameCard.vue'

const games = ref([
  { id: 1, title: 'Elden Ring', year: 2022, rating: 9.4, cover: 'https://avatars.mds.yandex.net/i?id=71e4ddcde3970ca1219c241e367172ac54e1ebf2-4055744-images-thumbs&n=13' },
  { id: 2, title: 'Hollow Knight', year: 2017, rating: 9.0, cover: 'https://avatars.mds.yandex.net/i?id=74175e561c4f57206b0afc800e7eeb2b4d12c181-12473016-images-thumbs&n=13' },
  { id: 3, title: 'Stardew Valley', year: 2016, rating: 8.7, cover: 'https://avatars.mds.yandex.net/i?id=663cfb16538e88b74840b9d988a349b95ee0c1af-4949878-images-thumbs&n=13' }
])

const filters = ref({ q: '' })

const filteredGames = computed(() => {
  if (!filters.value.q) return games.value
  return games.value.filter(game =>
    game.title.toLowerCase().includes(filters.value.q.toLowerCase())
  )
})

const totalGames = computed(() => filteredGames.value.length)

watch(() => filters.value.q, () => {})
</script>

<style scoped>
.games-page { max-width: 1400px; margin: 0 auto; padding: 2rem; color: white; }
.games-header { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem; }
.games-title { font-size: 2rem; font-weight: 700; display: flex; align-items: baseline; gap: 0.5rem; }
.games-count { font-size: 1.5rem; font-weight: 700; color: #2295ec; }
.filters-row { display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; margin-bottom: 0.5rem; }
.full-width { flex: 1 1 100%; }
.games-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px,1fr)); gap: 2rem; }
</style>
