import axios from 'axios';

// In a real app, this would be an actual Axios instance pointing to the backend.
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1' // Assuming FastAPI runs on 8000
});

export const AssessmentService = {
  async createConfig(payload: any) {
    return api.post('/assessments', payload);
  },

  async runAssessment(id: string) {
    return api.post(`/assessments/${id}/run`);
  },

  async getConfig(id: string) {
    return api.get(`/assessments/${id}`);
  },

  async getStatus(id: string) {
    return api.get(`/assessments/${id}/status`);
  },

  async getTraces(id: string) {
    return api.get(`/assessments/${id}/traces`);
  },

  async getFindings(id: string) {
    return api.get(`/assessments/${id}/findings`);
  },

  async getReport(id: string) {
    return api.get(`/assessments/${id}/report`);
  }
};

export default api;
