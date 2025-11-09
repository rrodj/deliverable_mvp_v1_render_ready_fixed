import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const api = axios.create({ baseURL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = config.headers || {};
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

export const login = async (username: string, password: string) => {
  const res = await api.post('/auth/login', { username, password });
  return res.data as { access_token: string, token_type: string };
};

export const fetchHealth = async () => (await api.get('/healthz')).data;
export const fetchWeekly = async (week?: string) => (await api.get('/reports/weekly', { params: { week } })).data;
export const fetchAlerts = async () => (await api.get('/alerts')).data;
export const createTestAlert = async () => (await api.post('/alerts/test')).data;
export const fetchCalibrations = async () => (await api.get('/calibrations')).data;
export const createCalibration = async (payload: { device_id: string, offset: number, note?: string }) => (await api.post('/calibrations', payload)).data;
export const uploadMenuCsv = async (file: File) => {
  const form = new FormData();
  form.append('file', file);
  const res = await api.post('/uploads/menus', form, { headers: { 'Content-Type': 'multipart/form-data' } });
  return res.data as { items_ingested: number };
};

export const fetchRoiSummary = async () => (await api.get('/reports/roi')).data;

// --- Billing ---
export const fetchBillingPrices = async () => (await api.get('/billing/prices')).data;
export const fetchBillingStatus = async () => (await api.get('/billing/status')).data;
export const fetchBillingPortal = async () => (await api.get('/billing/portal')).data;
