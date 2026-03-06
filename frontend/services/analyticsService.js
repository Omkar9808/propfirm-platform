// Analytics Service
import apiRequest from './api';

export const getDashboardAnalytics = async (accountId) => {
  return await apiRequest(`/analytics/dashboard/${accountId}`);
};

export const getPerformanceMetrics = async (accountId) => {
  return await apiRequest(`/analytics/performance/${accountId}`);
};

export const getRiskMetrics = async (accountId) => {
  return await apiRequest(`/analytics/risk/${accountId}`);
};

export default {
  getDashboardAnalytics,
  getPerformanceMetrics,
  getRiskMetrics,
};
