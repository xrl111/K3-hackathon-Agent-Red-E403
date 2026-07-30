<template>
  <div>
    <PageHeader title="New Assessment" subtitle="Configure your AI security assessment target and policies" />

    <div class="cyber-card p-6 relative overflow-hidden">

      <div class="relative space-y-10 max-w-2xl">

        <!-- Step 1: Target URL -->
        <section class="animate-fade-in-up">
          <div class="flex items-center gap-3 mb-4">
            <span class="w-7 h-7 rounded-md bg-white/15 backdrop-blur-sm border border-white/20 text-white flex items-center justify-center text-xs font-bold">1</span>
            <h2 class="text-lg font-semibold text-text-primary">Target Configuration</h2>
          </div>
          <div class="ml-10">
            <AppInput
              v-model="targetUrl"
              label="Target API URL"
              placeholder="https://api.project-target.com/chat"
              :icon="Globe"
            />
          </div>
        </section>

        <!-- Step 2: Policies -->
        <section class="animate-fade-in-up animate-delay-100">
          <div class="flex items-center gap-3 mb-4">
            <span class="w-7 h-7 rounded-md bg-white/15 backdrop-blur-sm border border-white/20 text-white flex items-center justify-center text-xs font-bold">2</span>
            <h2 class="text-lg font-semibold text-text-primary">Security Policies</h2>
          </div>
          <div class="ml-10 space-y-2">
            <label
              v-for="policy in policies"
              :key="policy.text"
              class="flex items-center gap-3 p-3 rounded-lg border border-surface-border hover:border-cyber-cyan/20 hover:bg-cyber-cyan-subtle cursor-pointer transition-all group"
            >
              <input
                type="checkbox"
                :checked="policy.checked"
                class="w-4 h-4 rounded border-surface-border text-cyber-cyan focus:ring-cyber-cyan/30 bg-surface-card"
              />
              <span class="text-sm text-text-secondary group-hover:text-text-primary transition-colors">{{ policy.text }}</span>
            </label>
            <button class="flex items-center gap-1.5 text-cyber-cyan text-sm font-medium hover:underline mt-3">
              <Plus class="w-3.5 h-3.5" />
              Add Custom Policy
            </button>
          </div>
        </section>

        <!-- Step 3: Profiles -->
        <section class="animate-fade-in-up animate-delay-200">
          <div class="flex items-center gap-3 mb-4">
            <span class="w-7 h-7 rounded-md bg-white/15 backdrop-blur-sm border border-white/20 text-white flex items-center justify-center text-xs font-bold">3</span>
            <h2 class="text-lg font-semibold text-text-primary">Test Profiles</h2>
          </div>
          <div class="ml-10 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div
              v-for="profile in profiles"
              :key="profile.id"
              @click="toggleProfile(profile.id)"
              :class="[
                'p-4 rounded-xl border-2 cursor-pointer transition-all relative overflow-hidden group',
                selectedProfiles.includes(profile.id)
                  ? 'border-cyber-cyan bg-cyber-cyan-subtle cyber-glow'
                  : 'border-surface-border hover:border-cyber-cyan/30'
              ]"
            >
              <div class="flex items-center gap-2">
                <component :is="profile.icon" class="w-4 h-4" :class="selectedProfiles.includes(profile.id) ? 'text-cyber-cyan' : 'text-text-muted'" />
                <span class="font-medium text-sm">{{ profile.name }}</span>
              </div>
              <p class="text-xs text-text-muted mt-2 leading-relaxed">{{ profile.description }}</p>
              <!-- Selected indicator -->
              <div v-if="selectedProfiles.includes(profile.id)" class="absolute top-3 right-3 w-2 h-2 rounded-full bg-cyber-cyan shadow-[0_0_6px_rgba(6,182,212,0.6)]"></div>
            </div>
          </div>
        </section>

        <!-- Submit -->
        <div class="ml-10 pt-4 animate-fade-in-up animate-delay-300">
          <AppButton @click="$router.push('/assessments/uuid-1234/runner')">
            <Zap class="w-4 h-4" />
            Start Assessment
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Globe, Plus, Zap, Crosshair, Database } from '@lucide/vue';
import PageHeader from '../components/layout/PageHeader.vue';
import AppInput from '../components/ui/AppInput.vue';
import AppButton from '../components/ui/AppButton.vue';

const targetUrl = ref('');

const policies = ref([
  { text: 'Do not disclose CANARY_SECRET', checked: true },
  { text: 'Only respond in Vietnamese', checked: true },
]);

const profiles = ref([
  { id: 'direct_injection', name: 'Direct Injection', description: 'Test for common prompt injection and jailbreak techniques.', icon: Crosshair },
  { id: 'rag_poisoning', name: 'RAG Poisoning', description: 'Test resilience against manipulated context chunks.', icon: Database },
]);

const selectedProfiles = ref<string[]>(['direct_injection']);

const toggleProfile = (id: string) => {
  const idx = selectedProfiles.value.indexOf(id);
  if (idx >= 0) selectedProfiles.value.splice(idx, 1);
  else selectedProfiles.value.push(id);
};
</script>
