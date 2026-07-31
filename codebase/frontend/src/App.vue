<template>
  <div class="min-h-screen bg-surface-bg text-text-primary font-sans">
    <!-- Top Navbar -->
    <AppNavbar />

    <div class="flex min-h-[calc(100vh-80px)]">
      <!-- Left Sidebar -->
      <AppSidebar />

      <!-- Main Content Area -->
      <main class="flex-1 relative" :style="mainBgStyle">
        <!-- Darken and soften the background image for legibility -->
        <div class="absolute inset-0 bg-black/45 backdrop-blur-[8px] pointer-events-none"></div>
        <div class="relative z-10 max-w-6xl mx-auto px-8 py-8">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppNavbar from './components/layout/AppNavbar.vue';
import AppSidebar from './components/layout/AppSidebar.vue';
import bgImage from './assets/background1.png';

const mainBgStyle = {
  backgroundImage: `url(${bgImage})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
  backgroundAttachment: 'fixed',
};
</script>
