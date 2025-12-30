<template>
  <div class="admin-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1 class="page-title">Админ-панель</h1>
      <p class="page-subtitle">Управление контентом</p>
    </div>

    <!-- Табсы -->
    <TabView v-model:active-index="activeTab">
      <!-- Games Tab -->
      <TabPanel header="Игры">
        <div class="admin-actions mb-3">
          <Button
            label="Добавить игру"
            icon="pi pi-plus"
            class="add-button"
            @click="openCreateGameDialog"
          />
        </div>

        <DataTable
          :value="games"
          :loading="loading"
          :paginator="true"
          :rows="20"
          :total-records="totalGames"
          :lazy="true"
          data-key="id"
          show-gridlines
          @page="onGamePage"
        >
          <Column field="id" header="ID" style="width:70px" />

          <!-- Cover + загрузка -->
          <Column header="Обложка" style="width:120px">
            <template #body="{ data }">
              <div class="cover-cell">
                <img
                  v-if="data.cover_image_path"
                  :src="data.cover_image_path"
                  class="cover-thumb"
                />
                <Button
                  icon="pi pi-upload"
                  text
                  size="small"
                  title="Загрузить обложку"
                  @click="openCoverDialog(data)"
                />
              </div>
            </template>
          </Column>

          <Column field="title" header="Название" />
          <Column field="description" header="Описание">
            <template #body="{ data }">
              <div class="description-cell" :title="data.description">{{ data.description }}</div>
            </template>
          </Column>

          <Column header="Жанры">
            <template #body="{ data }">{{ data.genres.join(', ') }}</template>
          </Column>
          <Column field="developer" header="Разработчик" />
          <Column field="publisher" header="Издатель" />
          <Column field="release_year" header="Год" style="width:90px" />
          <Column header="Платформы">
            <template #body="{ data }">{{ data.platforms.join(', ') }}</template>
          </Column>
          <Column header="Рейтинг" style="width:90px">
            <template #body="{ data }">{{ data.average_rating?.toFixed(1) ?? '—' }}</template>
          </Column>

          <Column header="Действия" style="width:140px">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" rounded text @click="editGame(data)" />
              <Button icon="pi pi-trash" rounded text severity="danger" @click="confirmDeleteGame(data)" />
            </template>
          </Column>
        </DataTable>
      </TabPanel>

      <!-- Reviews Tab -->
      <TabPanel header="Отзывы">
        <DataTable
          :value="reviews"
          :loading="loading"
          :paginator="true"
          :rows="20"
          :total-records="totalReviews"
          :lazy="true"
          data-key="id"
          show-gridlines
          @page="onReviewPage"
        >
          <Column field="id" header="ID" style="width:70px" />
          <Column header="Игра" style="width:150px">
            <template #body="{ data }">
              <img v-if="data.game?.cover_image_path" :src="data.game.cover_image_path" class="cover-thumb mr-2" />
              <span>{{ data.game?.title || 'Игра не найдена' }}</span>
            </template>
          </Column>
          <Column field="rating" header="Рейтинг" style="width:100px" />
          <Column field="text" header="Текст" />
          <Column field="created_at" header="Дата" style="width:120px" />
          <Column header="Действия" style="width:140px">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" rounded text @click="editReview(data)" />
              <Button icon="pi pi-trash" rounded text severity="danger" @click="confirmDeleteReview(data)" />
            </template>
          </Column>
        </DataTable>
      </TabPanel>
    </TabView>

    <!-- Диалоги -->
    <GameDialog
      :visible="gameDialogVisible"
      :game="editingGame"
      @update:visible="gameDialogVisible = $event"
      @save="handleGameSaved"
    />
    <CoverDialog
      :visible="coverDialogVisible"
      :game="editingGameCover"
      @update:visible="coverDialogVisible = $event"
      @saved="handleCoverSaved"
    />
    <ReviewDialog
      :visible="reviewDialogVisible"
      :review="editingReview"
      @update:visible="reviewDialogVisible = $event"
      @save="handleReviewSaved"
    />
    <ConfirmDialog
      v-model:visible="deleteDialogVisible"
      @confirm="deleteItem"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import GameDialog from '../components/GameDialog.vue'
import CoverDialog from '../components/CoverDialog.vue'
import ReviewDialog from '../components/ReviewDialog.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import { api } from '@/api'

const activeTab = ref(0)
const loading = ref(false)

const games = ref([])
const totalGames = ref(0)
const editingGame = ref(null)

const reviews = ref([])
const totalReviews = ref(0)
const editingReview = ref(null)

const gameDialogVisible = ref(false)
const reviewDialogVisible = ref(false)
const coverDialogVisible = ref(false)
const editingGameCover = ref(null)
const deleteDialogVisible = ref(false)
const itemToDelete = ref(null)
const deleteType = ref('')

// --- LOAD ---
const loadGames = async (page = 1) => {
  loading.value = true
  try {
    const res = await fetch(api.games.list(page, 20))
    const data = await res.json()
    games.value = data.items || []
    totalGames.value = data.total || games.value.length
  } finally { loading.value = false }
}

const loadReviews = async (page = 1) => {
  loading.value = true
  try {
    const res = await fetch(api.reviews.list(page, 20))
    const data = await res.json()
    const withGames = await Promise.all(
      (data.items || []).map(async r => {
        try {
          const gRes = await fetch(api.games.get(r.game_id))
          r.game = gRes.ok ? await gRes.json() : null
        } catch { r.game = null }
        return r
      })
    )
    reviews.value = withGames
    totalReviews.value = data.total || withGames.length
  } finally { loading.value = false }
}

// --- Pagination ---
const onGamePage = e => loadGames(e.page + 1)
const onReviewPage = e => loadReviews(e.page + 1)

// --- CRUD ---
const openCreateGameDialog = () => { editingGame.value = null; gameDialogVisible.value = true }
const editGame = g => { editingGame.value = { ...g }; gameDialogVisible.value = true }
const editReview = r => { editingReview.value = { ...r }; reviewDialogVisible.value = true }

const openCoverDialog = g => { editingGameCover.value = g; coverDialogVisible.value = true }

const confirmDeleteGame = g => { itemToDelete.value = g; deleteType.value='game'; deleteDialogVisible.value=true }
const confirmDeleteReview = r => { itemToDelete.value = r; deleteType.value='review'; deleteDialogVisible.value=true }

const deleteItem = async () => {
  if (!itemToDelete.value) return
  if (deleteType.value === 'game') {
    await fetch(api.games.delete(itemToDelete.value.id), { method:'DELETE' })
    games.value = games.value.filter(g => g.id !== itemToDelete.value.id)
    totalGames.value--
  } else {
    await fetch(api.reviews.delete(itemToDelete.value.id), { method:'DELETE' })
    reviews.value = reviews.value.filter(r => r.id !== itemToDelete.value.id)
    totalReviews.value--
  }
  deleteDialogVisible.value = false
  itemToDelete.value = null
}

// --- Callbacks ---
const handleGameSaved = updated => {
  gameDialogVisible.value = false
  const idx = games.value.findIndex(g => g.id === updated.id)
  if (idx !== -1) games.value[idx] = updated
  else { games.value.unshift(updated); totalGames.value++ }
  games.value = [...games.value]
}

const handleCoverSaved = updated => {
  coverDialogVisible.value = false
  const idx = games.value.findIndex(g => g.id === updated.id)
  if (idx !== -1) {
    Object.assign(games.value[idx], updated)
  }
}


const handleReviewSaved = updated => {
  reviewDialogVisible.value = false
  const idx = reviews.value.findIndex(r => r.id === updated.id)
  if (idx !== -1) reviews.value[idx] = updated
  else { reviews.value.unshift(updated); totalReviews.value++ }
  reviews.value = [...reviews.value]
}

onMounted(() => { loadGames(); loadReviews() })
</script>

<style scoped>
.admin-page { max-width:1600px; margin:0 auto; padding:2rem; }
.page-title { font-size:2.2rem; color:white; margin-bottom:0.5rem; display:flex; align-items:center; }
.page-subtitle { color:#9ca3af; margin-bottom:1rem; }
.cover-thumb { max-height:80px; border-radius:4px; object-fit:cover; }
.cover-cell { display:flex; flex-direction:column; align-items:center; gap:0.3rem; }
.add-button { background: #2295EC; border:none; }

.description-cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

</style>
