<template>
  <Dialog
    :visible="visible"
    modal
    :style="{ width: '520px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <template #header>
      <span>{{ localGame.id ? 'Редактировать игру' : 'Добавить игру' }}</span>
    </template>

    <div class="dialog-body">
      <FloatLabel variant="on">
        <InputText v-model="localGame.title" />
        <label>Название</label>
      </FloatLabel>

      <FloatLabel variant="on">
        <Textarea v-model="localGame.description" auto-resize rows="3" />
        <label>Описание</label>
      </FloatLabel>

      <FloatLabel variant="on">
        <InputNumber
          v-model="localGame.release_year"
          :use-grouping="false"
          :min="1970"
          :max="new Date().getFullYear() + 5"
        />
        <label>Год выпуска</label>
      </FloatLabel>

      <FloatLabel variant="on">
        <InputText v-model="localGame.developer" />
        <label>Разработчик</label>
      </FloatLabel>

      <FloatLabel variant="on">
        <InputText v-model="localGame.publisher" />
        <label>Издатель</label>
      </FloatLabel>

      <!-- ЖАНРЫ -->
      <div class="multi-section">
        <label>Жанры</label>
        <MultiSelect
          v-model="localGame.genres"
          :options="allGenres"
          placeholder="Выберите жанры"
          :show-clear="true"
        />
        <div class="add-new">
          <InputText v-model="newGenre" placeholder="Новый жанр" @keyup.enter="addGenre" />
          <Button icon="pi pi-plus" @click="addGenre" />
        </div>
      </div>

      <!-- ПЛАТФОРМЫ -->
      <div class="multi-section">
        <label>Платформы</label>
        <MultiSelect
          v-model="localGame.platforms"
          :options="allPlatforms"
          placeholder="Выберите платформы"
          :show-clear="true"
        />
        <div class="add-new">
          <InputText v-model="newPlatform" placeholder="Новая платформа" @keyup.enter="addPlatform" />
          <Button icon="pi pi-plus" @click="addPlatform" />
        </div>
      </div>
    </div>

    <template #footer>
      <Button label="Отмена" text @click="$emit('update:visible', false)" />
      <Button label="Сохранить" icon="pi pi-check" @click="saveGame" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import FloatLabel from 'primevue/floatlabel'
import Button from 'primevue/button'
import MultiSelect from 'primevue/multiselect'
import { useToast } from 'primevue/usetoast'
import { api } from '@/api'

const toast = useToast()

const props = defineProps({
  visible: Boolean,
  game: Object
})

const emit = defineEmits(['update:visible', 'save'])

const localGame = ref({
  title: '',
  description: '',
  release_year: new Date().getFullYear(),
  developer: '',
  publisher: '',
  genres: [],
  platforms: []
})

const allGenres = ref([])
const allPlatforms = ref([])
const newGenre = ref('')
const newPlatform = ref('')

watch(() => props.game, g => {
  if (g) {
    localGame.value = {
      ...g,
      genres: [...(g.genres || [])],
      platforms: [...(g.platforms || [])]
    }
  } else {
    localGame.value = {
      title: '',
      description: '',
      release_year: new Date().getFullYear(),
      developer: '',
      publisher: '',
      genres: [],
      platforms: []
    }
  }
})

onMounted(async () => {
  const g = await fetch(api.games.genres()).then(r => r.json())
  const p = await fetch(api.games.platforms()).then(r => r.json())
  allGenres.value = g
  allPlatforms.value = p
})

const addGenre = () => {
  const v = newGenre.value.trim()
  if (!v) return
  if (!allGenres.value.includes(v)) allGenres.value.push(v)
  if (!localGame.value.genres.includes(v)) localGame.value.genres.push(v)
  newGenre.value = ''
}

const addPlatform = () => {
  const v = newPlatform.value.trim()
  if (!v) return
  if (!allPlatforms.value.includes(v)) allPlatforms.value.push(v)
  if (!localGame.value.platforms.includes(v)) localGame.value.platforms.push(v)
  newPlatform.value = ''
}

const saveGame = async () => {
  if (!localGame.value.title.trim()) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Название обязательно', life: 3000 })
    return
  }

  const method = localGame.value.id ? 'PATCH' : 'POST'
  const url = localGame.value.id
    ? api.games.update(localGame.value.id)
    : api.games.create()

  const res = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(localGame.value)
  })

  if (!res.ok) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Ошибка сохранения', life: 4000 })
    return
  }

  emit('save', await res.json())
  emit('update:visible', false)
  toast.add({ severity: 'success', summary: 'Готово', detail: 'Игра сохранена', life: 3000 })
}
</script>

<style scoped>
.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.multi-section {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.add-new {
  display: flex;
  gap: 0.4rem;
}
</style>
