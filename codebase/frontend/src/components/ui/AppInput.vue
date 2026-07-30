<template>
  <div class="space-y-1.5">
    <label v-if="label" :for="inputId" class="block text-xs font-medium text-text-secondary uppercase tracking-wider">
      {{ label }}
    </label>
    <div class="relative">
      <slot name="icon">
        <component v-if="icon" :is="icon" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted pointer-events-none" />
      </slot>
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :class="[
          'cyber-input w-full py-2.5 text-sm',
          icon ? 'pl-10 pr-4' : 'px-4',
          disabled ? 'opacity-50 cursor-not-allowed' : ''
        ]"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  modelValue?: string;
  label?: string;
  placeholder?: string;
  type?: string;
  icon?: any;
  disabled?: boolean;
}>(), {
  modelValue: '',
  type: 'text',
  disabled: false,
});

defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const inputId = computed(() => `input-${props.label?.toLowerCase().replace(/\s+/g, '-') || Math.random().toString(36).slice(2)}`);
</script>
