<template>
  <span :class="['inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold uppercase tracking-wider border', colorClasses]">
    <span v-if="dot" :class="['w-1.5 h-1.5 rounded-full', dotColor]"></span>
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  severity?: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'PASS' | 'FAIL' | 'OPEN' | 'PENDING' | string;
  label?: string;
  dot?: boolean;
}>(), {
  severity: 'LOW',
  dot: false,
});

const colorClasses = computed(() => {
  const map: Record<string, string> = {
    CRITICAL: 'bg-severity-critical/10 text-severity-critical border-severity-critical/20',
    HIGH: 'bg-severity-high/10 text-severity-high border-severity-high/20',
    MEDIUM: 'bg-severity-medium/10 text-severity-medium border-severity-medium/20',
    LOW: 'bg-surface-elevated text-text-muted border-surface-border',
    PASS: 'bg-status-pass/10 text-status-pass border-status-pass/20',
    FAIL: 'bg-severity-critical/10 text-severity-critical border-severity-critical/20',
    OPEN: 'bg-severity-high/10 text-severity-high border-severity-high/20',
    PENDING: 'bg-surface-elevated text-text-muted border-surface-border',
  };
  return map[props.severity?.toUpperCase()] || map.LOW;
});

const dotColor = computed(() => {
  const map: Record<string, string> = {
    CRITICAL: 'bg-severity-critical',
    HIGH: 'bg-severity-high',
    MEDIUM: 'bg-severity-medium',
    LOW: 'bg-text-muted',
    PASS: 'bg-status-pass',
    FAIL: 'bg-severity-critical',
    OPEN: 'bg-severity-high',
    PENDING: 'bg-text-muted',
  };
  return map[props.severity?.toUpperCase()] || map.LOW;
});
</script>
