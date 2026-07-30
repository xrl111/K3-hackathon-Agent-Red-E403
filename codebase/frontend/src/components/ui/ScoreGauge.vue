<template>
  <div class="flex flex-col items-center">
    <div class="relative" :style="{ width: `${size}px`, height: `${size}px` }">
      <svg class="w-full h-full -rotate-90" :viewBox="`0 0 ${size} ${size}`">
        <!-- Background track -->
        <circle
          :cx="center" :cy="center" :r="radius"
          fill="none"
          :stroke-width="strokeWidth"
          class="stroke-surface-elevated"
          :stroke-dasharray="circumference"
        />
        <!-- Animated value arc -->
        <circle
          :cx="center" :cy="center" :r="radius"
          fill="none"
          :stroke-width="strokeWidth"
          stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="offset"
          :class="strokeColor"
          style="transition: stroke-dashoffset 1.5s ease-out;"
        />
        <!-- Glow filter for the arc -->
        <circle
          :cx="center" :cy="center" :r="radius"
          fill="none"
          :stroke-width="strokeWidth + 4"
          stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="offset"
          :class="glowColor"
          opacity="0.3"
          style="transition: stroke-dashoffset 1.5s ease-out; filter: blur(6px);"
        />
      </svg>
      <!-- Center label -->
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="font-black text-text-primary font-mono" :class="valueFontSize">{{ animatedValue }}</span>
        <span class="text-[10px] font-medium text-text-muted uppercase tracking-widest mt-0.5">/ {{ max }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue';

const props = withDefaults(defineProps<{
  value: number;
  max?: number;
  size?: number;
  strokeWidth?: number;
  color?: 'cyan' | 'danger' | 'warning' | 'success';
}>(), {
  max: 100,
  size: 180,
  strokeWidth: 10,
  color: 'cyan',
});

const center = computed(() => props.size / 2);
const radius = computed(() => (props.size - props.strokeWidth * 2) / 2);
const circumference = computed(() => 2 * Math.PI * radius.value);
const offset = computed(() => circumference.value - (circumference.value * props.value) / props.max);

const strokeColor = computed(() => ({
  cyan: 'stroke-cyber-cyan',
  danger: 'stroke-severity-critical',
  warning: 'stroke-severity-high',
  success: 'stroke-status-pass',
}[props.color]));

const glowColor = computed(() => strokeColor.value);

const valueFontSize = computed(() => {
  if (props.size >= 180) return 'text-5xl';
  if (props.size >= 120) return 'text-3xl';
  return 'text-xl';
});

// Count-up animation
const animatedValue = ref(0);
const animateCountUp = () => {
  const duration = 1500;
  const startTime = performance.now();
  const startVal = 0;
  const endVal = props.value;

  const step = (currentTime: number) => {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    animatedValue.value = Math.round(startVal + (endVal - startVal) * eased);
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
};

onMounted(() => animateCountUp());
watch(() => props.value, () => animateCountUp());
</script>
