<template>
  <div
    :class="[
      'cyber-card overflow-hidden',
      glow ? 'cyber-glow' : '',
      padding ? 'p-6' : '',
      hoverable ? 'hover:bg-surface-hover cursor-pointer' : ''
    ]"
  >
    <!-- Optional header -->
    <div v-if="$slots.header || title" class="flex items-center justify-between px-6 py-4 border-b border-surface-border bg-surface-card/50">
      <slot name="header">
        <h3 class="text-sm font-semibold text-text-primary tracking-wide">{{ title }}</h3>
      </slot>
    </div>
    <!-- Body -->
    <div :class="$slots.header || title ? 'p-6' : ''">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string;
  glow?: boolean;
  padding?: boolean;
  hoverable?: boolean;
}>(), {
  glow: false,
  padding: true,
  hoverable: false,
});
</script>
