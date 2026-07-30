<template>
  <button
    :class="[
      'inline-flex items-center justify-center gap-2 font-medium rounded-lg transition-all duration-200 cursor-pointer select-none',
      'active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100',
      sizeClasses,
      variantClasses
    ]"
    :disabled="disabled || loading"
  >
    <!-- Loading spinner -->
    <svg v-if="loading" class="animate-spin -ml-0.5 w-4 h-4" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
}>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false,
});

const sizeClasses = computed(() => ({
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-5 py-2.5 text-sm',
  lg: 'px-6 py-3 text-base',
}[props.size]));

const variantClasses = computed(() => ({
  primary: 'bg-cyber-cyan text-slate-950 hover:bg-cyber-cyan-hover shadow-lg shadow-cyber-cyan-glow',
  secondary: 'bg-surface-elevated text-text-primary border border-surface-border hover:border-cyber-cyan/30 hover:bg-surface-card',
  danger: 'bg-severity-critical/10 text-severity-critical border border-severity-critical/20 hover:bg-severity-critical/20',
  ghost: 'text-text-secondary hover:text-text-primary hover:bg-surface-hover',
}[props.variant]));
</script>
