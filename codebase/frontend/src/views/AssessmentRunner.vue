<template>
  <div>
    <PageHeader title="Test Execution Dashboard">
      <template #subtitle>
        <p class="text-sm text-slate-300 mt-1">Assessment ID: <span class="text-yellow-400">{{ assessmentId }}</span></p>
      </template>
      <template #actions>
        <AppButton variant="secondary" @click="$router.push(`/assessments/${assessmentId}/findings`)">
          <Eye class="w-4 h-4" />
          View Findings
        </AppButton>
      </template>
    </PageHeader>

    <div class="space-y-6">
      <!-- Progress Section -->
      <AppCard class="animate-fade-in-up">
        <div class="flex justify-between items-end mb-4">
          <div>
            <div class="text-[11px] font-medium text-text-muted uppercase tracking-wider">Current Phase</div>
            <div class="text-base font-semibold mt-1 flex items-center gap-2" :class="status?.status === 'CANCELLED' ? 'text-severity-critical' : 'text-cyber-cyan'">
              <span v-if="status?.status === 'RUNNING'" class="w-2 h-2 rounded-full bg-cyber-cyan animate-pulse shadow-[0_0_6px_rgba(250,204,21,0.5)]"></span>
              <span v-else-if="status?.status === 'CANCELLED'" class="w-2 h-2 rounded-full bg-severity-critical"></span>
              <span v-else class="w-2 h-2 rounded-full bg-cyber-cyan"></span>
              {{ status?.current_phase || 'Initializing...' }}
            </div>
          </div>
          <AppButton v-if="status?.status === 'RUNNING'" variant="secondary" @click="cancelTest" class="border-severity-critical/20 text-severity-critical hover:bg-severity-critical/10">
            <Square class="w-4 h-4" />
            Stop
          </AppButton>
        </div>
        <AppProgressBar
          :percentage="status?.progress_percentage || 0"
          label="Test Progress"
          :subtitle="`${status?.completed_tests || 0} / ${status?.total_tests || 0} tests completed`"
        />

        <div v-if="status?.status === 'COMPLETED'" class="mt-5 pt-4 border-t border-surface-border flex justify-between items-center animate-fade-in-up">
          <p class="text-sm font-medium text-text-secondary">
            Assessment finished. <span class="text-cyber-cyan">{{ status?.current_phase }}</span>
          </p>
          <AppButton @click="$router.push(`/assessments/${assessmentId}/report`)">
            <Zap class="w-4 h-4" />
            View Final Report
          </AppButton>
        </div>
      </AppCard>

      <!-- Chat & RAG Trace UI -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[520px] animate-fade-in-up animate-delay-100">

        <!-- Chat View -->
        <div class="lg:col-span-2 cyber-card flex flex-col overflow-hidden">
          <div class="px-5 py-3 border-b border-surface-border bg-surface-card/80 flex items-center gap-2">
            <Terminal class="w-4 h-4 text-cyber-cyan" />
            <span class="text-sm font-semibold text-text-primary">Execution Trace</span>
          </div>
          <div class="flex-1 overflow-y-auto p-5 space-y-5">
            <div v-for="trace in traces?.traces" :key="trace.trace_id" class="space-y-4">
              <!-- System Prompt (left) -->
              <div class="flex gap-3 items-start">
                <div class="w-7 h-7 rounded-md bg-cyber-cyan/10 border border-cyber-cyan/20 text-cyber-cyan flex items-center justify-center shrink-0 text-xs font-bold">S</div>
                <div
                  class="bg-surface-elevated/80 p-3.5 rounded-xl rounded-tl-none border text-sm cursor-pointer transition-all"
                  :class="activeTrace?.trace_id === trace.trace_id ? 'border-cyber-cyan/40 cyber-glow' : 'border-surface-border hover:border-cyber-cyan/20'"
                  @click="activeTrace = trace"
                >
                  <!-- Agent Thought -->
                  <div v-if="trace.agent_thought" class="mb-3 p-3 bg-slate-900/50 rounded-lg border border-slate-700/50 text-left">
                    <div class="text-[10px] font-bold text-cyber-cyan mb-1 flex items-center gap-1 uppercase tracking-wider">
                      <Terminal class="w-3 h-3" /> Agent Thought Process
                    </div>
                    <div class="trace-mono text-slate-400 text-xs italic">{{ trace.agent_thought }}</div>
                  </div>
                  <span class="trace-mono text-text-secondary">{{ trace.prompt_sent }}</span>
                  <!-- Evaluator badge -->
                  <div class="mt-2 flex items-center gap-2">
                    <AppBadge :severity="trace.evaluator_pass ? 'PASS' : 'FAIL'" :dot="true">
                      {{ trace.evaluator_pass ? 'DEFENDED' : 'BREACHED' }}
                    </AppBadge>
                    <span class="trace-mono text-[10px] text-text-muted truncate">{{ trace.evaluator_reason }}</span>
                  </div>
                </div>
              </div>

              <!-- AI Response (right) -->
              <div class="flex gap-3 items-start flex-row-reverse">
                <div class="w-7 h-7 rounded-md bg-surface-elevated border border-surface-border text-text-muted flex items-center justify-center shrink-0 text-[10px] font-bold">AI</div>
                <div class="trace-mono bg-surface-elevated/80 border border-surface-border text-text-primary p-3.5 rounded-xl rounded-tr-none text-sm max-w-[80%]">
                  {{ trace.model_response }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- RAG Context Panel -->
        <div class="cyber-card flex flex-col overflow-hidden">
          <div class="px-5 py-3 border-b border-surface-border bg-surface-card/80 flex items-center gap-2">
            <Database class="w-4 h-4 text-cyber-cyan" />
            <span class="text-sm font-semibold text-text-primary">RAG Chunks</span>
          </div>
          <div v-if="activeTrace" class="flex-1 overflow-y-auto p-4 space-y-3">
            <div
              v-for="chunk in activeTrace.retrieved_chunks"
              :key="chunk.chunk_id"
              :class="[
                'p-3 text-sm rounded-lg border transition-all',
                chunk.is_poisoned
                  ? 'bg-severity-critical/5 border-severity-critical/20 cyber-glow-danger'
                  : 'bg-surface-elevated/50 border-surface-border'
              ]"
            >
              <div class="flex justify-between items-center mb-2">
                <span class="text-[10px] font-mono font-bold" :class="chunk.is_poisoned ? 'text-severity-critical' : 'text-text-muted'">
                  {{ chunk.chunk_id }}
                </span>
                <span class="text-[10px] font-mono text-cyber-cyan">{{ chunk.score.toFixed(2) }}</span>
              </div>
              <p :class="chunk.is_poisoned ? 'text-severity-critical/90' : 'text-text-secondary'" class="trace-mono text-xs leading-relaxed">
                {{ chunk.text }}
              </p>
              <div v-if="chunk.is_poisoned" class="mt-2">
                <AppBadge severity="CRITICAL" :dot="true">POISONED</AppBadge>
              </div>
            </div>
          </div>
          <div v-else class="flex-1 flex items-center justify-center p-6">
            <div class="text-center">
              <Database class="w-8 h-8 text-text-muted/30 mx-auto mb-2" />
              <p class="text-xs text-text-muted">Click on a prompt to inspect retrieved chunks</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { Eye, Terminal, Database, Zap, Square } from '@lucide/vue';
import { AssessmentService } from '../services/api';
import PageHeader from '../components/layout/PageHeader.vue';
import AppCard from '../components/ui/AppCard.vue';
import AppButton from '../components/ui/AppButton.vue';
import AppBadge from '../components/ui/AppBadge.vue';
import AppProgressBar from '../components/ui/AppProgressBar.vue';

const route = useRoute();
const assessmentId = route.params.id as string;

const status = ref<any>(null);
const traces = ref<any>(null);
const activeTrace = ref<any>(null);
let pollInterval: any;

const fetchStatus = async () => {
  const res = await AssessmentService.getStatus(assessmentId);
  status.value = res.data;
};

const fetchTraces = async () => {
  const res = await AssessmentService.getTraces(assessmentId);
  
  const parsedTraces = res.data.traces.map((trace: any) => {
    let chunks: any[] = [];
    let thought = "";
    if (trace.retrieved_chunks_json) {
      try {
        const rawChunks = JSON.parse(trace.retrieved_chunks_json);
        rawChunks.forEach((c: any, index: number) => {
          if (c.metadata?.is_thought) {
            thought = c.content;
          } else {
            chunks.push({
              chunk_id: c.metadata?.source_id || `chunk-${index}`,
              is_poisoned: c.metadata?.is_poisoned || false,
              score: 0.99,
              text: c.content
            });
          }
        });
      } catch(e) {
        console.error('Failed to parse chunks', e);
      }
    }
    return { ...trace, retrieved_chunks: chunks, agent_thought: thought };
  });

  traces.value = { ...res.data, traces: parsedTraces };
  if (parsedTraces.length > 0 && !activeTrace.value) {
    activeTrace.value = parsedTraces[0];
  }
};

const cancelTest = async () => {
  try {
    await AssessmentService.cancelAssessment(assessmentId);
    if (pollInterval) clearInterval(pollInterval);
    if (status.value) {
      status.value.status = 'CANCELLED';
      status.value.current_phase = 'Assessment Cancelled';
    }
  } catch(e) {
    console.error('Failed to cancel test', e);
  }
};

onMounted(() => {
  fetchStatus();
  fetchTraces();
  pollInterval = setInterval(() => {
    if (status.value?.status === 'COMPLETED' || status.value?.status === 'FAILED' || status.value?.status === 'CANCELLED') {
      clearInterval(pollInterval);
      return;
    }
    fetchStatus();
    fetchTraces();
  }, 3000);
});

onUnmounted(() => clearInterval(pollInterval));
</script>

<style scoped>
.trace-mono {
  font-family: 'JetBrains Mono', ui-monospace, Consolas, monospace;
}
</style>
