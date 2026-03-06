import React from 'react';
import { motion } from 'framer-motion';
import { useAccount } from '../../contexts/AccountContext';

const OverviewCard = ({ icon, title, value, subtext, delay }) => {
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
          <i className={`${icon} text-green-400`}></i> {title}
        </h3>
      </div>
      <div className="card-value text-2xl font-bold">{value}</div>
      {subtext && <div className="card-status text-sm">{subtext}</div>}
    </motion.div>
  );
};

export const AccountOverviewCards = () => {
  const { selectedAccount, isUpdating } = useAccount();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <OverviewCard
        icon="fas fa-hashtag"
        title="Account ID"
        value={selectedAccount.id}
        subtext={
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-400 rounded-full pulse-glow"></span>
            <span>{selectedAccount.status}</span>
          </div>
        }
        delay={0.1}
      />

      <OverviewCard
        icon="fas fa-chart-line"
        title="Performance Status"
        value={
          <span className={selectedAccount.performanceChange >= 0 ? 'text-green-400' : 'text-red-400'}>
            {selectedAccount.performanceStatus}
          </span>
        }
        subtext={
          <div className="flex items-center gap-2">
            <span className={selectedAccount.performanceChange >= 0 ? 'text-emerald-400' : 'text-red-400'}>
              {selectedAccount.performanceChange >= 0 ? '▲' : '▼'} {Math.abs(selectedAccount.performanceChange)}%
            </span>
            <span>this period</span>
          </div>
        }
        delay={0.2}
      />

      <OverviewCard
        icon="fas fa-calendar-check"
        title="Trading Days"
        value={
          <span>
            {selectedAccount.tradingDays}
            <span className="text-sm text-gray-400">/{selectedAccount.minTradingDays}</span>
          </span>
        }
        subtext={
          <div>
            <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
              <motion.div
                className="bg-gradient-to-r from-green-400 to-cyan-400 h-2 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${(selectedAccount.tradingDays / selectedAccount.minTradingDays) * 100}%` }}
                transition={{ duration: 1, delay: 0.5 }}
              />
            </div>
            <span className="text-xs">min required</span>
          </div>
        }
        delay={0.3}
      />

      <OverviewCard
        icon="fas fa-stopwatch"
        title="Challenge Timeline"
        value={
          <span>
            Day {selectedAccount.dayNumber}
            <span className="text-sm text-gray-400"> of {selectedAccount.totalDays}</span>
          </span>
        }
        subtext={
          <span className="text-cyan-400">
            {selectedAccount.totalDays - selectedAccount.dayNumber} days remaining
          </span>
        }
        delay={0.4}
      />
    </div>
  );
};
