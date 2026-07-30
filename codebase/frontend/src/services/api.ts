import axios from 'axios';
import { 
  mockAssessmentConfig, 
  mockStatus, 
  mockTraces, 
  mockFindings, 
  mockReport 
} from '../mocks';

// In a real app, this would be an actual Axios instance pointing to the backend.
const api = axios.create({
  baseURL: '/api/v1'
});

// Helper to simulate network latency
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const AssessmentService = {
  async getConfig(id: string) {
    await delay(300);
    return { data: mockAssessmentConfig };
  },

  async getStatus(id: string) {
    await delay(200);
    // Simulate progression if we want, or just return mock Status
    return { data: mockStatus };
  },

  async getTraces(id: string) {
    await delay(400);
    return { data: mockTraces };
  },

  async getFindings(id: string) {
    await delay(500);
    return { data: mockFindings };
  },

  async getReport(id: string) {
    await delay(300);
    return { data: mockReport };
  }
};

export default api;
