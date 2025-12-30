<template>
  <Dialog
    :visible="visible"
    modal
    :style="{ width: '500px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <template #header>
      <span>{{ review?.id ? 'Редактировать отзыв' : 'Добавить отзыв' }}</span>
    </template>

    <div class="dialog-body">
      <FloatLabel variant="on">
        <InputText id="rating" v-model="localReview.rating" class="rounded-input" type="number" />
        <label for="rating">Рейтинг</label>
      </FloatLabel>

      <FloatLabel variant="on">
        <InputText id="text" v-model="localReview.text" class="rounded-input" />
        <label for="text">Текст</label>
      </FloatLabel>
    </div>

    <template #footer>
      <Button label="Отмена" text @click="$emit('update:visible', false)" />
      <Button label="Сохранить" icon="pi pi-check" @click="saveReview" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import FloatLabel from 'primevue/floatlabel';
import Button from 'primevue/button';
import { api } from '@/api';

const props = defineProps({ visible: Boolean, review: Object });
const emit = defineEmits(['update:visible', 'save']);
const localReview = ref({ rating: 0, text: '' });

watch(
  () => props.review,
  (r) => {
    if (r) localReview.value = { ...r };
    else localReview.value = { rating: 0, text: '' };
  },
);

const saveReview = async () => {
  let res;
  if (localReview.value.id) {
    res = await fetch(api.reviews.update(localReview.value.id), {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(localReview.value),
    });
  } else {
    res = await fetch(api.reviews.create(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(localReview.value),
    });
  }
  const saved = await res.json();
  emit('save', saved);
  emit('update:visible', false);
};
</script>

<style scoped>
.dialog-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.rounded-input {
  border-radius: 6px;
}
</style>
