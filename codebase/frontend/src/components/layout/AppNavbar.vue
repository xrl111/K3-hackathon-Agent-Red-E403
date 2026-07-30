<template>
  <header class="h-14 border-b border-surface-border bg-black/95 backdrop-blur-md sticky top-0 z-50">
    <div class="h-full px-6 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/20 flex items-center justify-center">
          <Shield class="w-4 h-4 text-cyber-cyan" />
        </div>
        <span class="brand-title text-sm tracking-wide">PI-RAG SECURITY CHECKER</span>
      </div>
      
      <!-- Right actions -->
      <div class="flex items-center gap-4">
        <div class="navbar-text flex items-center gap-2 text-xs">
          <span class="w-2 h-2 rounded-full bg-status-pass animate-pulse"></span>
          System Online
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Shield } from '@lucide/vue';
</script>

<style scoped>
.brand-title {
  color: #facc15;
  font-family: 'Press Start 2P', "PP NeueBit", sans-serif;
  font-weight: 400;
  font-size: 0.625rem;
  line-height: 1.35;
  text-shadow: 2px 2px 0 rgba(113, 63, 18, 0.9), 0 0 8px rgba(250, 204, 21, 0.5);
}

.navbar-text {
  color: #ffffff;
  font-family: 'Press Start 2P', "PP NeueBit", sans-serif;
  font-size: 0.55rem;
  line-height: 1.35;
  text-shadow: 1px 1px 0 rgba(0, 0, 0, 0.9);
}
</style>
