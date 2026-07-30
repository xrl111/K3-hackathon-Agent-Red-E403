<template>
  <header class="h-14 border-b border-surface-border bg-surface-card/80 backdrop-blur-md sticky top-0 z-50">
    <div class="h-full px-6 flex items-center justify-between">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/20 flex items-center justify-center">
          <Shield class="w-4 h-4 text-cyber-cyan" />
        </div>
        <span class="font-bold text-sm gradient-text tracking-wide">PI-RAG SECURITY CHECKER</span>
      </div>
      
      <!-- Right actions -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 text-xs text-text-muted">
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
