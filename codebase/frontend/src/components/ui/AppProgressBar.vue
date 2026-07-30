<template>
  <div class="space-y-2">
    <div class="flex justify-between items-center">
      <span class="text-xs font-medium text-text-secondary uppercase tracking-wider">{{ label }}</span>
      <span class="text-sm font-bold text-cyber-cyan font-mono">{{ percentage }}%</span>
    </div>
    <div class="h-2.5 w-full bg-surface-elevated rounded-full overflow-hidden">
      <div
        class="h-full rounded-full relative transition-all duration-1000 ease-out"
        :class="barColor"
        :style="{ width: `${percentage}%` }"
      >
        <!-- Shimmer effect -->
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent" style="animation: shimmer 2s infinite"></div>
      </div>
    </div>
    <div v-if="subtitle" class="text-xs text-text-muted">{{ subtitle }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  percentage: number;
  label?: string;
  subtitle?: string;
  color?: 'cyan' | 'danger' | 'warning' | 'success';
}>(), {
  label: 'Progress',
  color: 'cyan',
});

const barColor = computed(() => ({
  cyan: 'bg-cyber-cyan shadow-[0_0_12px_rgba(6,182,212,0.4)]',
  danger: 'bg-severity-critical shadow-[0_0_12px_rgba(239,68,68,0.4)]',
  warning: 'bg-severity-high shadow-[0_0_12px_rgba(245,158,11,0.4)]',
  success: 'bg-status-pass shadow-[0_0_12px_rgba(16,185,129,0.4)]',
}[props.color]));
</script>
