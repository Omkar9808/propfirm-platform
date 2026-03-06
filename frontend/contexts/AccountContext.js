import React, { createContext, useContext, useState, useEffect } from 'react';

const AccountContext = createContext();

export const useAccount = () => {
  const context = useContext(AccountContext);
  if (!context) {
    throw new Error('useAccount must be used within AccountProvider');
  }
  return context;
};

// Sample account data - in production, this would come from an API
const accountsData = {
  account1: {
    id: '#12345',
    name: 'Account #12345 - $5K Challenge',
    accountSize: 5000,
    balance: 5000.00,
    equity: 5123.45,
    floatingPnL: 123.45,
    profit: 247,
    profitTarget: 800,
    profitTargetPercent: 8,
    dailyLoss: 115,
    maxDailyLoss: 250,
    drawdown: 90,
    maxDrawdown: 500,
    tradingDays: 7,
    minTradingDays: 10,
    startDate: 'Mar 1, 2026',
    dayNumber: 7,
    totalDays: 30,
    status: 'Active Phase 1',
    performanceStatus: 'Profitable',
    performanceChange: 2.47,
    winRate: 78,
    wins: 18,
    losses: 5,
    profitFactor: 2.34,
    disciplineScore: 87,
    avgTradeDuration: 4.2,
    profitPerTrade: 53.42,
    ruleCompliance: {
      minTradingDays: true,
      dailyLossLimit: true,
      maxDrawdown: true
    }
  },
  account2: {
    id: '#67890',
    name: 'Account #67890 - $10K Challenge',
    accountSize: 10000,
    balance: 10000.00,
    equity: 10345.80,
    floatingPnL: 345.80,
    profit: 545,
    profitTarget: 800,
    profitTargetPercent: 8,
    dailyLoss: 85,
    maxDailyLoss: 500,
    drawdown: 150,
    maxDrawdown: 1000,
    tradingDays: 12,
    minTradingDays: 10,
    startDate: 'Feb 15, 2026',
    dayNumber: 12,
    totalDays: 30,
    status: 'Active Phase 1',
    performanceStatus: 'Profitable',
    performanceChange: 3.46,
    winRate: 82,
    wins: 23,
    losses: 5,
    profitFactor: 3.12,
    disciplineScore: 92,
    avgTradeDuration: 3.8,
    profitPerTrade: 67.89,
    ruleCompliance: {
      minTradingDays: true,
      dailyLossLimit: true,
      maxDrawdown: true
    }
  },
  account3: {
    id: '#11111',
    name: 'Account #11111 - $25K Challenge',
    accountSize: 25000,
    balance: 25000.00,
    equity: 24875.50,
    floatingPnL: -124.50,
    profit: -124.50,
    profitTarget: 2000,
    profitTargetPercent: 8,
    dailyLoss: 124.50,
    maxDailyLoss: 1250,
    drawdown: 250,
    maxDrawdown: 2500,
    tradingDays: 5,
    minTradingDays: 10,
    startDate: 'Mar 5, 2026',
    dayNumber: 5,
    totalDays: 30,
    status: 'Active Phase 1',
    performanceStatus: 'Negative',
    performanceChange: -0.50,
    winRate: 45,
    wins: 5,
    losses: 6,
    profitFactor: 0.85,
    disciplineScore: 72,
    avgTradeDuration: 5.5,
    profitPerTrade: -45.23,
    ruleCompliance: {
      minTradingDays: false,
      dailyLossLimit: true,
      maxDrawdown: true
    }
  }
};

export const AccountProvider = ({ children }) => {
  const [selectedAccountId, setSelectedAccountId] = useState('account1');
  const [selectedAccount, setSelectedAccount] = useState(accountsData.account1);
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    // Load saved account from localStorage
    const savedAccount = localStorage.getItem('selectedAccount');
    if (savedAccount && accountsData[savedAccount]) {
      setSelectedAccountId(savedAccount);
      setSelectedAccount(accountsData[savedAccount]);
    }
  }, []);

  const switchAccount = (accountId) => {
    if (accountsData[accountId]) {
      setIsUpdating(true);
      setSelectedAccountId(accountId);
      setSelectedAccount(accountsData[accountId]);
      localStorage.setItem('selectedAccount', accountId);
      
      // Simulate loading delay for smooth animation
      setTimeout(() => {
        setIsUpdating(false);
      }, 300);
    }
  };

  const value = {
    selectedAccountId,
    selectedAccount,
    switchAccount,
    accounts: accountsData,
    isUpdating
  };

  return (
    <AccountContext.Provider value={value}>
      {children}
    </AccountContext.Provider>
  );
};
