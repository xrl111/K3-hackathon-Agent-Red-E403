<template>
  <header class="h-20 border-b border-surface-border bg-black/95 backdrop-blur-md">
    <div class="h-full px-6 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/20 flex items-center justify-center">
          <Shield class="w-4 h-4 text-cyber-cyan" />
        </div>
        <div class="brand-title flex items-center gap-3">
          <span class="brand-accent">PI-RAG</span>
          <span class="brand-white">SECURITY CHECKER</span>
          <img :src="logo" alt="PI-RAG logo" class="h-12 w-[4.5rem] rounded-md object-cover object-center" />
        </div>
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
import logo from '../../assets/logo.png';
</script>

<style scoped>
.brand-title {
  font-family: 'Press Start 2P', "PP NeueBit", sans-serif;
  font-weight: 400;
  font-size: clamp(1.125rem, 1.7vw, 1.5rem);
  line-height: 1.35;
  white-space: nowrap;
}

.brand-accent {
  color: #facc15;
  text-shadow: 2px 2px 0 rgba(113, 63, 18, 0.9), 0 0 8px rgba(250, 204, 21, 0.5);
}

.brand-white {
  color: #ffffff;
  text-shadow: 2px 2px 0 rgba(0, 0, 0, 0.9), 0 0 8px rgba(255, 255, 255, 0.18);
}

.navbar-text {
  color: #ffffff;
  font-family: 'Press Start 2P', "PP NeueBit", sans-serif;
  font-size: 0.55rem;
  line-height: 1.35;
  text-shadow: 1px 1px 0 rgba(0, 0, 0, 0.9);
}
</style>
