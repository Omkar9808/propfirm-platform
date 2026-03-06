// Account Service
import apiRequest from './api';

export const getAccounts = async () => {
  return await apiRequest('/accounts');
};

export const getAccountById = async (accountId) => {
  return await apiRequest(`/accounts/${accountId}`);
};

export const getAccountPerformance = async (accountId) => {
  return await apiRequest(`/accounts/${accountId}/performance`);
};

export default {
  getAccounts,
  getAccountById,
  getAccountPerformance,
};
