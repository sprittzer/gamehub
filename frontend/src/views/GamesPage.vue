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

      <div class="filters-row compact-filters">
        <MultiSelect
          v-model="selectedGenres"
          :options="availableGenres"
          placeholder="Жанры"
          display="chip"
          class="filter-item"
        />
        <MultiSelect
          v-model="selectedPlatforms"
          :options="availablePlatforms"
          placeholder="Платформы"
          display="chip"
          class="filter-item"
        />
        <div class="filter-item slider-wrapper">
          <label class="slider-label">Год: {{ yearRange[0] }} - {{ yearRange[1] }}</label>
          <Slider v-model="yearRange" range :min="1980" :max="2030" />
        </div>
        <div class="filter-item slider-wrapper">
          <label class="slider-label"
            >Рейтинг: {{ ratingRange[0].toFixed(1) }} - {{ ratingRange[1].toFixed(1) }}</label
          >
          <Slider v-model="ratingRange" range :min="0" :max="10" :step="0.1" />
        </div>
        <InputText
          v-model="filters.developer"
          placeholder="Разработчик"
          class="filter-item developer-input"
        />
        <div class="filter-item buttons-group">
          <Button label="Применить" icon="pi pi-check" severity="secondary" @click="applyFilters" />
          <Button
            label="Сбросить"
            icon="pi pi-refresh"
            outlined
            class="ml-2"
            @click="resetFilters"
          />
        </div>
      </div>
    </div>

    <div class="games-section">
      <ProgressSpinner v-if="loading" class="loading-spinner" />

      <div v-else-if="games.length" class="games-grid">
        <GameCard v-for="game in games" :key="game.id" :game="game" />
      </div>

      <div v-else class="empty-state">
        <i class="pi pi-inbox empty-icon"></i>
        <h3>Игры не найдены</h3>
      </div>
    </div>

    <Paginator
      v-if="totalPages > 1"
      :rows="pageSize"
      :total-records="totalGames"
      :first="(currentPage - 1) * pageSize"
      @page="onPageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import InputText from 'primevue/inputtext';
import MultiSelect from 'primevue/multiselect';
import Slider from 'primevue/slider';
import Button from 'primevue/button';
import Paginator from 'primevue/paginator';
import ProgressSpinner from 'primevue/progressspinner';
import GameCard from '@/components/GameCard.vue';
import { api } from '@/api';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const games = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = 20;
const totalGames = ref(0);
const totalPages = ref(0);

const filters = ref({
  q: '',
  genres: null,
  platforms: null,
  developer: '',
  min_year: null,
  max_year: null,
  min_rating: null,
  max_rating: null,
});

const selectedGenres = ref([]);
const selectedPlatforms = ref([]);
const availableGenres = ref([]);
const availablePlatforms = ref([]);

const yearRange = ref([1990, 2030]);
const ratingRange = ref([0, 10]);

// --- Загрузка жанров и платформ ---
const loadGenresAndPlatforms = async () => {
  try {
    const [g, p] = await Promise.all([fetch(api.games.genres()), fetch(api.games.platforms())]);
    if (g.ok) availableGenres.value = await g.json();
    if (p.ok) availablePlatforms.value = await p.json();
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: err.message, life: 4000 });
  }
};

// --- Загрузка игр ---
const loadGames = async (applyFilter = false) => {
  loading.value = true;
  try {
    const params = new URLSearchParams();

    params.append('page', currentPage.value);
    params.append('page_size', pageSize);

    if (applyFilter) {
      if (filters.value.q) params.append('q', filters.value.q);
      if (filters.value.genres) params.append('genres', filters.value.genres);
      if (filters.value.platforms) params.append('platforms', filters.value.platforms);
      if (filters.value.developer) params.append('developer', filters.value.developer);
      if (filters.value.min_year !== null) params.append('min_year', filters.value.min_year);
      if (filters.value.max_year !== null) params.append('max_year', filters.value.max_year);
      if (filters.value.min_rating !== null) params.append('min_rating', filters.value.min_rating);
      if (filters.value.max_rating !== null) params.append('max_rating', filters.value.max_rating);
    }

    const url = `${api.games.list()}?${params.toString()}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error('Ошибка API при загрузке игр');
    const data = await res.json();
    games.value = data.items || [];
    totalGames.value = data.total || 0;
    totalPages.value = data.pages || Math.ceil(totalGames.value / pageSize);
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: err.message, life: 4000 });
    games.value = [];
    totalGames.value = 0;
    totalPages.value = 0;
  } finally {
    loading.value = false;
  }
};

// --- Реактивный поиск ---
watch(
  () => filters.value.q,
  () => {
    currentPage.value = 1;
    loadGames(true);
  },
);

// --- Применение фильтров ---
const applyFilters = () => {
  filters.value.genres = selectedGenres.value.length ? selectedGenres.value.join(',') : null;
  filters.value.platforms = selectedPlatforms.value.length
    ? selectedPlatforms.value.join(',')
    : null;
  filters.value.min_year = yearRange.value[0];
  filters.value.max_year = yearRange.value[1];
  filters.value.min_rating = ratingRange.value[0];
  filters.value.max_rating = ratingRange.value[1];
  currentPage.value = 1;
  loadGames(true);
};

// --- Сброс фильтров ---
const resetFilters = () => {
  filters.value = {
    q: '',
    genres: null,
    platforms: null,
    developer: '',
    min_year: null,
    max_year: null,
    min_rating: null,
    max_rating: null,
  };
  selectedGenres.value = [];
  selectedPlatforms.value = [];
  yearRange.value = [1990, 2030];
  ratingRange.value = [0, 10];
  currentPage.value = 1;
  loadGames(true);
};

// --- Пагинация ---
const onPageChange = (e) => {
  currentPage.value = e.page + 1;
  loadGames(true);
};

onMounted(async () => {
  await loadGenresAndPlatforms();
  await loadGames(false);
});
</script>

<style scoped>
.games-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  color: white;
}
.games-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}
.games-title {
  font-size: 2rem;
  font-weight: 700;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}
.games-count {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2295ec;
}
.filters-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
}
.full-width {
  flex: 1 1 100%;
}
.compact-filters .filter-item {
  min-width: 150px;
  flex: 1 1 auto;
}
.slider-wrapper {
  flex: 1 1 200px;
  display: flex;
  flex-direction: column;
}
.slider-label {
  font-size: 0.85rem;
  margin-bottom: 0.2rem;
  color: #ccc;
}
.developer-input {
  flex: 1 1 150px;
}
.buttons-group {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}
.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 2rem;
}
.empty-state {
  text-align: center;
  padding: 4rem;
  color: #9ca3af;
}
.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
.loading-spinner {
  display: flex;
  justify-content: center;
  margin: 4rem 0;
}
</style>
