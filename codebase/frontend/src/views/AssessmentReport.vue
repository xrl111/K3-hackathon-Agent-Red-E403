<template>
  <div>
    <PageHeader title="Executive Dashboard" :subtitle="`Final Report — Assessment ${assessmentId}`">
      <template #subtitle>
        <p class="text-sm text-slate-300 mt-1">Final Report — Assessment <span class="text-yellow-400">{{ assessmentId }}</span></p>
      </template>
      <template #actions>
        <AppButton variant="secondary">
          <Download class="w-4 h-4" />
          Export PDF
        </AppButton>
      </template>
    </PageHeader>

    <div v-if="report" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Left Column -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Readiness Score Gauge -->
          <AppCard class="animate-fade-in-up" :padding="false">
            <div class="p-8 flex flex-col items-center text-center relative overflow-hidden group">
              <!-- Ambient glow -->
              <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700"
                   :class="report.readiness_score >= 70 ? 'bg-status-pass/5' : 'bg-severity-high/5'"
                   style="filter: blur(40px);">
              </div>

              <h2 class="text-xs font-semibold text-slate-300 uppercase tracking-widest mb-8">Readiness Score</h2>

              <ScoreGauge
                :value="report.readiness_score"
                :color="report.readiness_score >= 80 ? 'success' : report.readiness_score >= 50 ? 'warning' : 'danger'"
              />

              <div class="mt-8">
                <div class="text-[10px] text-text-muted uppercase tracking-wider mb-1.5">Recommendation</div>
                <AppBadge
                  :severity="report.recommendation === 'GO' ? 'PASS' : report.recommendation === 'NO GO' ? 'CRITICAL' : 'HIGH'"
                >
                  {{ report.recommendation }}
                </AppBadge>
              </div>
            </div>
          </AppCard>

          <!-- AI Executive Summary Card -->
          <AppCard title="AI Executive Summary" class="animate-fade-in-up animate-delay-100">
            <div v-if="report.executive_summary" class="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
              {{ report.executive_summary }}
            </div>
            <div v-else class="flex flex-col items-center justify-center py-6 text-center">
              <p class="text-sm text-slate-400 mb-4">No AI summary generated yet.</p>
              <AppButton @click="generateSummary" :disabled="isGeneratingSummary">
                <Sparkles v-if="!isGeneratingSummary" class="w-4 h-4 mr-2" />
                <Loader2 v-else class="w-4 h-4 mr-2 animate-spin" />
                {{ isGeneratingSummary ? 'Analyzing...' : 'Generate with AI' }}
              </AppButton>
            </div>
          </AppCard>
        </div>

        <!-- Metrics Column -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Metric Cards Row -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <MetricCard
              class="animate-fade-in-up animate-delay-100"
              label="Total Tests"
              :value="report.metrics.total_tests_run"
              :icon="FlaskConical"
              color="cyan"
            />
            <MetricCard
              class="animate-fade-in-up animate-delay-200"
              label="ASR (Attack Success)"
              :value="report.metrics.attack_success_rate_asr"
              :icon="Crosshair"
              color="warning"
            />
            <MetricCard
              class="animate-fade-in-up animate-delay-300"
              label="PRR (Poison Retrieval)"
              :value="report.metrics.poison_retrieval_rate_prr"
              :icon="Database"
              color="warning"
            />
          </div>

          <!-- Vulnerability Breakdown -->
          <AppCard title="Vulnerability Breakdown" :padding="false" class="animate-fade-in-up animate-delay-400">
            <div class="p-6 space-y-5">
              <div v-for="item in breakdownItems" :key="item.label" class="flex items-center gap-4">
                <div class="w-20 text-xs font-medium text-slate-300 uppercase tracking-wider">{{ item.label }}</div>
                <div class="flex-1 h-2.5 bg-surface-elevated rounded-full overflow-hidden">
                  <div
                    :class="item.barColor"
                    class="h-full rounded-full transition-all duration-1000 ease-out"
                    :style="{ width: `${Math.min((item.count / maxBreakdown) * 100, 100)}%` }"
                  ></div>
                </div>
                <div class="w-6 text-right text-sm font-bold font-mono" :class="item.textColor">{{ item.count }}</div>
              </div>
            </div>
          </AppCard>

          <!-- Radar dimensions -->
          <AppCard title="Security Dimensions" :padding="false" class="animate-fade-in-up animate-delay-500">
            <div class="p-6">
              <div class="space-y-4">
                <div v-for="(label, i) in report.radar_chart?.labels || []" :key="label" class="flex items-center gap-4">
                  <div class="w-36 text-xs font-medium text-slate-300">{{ label }}</div>
                  <div class="flex-1 h-2 bg-surface-elevated rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full bg-cyber-cyan transition-all duration-1000 ease-out"
                      :style="{ width: `${report.radar_chart?.data?.[i] || 0}%` }"
                    ></div>
                  </div>
                  <span class="text-xs font-mono font-bold text-cyber-cyan w-8 text-right">{{ report.radar_chart?.data?.[i] || 0 }}%</span>
                </div>
              </div>
            </div>
          </AppCard>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Download, FlaskConical, Crosshair, Database, Sparkles, Loader2 } from '@lucide/vue';
import { AssessmentService } from '../services/api';
import PageHeader from '../components/layout/PageHeader.vue';
import AppCard from '../components/ui/AppCard.vue';
import AppButton from '../components/ui/AppButton.vue';
import AppBadge from '../components/ui/AppBadge.vue';
import ScoreGauge from '../components/ui/ScoreGauge.vue';
import MetricCard from '../components/ui/MetricCard.vue';

const route = useRoute();
const assessmentId = route.params.id as string;
const report = ref<any>(null);
const isGeneratingSummary = ref(false);

onMounted(async () => {
  const res = await AssessmentService.getReport(assessmentId);
  report.value = res.data;
});

const generateSummary = async () => {
  if (isGeneratingSummary.value) return;
  isGeneratingSummary.value = true;
  try {
    const res = await AssessmentService.generateReportSummary(assessmentId);
    if (res.data && res.data.executive_summary) {
      report.value.executive_summary = res.data.executive_summary;
    }
  } catch (err) {
    console.error("Failed to generate summary", err);
    alert("Failed to generate AI summary. Please try again.");
  } finally {
    isGeneratingSummary.value = false;
  }
};

const breakdownItems = computed(() => {
  if (!report.value) return [];
  return [
    { label: 'Critical', count: report.value.metrics.total_critical, barColor: 'bg-severity-critical shadow-[0_0_8px_rgba(239,68,68,0.3)]', textColor: 'text-severity-critical' },
    { label: 'High', count: report.value.metrics.total_high, barColor: 'bg-severity-high shadow-[0_0_8px_rgba(245,158,11,0.3)]', textColor: 'text-severity-high' },
    { label: 'Medium', count: report.value.metrics.total_medium, barColor: 'bg-severity-medium shadow-[0_0_8px_rgba(234,179,8,0.3)]', textColor: 'text-severity-medium' },
  ];
});

const maxBreakdown = computed(() => {
  if (!report.value) return 1;
  return Math.max(report.value.metrics.total_critical, report.value.metrics.total_high, report.value.metrics.total_medium, 1);
});
</script>
