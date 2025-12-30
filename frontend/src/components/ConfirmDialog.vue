<template>
  <Dialog
    :visible="visible"
    header="Подтвердите действие"
    modal
    @hide="$emit('update:visible', false)"
  >
    <p>Вы уверены?</p>
    <template #footer>
      <Button label="Отмена" class="p-button-text" @click="$emit('update:visible', false)" />
      <Button label="Да" class="p-button-danger" @click="$emit('confirm')" />
    </template>
  </Dialog>
</template>

<script setup>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
</script>
