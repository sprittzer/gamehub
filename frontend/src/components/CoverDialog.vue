<template>
  <Dialog
    :visible="visible"
    modal
    :style="{ width:'400px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <template #header>
      <span>Загрузить обложку: {{ game?.title }}</span>
    </template>

    <div class="dialog-body">
      <input type="file" accept="image/*" @change="onFileSelected" />
      <img v-if="preview" :src="preview" class="cover-preview" />
    </div>

    <template #footer>
      <Button label="Закрыть" text @click="$emit('update:visible', false)" />
      <Button label="Загрузить" :disabled="!selectedFile" @click="uploadCover" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import { api } from '@/api'
import { useToast } from 'primevue/usetoast'

const toast = useToast()


const props = defineProps({ visible:Boolean, game:Object })
const emit = defineEmits(['update:visible','saved'])

const selectedFile = ref(null)
const preview = ref(null)

watch(() => props.game, g => {
  preview.value = g?.cover_image_path || null
  selectedFile.value = null
})

const onFileSelected = (event) => {
  const file = event.target.files[0]
  if (!file) return
  selectedFile.value = file
  preview.value = URL.createObjectURL(file)
}

const uploadCover = async () => {
  if (!selectedFile.value || !props.game) {
    toast.add({ severity: 'warn', summary: 'Внимание', detail: 'Файл не выбран', life: 3000 })
    return
  }

  const formData = new FormData()
  formData.append('cover_image', selectedFile.value)

  try {
    const res = await fetch(api.games.cover(props.game.id), { method: 'PATCH', body: formData })
    if (!res.ok) {
      const text = await res.text()
      toast.add({ severity: 'error', summary: 'Ошибка', detail: `Не удалось загрузить обложку: ${text}`, life: 4000 })
      console.error('Ошибка загрузки обложки', text)
      return
    }

    const data = await res.json()
    toast.add({ severity: 'success', summary: 'Успех', detail: 'Обложка успешно загружена', life: 3000 })
    emit('saved', { ...props.game, cover_image_path: data.cover_image_path })
    emit('update:visible', false)
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Ошибка', detail: err.message, life: 4000 })
    console.error(err)
  }
}

</script>

<style scoped>
.cover-preview { max-width:100%; max-height:200px; margin-top:1rem; border-radius:6px; }
.dialog-body { display:flex; flex-direction:column; align-items:center; gap:0.5rem; padding:1rem 0; }
</style>
