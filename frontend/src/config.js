// Configuración de la API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

export const API_ENDPOINTS = {
  HEALTH: `${API_BASE_URL}/health`,
  METRICS: `${API_BASE_URL}/metrics`,
  PREDICT: `${API_BASE_URL}/predict`,
  TRAIN: `${API_BASE_URL}/train`,
  TRAINING_STATUS: `${API_BASE_URL}/training-status`,
  BENCHMARK: `${API_BASE_URL}/benchmark`,
  SAMPLE_DATA: `${API_BASE_URL}/sample-data`,
};

export default API_BASE_URL; 