import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload a CSV file for report generation
 */
export const uploadReport = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/reports/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get list of all reports
 */
export const getReports = async () => {
  const response = await api.get('/reports');
  return response.data;
};

/**
 * Predict claims outcomes using ML model
 */
export const predictClaims = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/reports/predict', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};
