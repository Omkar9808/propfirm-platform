import React from 'react';
import { motion } from 'framer-motion';
import { useAccount } from '../AccountContext';

const TraderMetricCard = ({ icon, title, value, subtext, color, delay }) => {
  const colorClasses = {
    blue: 'text-blue-400',
    cyan: 'text-cyan-400',
    yellow: 'text-yellow-400',
    orange: 'text-orange-400',
    pink: 'text-pink-400',
    purple: 'text-purple-400'
  };

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
          <i className={`${icon} ${colorClasses[color] || 'text-green-400'}`}></i> {title}
        </h3>
      </div>
      <div className="card-value text-3xl font-bold text-green-400">{value}</div>
      {subtext && <div className="card-status text-sm">{subtext}</div>}
    </motion.div>
  );
};

export const AdvancedTraderMetrics = () => {
  const { selectedAccount } = useAccount();

  return (
    <>
      <h2 className="text-2xl font-bold mb-6 mt-8 flex items-center gap-3">
        <i className="fas fa-brain text-purple-400"></i>
        Trader Performance Metrics
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <TraderMetricCard
          icon="fas fa-percentage"
          title="Win Rate"
          value={`${selectedAccount.winRate}%`}
          subtext={
            <span>
              <span className="text-gray-400">{selectedAccount.wins}W / </span>
              <span className="text-gray-400">{selectedAccount.losses}L</span>
            </span>
          }
          color="blue"
          delay={1.2}
        />

        <TraderMetricCard
          icon="fas fa-chart-pie"
          title="Profit Factor"
          value={selectedAccount.profitFactor.toFixed(2)}
          subtext="Gross Profit / Gross Loss"
          color="cyan"
          delay={1.3}
        />

        <TraderMetricCard
          icon="fas fa-star"
          title="Discipline Score"
          value={
            <span>
              {selectedAccount.disciplineScore}
              <span className="text-lg text-gray-400">/100</span>
            </span>
          }
          subtext={
            selectedAccount.disciplineScore >= 80 ? (
              "Excellent risk management"
            ) : selectedAccount.disciplineScore >= 60 ? (
              "Good discipline"
            ) : (
              "Needs improvement"
            )
          }
          color="yellow"
          delay={1.4}
        />

        <TraderMetricCard
          icon="fas fa-bolt"
          title="Avg Trade Duration"
          value={
            <span>
              {selectedAccount.avgTradeDuration}
              <span className="text-lg text-gray-400"> hrs</span>
            </span>
          }
          subtext="Swing trading style"
          color="orange"
          delay={1.5}
        />

        <TraderMetricCard
          icon="fas fa-coins"
          title="Profit per Trade"
          value={`$${selectedAccount.profitPerTrade.toFixed(2)}`}
          subtext="Average winning trade"
          color="pink"
          delay={1.6}
        />
      </div>
    </>
  );
};
