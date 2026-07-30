<template>
  <div class="flex items-center justify-between mb-8 animate-fade-in-up">
    <div>
      <h1 class="page-title text-2xl font-bold text-text-primary tracking-tight">{{ title }}</h1>
      <slot name="subtitle">
        <p v-if="subtitle" class="text-sm text-slate-300 mt-1">{{ subtitle }}</p>
      </slot>
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

<style scoped>
.page-title {
  text-shadow: 0 3px 5px rgba(0, 0, 0, 0.85);
}
</style>
