<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-surface-bg/80 backdrop-blur-sm"></div>
        
        <!-- Modal Panel -->
        <div :class="['relative w-full rounded-xl border border-surface-border bg-surface-card shadow-2xl', sizeClass]">
          <!-- Glow accent top border -->
          <div class="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-cyber-cyan/50 to-transparent"></div>

          <!-- Header -->
          <div v-if="$slots.header || title" class="flex items-center justify-between p-6 pb-0">
            <slot name="header">
              <h2 class="text-lg font-bold text-text-primary">{{ title }}</h2>
            </slot>
            <button @click="$emit('close')" class="p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface-elevated transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
          </div>

          <!-- Body -->
          <div class="p-6">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="flex items-center justify-end gap-3 px-6 pb-6 pt-2 border-t border-surface-border mt-2">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  show: boolean;
  title?: string;
  size?: 'sm' | 'md' | 'lg';
}>(), {
  size: 'md',
});

defineEmits<{
  (e: 'close'): void;
}>();

const sizeClass = computed(() => ({
  sm: 'max-w-md',
  md: 'max-w-2xl',
  lg: 'max-w-4xl',
}[props.size]));
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .relative {
  transform: scale(0.95) translateY(8px);
}
.modal-leave-to .relative {
  transform: scale(0.95) translateY(8px);
}
</style>
