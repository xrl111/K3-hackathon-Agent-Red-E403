<template>
  <div>
    <PageHeader title="Triage & Review" :subtitle="`Assessment ID: ${assessmentId}`">
      <template #actions>
        <AppButton @click="$router.push(`/assessments/${assessmentId}/report`)">
          <FileBarChart class="w-4 h-4" />
          Generate Report
        </AppButton>
      </template>
    </PageHeader>

    <div class="space-y-6">
      <!-- Filters -->
      <div class="flex gap-3 animate-fade-in-up">
        <select v-model="filterSeverity" class="cyber-input px-4 py-2 text-sm">
          <option value="">All Severities</option>
          <option value="CRITICAL">CRITICAL</option>
          <option value="HIGH">HIGH</option>
        </select>
        <select v-model="filterStatus" class="cyber-input px-4 py-2 text-sm">
          <option value="">All Status</option>
          <option value="OPEN">OPEN</option>
          <option value="MANUAL_VERIFICATION">MANUAL VERIFICATION</option>
        </select>
      </div>

      <!-- Findings Table -->
      <div class="cyber-card overflow-hidden animate-fade-in-up animate-delay-100">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-surface-border bg-surface-card/80">
              <th class="px-5 py-3 text-[11px] font-semibold text-text-muted uppercase tracking-wider">ID</th>
              <th class="px-5 py-3 text-[11px] font-semibold text-text-muted uppercase tracking-wider">Severity</th>
              <th class="px-5 py-3 text-[11px] font-semibold text-text-muted uppercase tracking-wider">Type</th>
              <th class="px-5 py-3 text-[11px] font-semibold text-text-muted uppercase tracking-wider">Status</th>
              <th class="px-5 py-3 text-[11px] font-semibold text-text-muted uppercase tracking-wider">Description</th>
              <th class="px-5 py-3 text-[11px] font-semibold text-text-muted uppercase tracking-wider w-20"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="finding in filteredFindings"
              :key="finding.id"
              class="border-b border-surface-border/50 hover:bg-surface-hover transition-colors cursor-pointer group"
              @click="selectedFinding = finding"
            >
              <td class="px-5 py-3.5 text-sm font-mono text-text-secondary">{{ finding.id }}</td>
              <td class="px-5 py-3.5">
                <AppBadge :severity="finding.severity" :dot="true">{{ finding.severity }}</AppBadge>
              </td>
              <td class="px-5 py-3.5 text-sm font-mono text-text-secondary">{{ finding.type }}</td>
              <td class="px-5 py-3.5">
                <AppBadge severity="PENDING">{{ finding.status.replace('_', ' ') }}</AppBadge>
              </td>
              <td class="px-5 py-3.5 text-sm text-text-muted max-w-xs truncate">{{ finding.description }}</td>
              <td class="px-5 py-3.5">
                <span class="text-cyber-cyan text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">Review →</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Finding Detail Modal -->
    <AppModal :show="!!selectedFinding" @close="selectedFinding = null" size="md">
      <template #header>
        <div class="flex items-center gap-3">
          <span :class="[
            'w-10 h-10 rounded-lg flex items-center justify-center shadow-lg',
            selectedFinding?.severity === 'CRITICAL' ? 'bg-severity-critical/20 text-severity-critical' : 'bg-severity-high/20 text-severity-high'
          ]">
            <TriangleAlert class="w-5 h-5" />
          </span>
          <div>
            <h3 class="text-base font-bold text-text-primary">{{ selectedFinding?.type }}</h3>
            <p class="text-xs text-text-muted font-mono mt-0.5">Trace: {{ selectedFinding?.trace_id }}</p>
          </div>
        </div>
      </template>

      <div class="space-y-5" v-if="selectedFinding">
        <div>
          <h4 class="text-[11px] font-semibold text-text-muted uppercase tracking-wider mb-2">Description</h4>
          <div class="p-4 bg-surface-elevated rounded-lg text-sm text-text-secondary border border-surface-border leading-relaxed">
            {{ selectedFinding.description }}
          </div>
        </div>
        <div>
          <h4 class="text-[11px] font-semibold text-text-muted uppercase tracking-wider mb-2">Remediation</h4>
          <div class="p-4 bg-cyber-cyan-subtle rounded-lg text-sm text-cyber-cyan border border-cyber-cyan/10 leading-relaxed">
            {{ selectedFinding.remediation }}
          </div>
        </div>
      </div>

      <template #footer>
        <AppButton variant="secondary" @click="selectedFinding = null">
          Mark as False Positive
        </AppButton>
        <AppButton variant="danger" @click="selectedFinding = null">
          <TriangleAlert class="w-3.5 h-3.5" />
          Confirm Vulnerability
        </AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { FileBarChart, TriangleAlert } from '@lucide/vue';
import { AssessmentService } from '../services/api';
import PageHeader from '../components/layout/PageHeader.vue';
import AppButton from '../components/ui/AppButton.vue';
import AppBadge from '../components/ui/AppBadge.vue';
import AppModal from '../components/ui/AppModal.vue';

const route = useRoute();
const assessmentId = route.params.id as string;

const findings = ref<any[]>([]);
const selectedFinding = ref<any>(null);
const filterSeverity = ref('');
const filterStatus = ref('');

const filteredFindings = computed(() => {
  return findings.value.filter(f => {
    if (filterSeverity.value && f.severity !== filterSeverity.value) return false;
    if (filterStatus.value && f.status !== filterStatus.value) return false;
    return true;
  });
});

onMounted(async () => {
  const res = await AssessmentService.getFindings(assessmentId);
  findings.value = res.data;
});
</script>
