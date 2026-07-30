<template>
  <div class="flex items-center justify-between mb-8 animate-fade-in-up">
    <div>
      <h1 class="text-2xl font-bold text-text-primary tracking-tight">{{ title }}</h1>
      <p v-if="subtitle" class="text-sm text-text-muted mt-1">{{ subtitle }}</p>
    </div>
    <div class="flex items-center gap-3">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  subtitle?: string;
}>();
</script>
