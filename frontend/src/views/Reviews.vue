<template>
  <div class="reviews-page">
    <h1 class="page-title">Мои отзывы</h1>

    <div v-if="loading" class="loading">
      <ProgressSpinner />
    </div>

    <div v-else>
      <div v-if="reviews.length">
        <div v-for="review in reviews" :key="review.id" class="review-card">
          <!-- Игра -->
          <div class="game-info" @click="goToGame(review.game_id)">
            <img :src="review.game?.cover_image_path || placeholderImage" alt="Game Image" class="game-image" />
            <span class="game-title" :title="review.game?.title">{{ review.game?.title || 'Игра не найдена' }}</span>
          </div>

          <!-- Отзыв -->
          <div class="review-content">
            <div class="review-rating">
              <i v-for="n in Math.round(review.rating)" :key="n" class="pi pi-star-fill"></i>
            </div>
            <p>{{ review.text }}</p>
            <span class="review-date">{{ formatDate(review.created_at) }}</span>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <Message severity="info" :closable="false">
          У вас пока нет отзывов
        </Message>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Message from 'primevue/message'
import ProgressSpinner from 'primevue/progressspinner'
import { api } from '@/api'

const router = useRouter()
const reviews = ref([])
const loading = ref(false)
const placeholderImage = '/images/game-placeholder.png'

const loadReviews = async () => {
  loading.value = true
  try {
    const res = await fetch(api.reviews.myReviews())
    if (!res.ok) throw new Error('Ошибка загрузки')
    const data = await res.json()
    const items = data.items || []

    // Подгружаем игры
    const reviewsWithGames = await Promise.all(
      items.map(async (r) => {
        try {
          const gameRes = await fetch(api.games.get(r.game_id))
          r.game = gameRes.ok ? await gameRes.json() : null
        } catch {
          r.game = null
        }
        return r
      })
    )
    reviews.value = reviewsWithGames
  } catch (err) {
    console.error(err)
    reviews.value = []
  } finally {
    loading.value = false
  }
}

const goToGame = (gameId) => {
  if (gameId) router.push(`/games/${gameId}`)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString()
}

onMounted(loadReviews)
</script>

<style scoped>
.reviews-page {
  padding: 2rem;
}

.page-title {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: white;
}

.loading {
  display: flex;
  justify-content: center;
  margin: 4rem 0;
}

.review-card {
  display: flex;
  gap: 1rem;
  background: rgba(0,0,0,0.6);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.game-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
  cursor: pointer;
}

.game-info:hover .game-title {
  text-decoration: underline;
}

.game-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.game-title {
  font-weight: 600;
  color: #4f46e5;
  text-align: center;
  max-width: 100px;       /* ограничение по ширине картинки */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* многоточие если длинное название */
}

.review-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.review-rating i {
  color: #facc15;
  margin-right: 0.1rem;
}

.review-date {
  font-size: 0.8rem;
  color: #9ca3af;
}
</style>
