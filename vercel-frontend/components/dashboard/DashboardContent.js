import React from 'react';
import { motion } from 'framer-motion';
import { useAccount } from './AccountContext';
import { AccountOverviewCards } from './AccountOverviewCards';
import { PerformanceAnalytics } from './PerformanceAnalytics';
import { RiskMetrics } from './RiskMetrics';
import { AdvancedTraderMetrics } from './AdvancedTraderMetrics';
import { ChartsSection } from './ChartsSection';
import { RecentTradesTable } from './RecentTradesTable';

export const DashboardContent = () => {
  const { selectedAccountId, switchAccount, accounts, isUpdating } = useAccount();

  return (
    <motion.div
      className="dashboard-container"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Top Bar with Account Selector */}
      <div className="top-bar mb-8">
        <div className="menu-toggle">
          <i className="fas fa-bars"></i>
        </div>
        <div className="account-selector">
          <select
            id="accountSelect"
            value={selectedAccountId}
            onChange={(e) => switchAccount(e.target.value)}
            className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm focus:border-green-400 focus:outline-none transition-colors"
          >
            {Object.entries(accounts).map(([key, account]) => (
              <option key={key} value={key}>
                {account.name}
              </option>
            ))}
          </select>
        </div>
        <div className="user-info">
          <i className="fas fa-user-circle"></i>
          <span>John Doe</span>
        </div>
      </div>

      {/* Main Dashboard Content */}
      <div className={`transition-opacity duration-300 ${isUpdating ? 'opacity-50' : 'opacity-100'}`}>
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-3">
          <i className="fas fa-home text-green-400"></i>
          Trading Terminal Dashboard
        </h1>

        {/* SECTION 1: Overview Cards */}
        <AccountOverviewCards />

        {/* SECTION 2: Performance Analytics */}
        <PerformanceAnalytics />

        {/* SECTION 3: Risk Metrics */}
        <RiskMetrics />

        {/* SECTION 4: Advanced Trader Metrics */}
        <AdvancedTraderMetrics />

        {/* SECTION 5: Charts */}
        <ChartsSection />

        {/* SECTION 6: Recent Trades */}
        <RecentTradesTable />

        {/* Rule Violations Section */}
        <motion.div
          className="violations-section mt-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 2.0 }}
        >
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <i className="fas fa-shield-alt text-green-400"></i>
            Rule Violations
          </h3>
          <div className="violations-box clean summary-card">
            <i className="fas fa-check-circle text-green-400 text-3xl mb-3"></i>
            <p className="text-gray-300">No violations detected. Keep up the good work!</p>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};
