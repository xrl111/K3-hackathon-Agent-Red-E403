<template>
  <div class="cyber-card p-5 group relative overflow-hidden">
    <!-- Subtle hover glow -->
    <div class="absolute inset-0 bg-gradient-to-br from-cyber-cyan/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
    
    <div class="relative z-10">
      <div class="flex items-center justify-between mb-3">
        <span class="text-[11px] font-medium text-slate-300 uppercase tracking-wider">{{ label }}</span>
        <component v-if="icon" :is="icon" class="w-4 h-4 text-text-muted" />
      </div>
      <div class="font-['JetBrains_Mono'] font-bold leading-none" :class="[valueSizeClass, valueColorClass]">
        {{ value }}
      </div>
      <div v-if="subtitle" class="text-xs text-text-muted mt-2">{{ subtitle }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  label: string;
  value: string | number;
  subtitle?: string;
  icon?: any;
  size?: 'sm' | 'md' | 'lg';
  color?: 'default' | 'cyan' | 'danger' | 'warning' | 'success';
}>(), {
  size: 'md',
  color: 'default',
});

const valueSizeClass = computed(() => ({
  sm: 'text-xl',
  md: 'text-3xl',
  lg: 'text-4xl',
}[props.size]));

const valueColorClass = computed(() => ({
  default: 'text-text-primary',
  cyan: 'text-cyber-cyan',
  danger: 'text-severity-critical',
  warning: 'text-severity-high',
  success: 'text-status-pass',
}[props.color]));
</script>
