<template>
  <Card class="game-card" @click="onCardClick">
    <template #header>
      <div class="media">
        <img
          v-if="coverImage"
          :src="coverImage"
          :alt="game.title"
        />
        <div v-else class="placeholder">
          <i class="pi pi-image"></i>
        </div>

        <!-- OVERLAY -->
        <div class="overlay">
          <h3 class="title" :title="game.title">
            {{ game.title }}
          </h3>

          <div class="meta">
            <span v-if="game.average_rating" class="rating">
              <i class="pi pi-star-fill"></i>
              {{ game.average_rating.toFixed(1) }}
            </span>

            <span v-if="game.release_year" class="year">
              {{ game.release_year }}
            </span>
          </div>

          <div v-if="game.genres?.length" class="genres">
            <span
              v-for="genre in displayedGenres"
              :key="genre"
              class="genre"
              :title="genre"
            >
              {{ genre }}
            </span>

            <span v-if="remainingGenres > 0" class="more">
              +{{ remainingGenres }}
            </span>
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import Card from 'primevue/card'

const props = defineProps({
  game: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const coverImage = computed(() =>
  props.game.cover_image_path || props.game.cover_image || null
)

const displayedGenres = computed(() =>
  props.game.genres?.slice(0, 2) || []
)

const remainingGenres = computed(() =>
  Math.max(0, (props.game.genres?.length || 0) - 2)
)

const onCardClick = () => {
  router.push(`/games/${props.game.id}`)
}
</script>

<style scoped>
/* ===== CARD ===== */
.game-card {
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: #0f172a;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.game-card:hover {
  transform: scale(1.03);
  border-color: #3b82f6;
  box-shadow: 0 12px 30px rgba(59, 130, 246, 0.25);
}

/* ===== MEDIA ===== */
.media {
  position: relative;
  height: 320px;
  width: 100%;
  overflow: hidden;
}

.media img,
.placeholder {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: filter 0.25s ease, transform 0.25s ease;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e293b;
  color: rgba(255, 255, 255, 0.4);
  font-size: 3rem;
}

/* ===== OVERLAY ===== */
.overlay {
  position: absolute;
  inset: 0;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.5rem;
  background: linear-gradient(
    to top,
    rgba(2, 6, 23, 0.85),
    rgba(2, 6, 23, 0.4),
    transparent
  );
  opacity: 0;
  transition: opacity 0.25s ease;
}

.game-card:hover .overlay {
  opacity: 1;
}

.game-card:hover img {
  filter: brightness(0.6);
  transform: scale(1.05);
}

/* ===== TEXT ===== */
.title {
  font-size: 1rem;
  font-weight: 700;
  color: white;
  line-height: 1.3;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: #e5e7eb;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #facc15;
}

.genres {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.genre,
.more {
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  color: #e5e7eb;
  white-space: nowrap;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ===== PRIME CARD RESET ===== */
:deep(.p-card-body),
:deep(.p-card-content) {
  padding: 0;
}
</style>
