<template>
  <div class="game-detail-page">
    <!-- Загрузка -->
    <div v-if="loading" class="loading-container">
      <ProgressSpinner />
      <p>Загрузка информации...</p>
    </div>

    <!-- Ошибка загрузки игры -->
    <div v-else-if="error" class="error-container">
      <Message severity="error" :closable="false">{{ error }}</Message>
      <Button label="Вернуться к каталогу" class="mt-4" @click="$router.push('/games')" />
    </div>

    <!-- Контент -->
    <div v-else-if="game" class="game-content">
      <Button
        label="Назад"
        icon="pi pi-arrow-left"
        severity="secondary"
        outlined
        class="back-button"
        @click="$router.push('/games')"
      />

      <!-- Основная секция: инфо + изображение -->
      <div class="game-main">
        <div class="game-info" :style="{ background: gradientColor }">
          <h1 class="title">{{ game.title }}</h1>
          <div class="rating">
            <Rating :model-value="game.average_rating" :readonly="true" :stars="10" :cancel="false" />
            <span>{{ game.average_rating?.toFixed(1) || '0.0' }}/10</span>
            <span>({{ game.reviews_count || 0 }} отзывов)</span>
          </div>
          <div class="meta">
            <span v-if="game.release_year">📅 {{ game.release_year }}</span>
            <span v-if="game.developer">🏢 {{ game.developer }}</span>
            <span v-if="game.publisher">🏷️ {{ game.publisher }}</span>
          </div>
          <div v-if="game.genres?.length" class="genres">
            <Chip v-for="g in game.genres" :key="g" :label="g" class="genre" />
          </div>
          <div v-if="game.platforms?.length" class="platforms">
            <Tag v-for="p in game.platforms" :key="p" :value="p" severity="secondary" class="platform" />
          </div>
          <p v-if="game.description" class="description">{{ game.description }}</p>
        </div>

        <div class="game-cover">
          <img v-if="game.cover_image_path" :src="game.cover_image_path" :alt="game.title" />
          <div v-else class="cover-placeholder">
            <i class="pi pi-image"></i>
          </div>
        </div>
      </div>

      <!-- Если нет отзыва — форма на странице -->
      <Card v-if="!hasOwnReview" class="review-form-card">
        <template #title>
          <h3>Оставить отзыв</h3>
        </template>
        <template #content>
          <div class="review-form">
            <div class="form-field">
              <label>Ваша оценка</label>
              <Rating v-model="reviewForm.rating" :stars="10" :cancel="false" />
              <span v-if="reviewForm.rating">{{ reviewForm.rating }}/10</span>
            </div>
            <div class="form-field">
              <label>Ваш отзыв</label>
              <Textarea
                v-model="reviewForm.text"
                rows="5"
                placeholder="Напишите ваш отзыв о игре..."
              />
            </div>
            <Message v-if="reviewError" severity="error" :closable="true" class="mb-2">{{ reviewError }}</Message>
            <Button
              label="Отправить отзыв"
              icon="pi pi-check"
              :disabled="!canSubmitReview"
              @click="submitReview"
            />
          </div>
        </template>
      </Card>

      <!-- Список отзывов -->
      <div class="reviews-section">
        <Card>
          <template #title>
            <h3>Отзывы ({{ reviewsData.items?.length || 0 }})</h3>
          </template>
          <template #content>
            <div v-if="reviewsData.items?.length" class="reviews-list">
              <div v-for="review in reviewsData.items" :key="review.id" class="review-item">
                <div class="review-header">
                  <div class="review-info">
                    <Rating :model-value="review.rating" :readonly="true" :stars="10" :cancel="false" />
                    <span>{{ review.rating }}/10</span>
                    <span class="date">  {{ formatDate(review.created_at) }}</span>
                  </div>
                  <div v-if="review.is_own" class="actions">
                    <Button icon="pi pi-pencil" severity="warning" text @click="openEditDialog(review)" />
                    <Button icon="pi pi-trash" severity="danger" text @click="deleteReview(review.id)" />
                  </div>
                </div>
                <p class="review-text">{{ review.text }}</p>
              </div>
            </div>
            <div v-else class="empty">
              <i class="pi pi-inbox"></i>
              <p>Нет отзывов, будьте первым!</p>
            </div>
          </template>
        </Card>
      </div>

      <!-- Диалог редактирования/обновления отзыва -->
      <Dialog v-model:visible="dialogVisible" header="Редактирование отзыва" :modal="true" :closable="true" :style="{ width: '600px' }">
        <div class="review-form">
          <div class="form-field">
            <label>Ваша оценка</label>
            <Rating v-model="reviewForm.rating" :stars="10" :cancel="false" />
            <span v-if="reviewForm.rating">{{ reviewForm.rating }}/10</span>
          </div>

          <div class="form-field">
            <label>Ваш отзыв</label>
            <Textarea v-model="reviewForm.text" rows="5" placeholder="Напишите ваш отзыв о игре..." />
          </div>

          <Message v-if="reviewError" severity="error" :closable="true" class="mb-2">{{ reviewError }}</Message>

          <Button
            label="Сохранить"
            icon="pi pi-check"
            :disabled="!canSubmitReview"
            @click="submitReview"
          />
        </div>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import Card from 'primevue/card'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import Message from 'primevue/message'
import Rating from 'primevue/rating'
import Textarea from 'primevue/textarea'
import Chip from 'primevue/chip'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import { api } from '@/api'

const route = useRoute()
const game = ref(null)
const loading = ref(true)
const error = ref(null)
const reviewsData = ref({ items: [] })
const reviewForm = ref({ rating: null, text: '' })
const ownReviewId = ref(null)
const reviewError = ref('')
const dialogVisible = ref(false)

const hasOwnReview = computed(() => !!ownReviewId.value)
const canSubmitReview = computed(() => reviewForm.value.rating && reviewForm.value.text.length >= 10)

const gradientColor = `linear-gradient(to bottom, rgba(${Math.floor(Math.random()*255)},${Math.floor(Math.random()*255)},${Math.floor(Math.random()*255)},0.2), rgba(0,0,0,0.2))`

const loadGame = async () => {
  try {
    loading.value = true
    const response = await fetch(api.games.get(route.params.id))
    if (!response.ok) throw new Error('Ошибка загрузки игры')
    game.value = await response.json()
  } catch (err) {
    console.error(err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const loadReviews = async () => {
  try {
    const response = await fetch(api.reviews.gameReviews(route.params.id))
    if (!response.ok) return
    const data = await response.json()
    
    reviewsData.value = {
      ...data,
      items: data.items.map(r => ({ ...r, is_own: r.is_own || false }))
    }

    const own = reviewsData.value.items.find(r => r.is_own)
    if (own) {
      reviewForm.value.rating = own.rating
      reviewForm.value.text = own.text
      ownReviewId.value = own.id
    } else {
      reviewForm.value.rating = null
      reviewForm.value.text = ''
      ownReviewId.value = null
    }
  } catch (err) {
    console.error(err)
  }
}

const openEditDialog = (review) => {
  reviewForm.value.rating = review.rating
  reviewForm.value.text = review.text
  ownReviewId.value = review.id
  reviewError.value = ''
  dialogVisible.value = true
}

const submitReview = async () => {
  if (!canSubmitReview.value) return
  reviewError.value = ''
  try {
    const payload = { game_id: route.params.id, rating: reviewForm.value.rating, text: reviewForm.value.text }
    let response

    if (ownReviewId.value) {
      response = await fetch(api.reviews.update(ownReviewId.value), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    } else {
      response = await fetch(api.reviews.create(), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    }

    if (!response.ok) {
      const data = await response.json()
      reviewError.value = data.detail || 'Не удалось отправить отзыв'
      return
    }

    dialogVisible.value = false
    reviewForm.value.rating = null
    reviewForm.value.text = ''
    ownReviewId.value = null

    // Обновляем список отзывов и инфо об игре
    await loadReviews()
    await loadGame()
  } catch (err) {
    reviewError.value = err.message
  }
}

const deleteReview = async (id) => {
  if (!confirm('Вы уверены, что хотите удалить отзыв?')) return
  try {
    const response = await fetch(api.reviews.delete(id), { method: 'DELETE' })
    if (!response.ok) throw new Error('Не удалось удалить отзыв')

    reviewForm.value.rating = null
    reviewForm.value.text = ''
    ownReviewId.value = null
    reviewError.value = ''

    await loadReviews()
    await loadGame()
  } catch (err) {
    reviewError.value = err.message
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('ru-RU', { year:'numeric', month:'long', day:'numeric' })
}

onMounted(async () => {
  await loadGame()
  await loadReviews()
})
</script>

<style scoped>
.game-detail-page { max-width:1200px; margin:0 auto; padding:2rem; color:#f0f0f0; }
.loading-container, .error-container { text-align:center; min-height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.back-button { margin-bottom:1rem; }

.game-main { display:flex; gap:2rem; margin-bottom:3rem; }
.game-info { flex:1; padding:2rem; border-radius:12px; backdrop-filter:blur(8px); display:flex; flex-direction:column; gap:1rem; }
.title { font-size:2.5rem; font-weight:700; }
.rating { display:flex; gap:0.5rem; align-items:center; }
.meta { display:flex; gap:1rem; flex-wrap:wrap; color:#ccc; }
.genres, .platforms { display:flex; gap:0.5rem; flex-wrap:wrap; }
.description { margin-top:1rem; line-height:1.6; }

.game-cover { width:350px; border-radius:12px; overflow:hidden; display:flex; align-items:center; justify-content:center; background:#222; }
.game-cover img { width:100%; height:auto; object-fit:cover; }
.cover-placeholder { color:#666; font-size:3rem; }

.review-form-card { margin-bottom:2rem; }
.review-form { display:flex; flex-direction:column; gap:1rem; }
.form-field { display:flex; flex-direction:column; gap:0.5rem; }

.reviews-section { margin-top:2rem; }
.reviews-list { display:flex; flex-direction:column; gap:1rem; }
.review-item { background: rgba(255,255,255,0.05); padding:1rem; border-radius:8px; }
.review-header { display:flex; justify-content:space-between; align-items:center; gap:0.5rem; margin-bottom:0.5rem; }
.review-text { line-height:1.4; }
.empty { text-align:center; opacity:0.5; }
.actions Button { margin-left:0.5rem; }
.review-info {
  display: flex;
  align-items: center;
  gap: 8px; /* или 10–12px, под вкус */
}

</style>
