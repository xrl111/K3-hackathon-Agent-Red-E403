<template>
  <aside class="w-60 border-r border-surface-border bg-black flex flex-col shrink-0">
    <!-- Workflow Steps -->
    <nav class="flex-1 p-4 space-y-1">
      <div class="text-[10px] font-semibold text-text-muted uppercase tracking-widest mb-4 px-3">Assessment Flow</div>
      
      <router-link
        v-for="(item, index) in navItems"
        :key="item.path"
        :to="item.path"
        :class="[
          'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group',
          isActive(item.path)
            ? 'bg-yellow-400/10 text-yellow-400 border border-yellow-400/30'
            : 'text-slate-500 hover:text-slate-400 hover:bg-surface-hover border border-transparent'
        ]"
      >
        <span
          :class="[
            'w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold shrink-0 transition-colors',
            isActive(item.path)
              ? 'bg-yellow-400 text-black'
              : isCompleted(index) 
                ? 'bg-status-pass/20 text-white'
                : 'bg-surface-elevated text-white'
          ]"
        >
          <svg v-if="isCompleted(index) && !isActive(item.path)" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          <span v-else>{{ index + 1 }}</span>
        </span>
        <span>{{ item.label }}</span>
        
        <!-- Active glow indicator -->
        <span v-if="isActive(item.path)" class="ml-auto w-1.5 h-1.5 rounded-full bg-yellow-400 shadow-[0_0_6px_rgba(250,204,21,0.6)]"></span>
      </router-link>
    </nav>
    
    <!-- Bottom info -->
    <div class="p-4 border-t border-surface-border">
      <div class="text-[10px] text-text-muted uppercase tracking-wider">Current ID</div>
      <div class="text-xs font-mono text-text-secondary mt-1 truncate">uuid-1234</div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const navItems = [
  { label: 'New Assessment', path: '/assessments/new' },
  { label: 'Test Runner', path: '/assessments/uuid-1234/runner' },
  { label: 'Findings', path: '/assessments/uuid-1234/findings' },
  { label: 'Report', path: '/assessments/uuid-1234/report' },
];

const currentIndex = computed(() => {
  return navItems.findIndex(item => route.path === item.path);
});

const isActive = (path: string) => route.path === path;
const isCompleted = (index: number) => index < currentIndex.value;
</script>
