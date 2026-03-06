import React from 'react';
import { motion } from 'framer-motion';
import { useAccount } from '../AccountContext';

const MetricCard = ({ icon, title, value, subtext, progressValue, progressColor, delay }) => {
  return (
    <motion.div
      className="summary-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.02, y: -4 }}
    >
      <div className="card-header">
        <h3>
          <i className={`${icon} ${progressColor || 'text-green-400'}`}></i> {title}
        </h3>
      </div>
      <div className={`card-value text-3xl font-bold ${value.includes('-') ? 'text-red-400' : 'text-green-400'}`}>
        {value}
      </div>
      {subtext && <div className="card-status text-sm">{subtext}</div>}
      {progressValue !== undefined && (
        <div className="mt-3">
          <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
            <motion.div
              className={`h-2 rounded-full ${progressColor ? progressColor.replace('text-', 'bg-') : 'bg-gradient-to-r from-green-400 to-cyan-400'}`}
              initial={{ width: 0 }}
              animate={{ width: `${progressValue}%` }}
              transition={{ duration: 1, delay: delay + 0.3 }}
            />
          </div>
        </div>
      )}
    </motion.div>
  );
};

export const PerformanceAnalytics = () => {
  const { selectedAccount, isUpdating } = useAccount();

  return (
    <>
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
        <i className="fas fa-chart-bar text-green-400"></i>
        Performance Analytics
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard
          icon="fas fa-dollar-sign"
          title="Current Balance"
          value={`$${selectedAccount.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
          subtext="Initial Capital"
          delay={0.5}
        />

        <MetricCard
          icon="fas fa-chart-line"
          title="Current Equity"
          value={`$${selectedAccount.equity.toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
          subtext={
            <div className="flex items-center gap-2">
              <span className={selectedAccount.floatingPnL >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                {selectedAccount.floatingPnL >= 0 ? '▲' : '▼'} ${Math.abs(selectedAccount.floatingPnL).toFixed(2)}
              </span>
              <span>({(selectedAccount.performanceChange).toFixed(2)}%)</span>
            </div>
          }
          progressValue={(selectedAccount.equity / selectedAccount.accountSize) * 100}
          delay={0.6}
        />

        <MetricCard
          icon="fas fa-coins"
          title="Floating P&L"
          value={`${selectedAccount.floatingPnL >= 0 ? '+' : ''}$${selectedAccount.floatingPnL.toFixed(2)}`}
          subtext="Open Positions P&L"
          progressValue={Math.abs((selectedAccount.floatingPnL / selectedAccount.accountSize) * 100)}
          progressColor={selectedAccount.floatingPnL >= 0 ? 'text-green-400' : 'text-red-400'}
          delay={0.7}
        />
      </div>
    </>
  );
};
