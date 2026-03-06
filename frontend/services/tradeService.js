// Trade Service
import apiRequest from './api';

export const getRecentTrades = async (accountId, limit = 10) => {
  return await apiRequest(`/trades/${accountId}?limit=${limit}`);
};

export const getTradeHistory = async (accountId, options = {}) => {
  const params = new URLSearchParams(options).toString();
  return await apiRequest(`/trades/${accountId}/history?${params}`);
};

export const getTradingActivity = async (accountId) => {
  return await apiRequest(`/trades/${accountId}/activity`);
};

export default {
  getRecentTrades,
  getTradeHistory,
  getTradingActivity,
};
