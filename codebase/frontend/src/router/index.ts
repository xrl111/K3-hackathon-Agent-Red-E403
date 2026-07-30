import { createRouter, createWebHistory } from 'vue-router';

// We will create these views next
const AssessmentNew = () => import('../views/AssessmentNew.vue');
const AssessmentRunner = () => import('../views/AssessmentRunner.vue');
const AssessmentFindings = () => import('../views/AssessmentFindings.vue');
const AssessmentReport = () => import('../views/AssessmentReport.vue');

const routes = [
  {
    path: '/',
    redirect: '/assessments/new'
  },
  {
    path: '/assessments/new',
    name: 'NewAssessment',
    component: AssessmentNew
  },
  {
    path: '/assessments/:id/runner',
    name: 'AssessmentRunner',
    component: AssessmentRunner
  },
  {
    path: '/assessments/:id/findings',
    name: 'AssessmentFindings',
    component: AssessmentFindings
  },
  {
    path: '/assessments/:id/report',
    name: 'AssessmentReport',
    component: AssessmentReport
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
