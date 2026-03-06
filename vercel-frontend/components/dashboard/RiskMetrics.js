import React from 'react';
import { motion } from 'framer-motion';
import { useAccount } from '../AccountContext';

const RiskCard = ({ icon, title, currentValue, limitValue, percentageUsed, colorScheme, subtext, delay }) => {
  const colorClasses = {
    green: { bar: 'from-green-400 to-cyan-400', text: 'text-green-400', icon: 'text-green-400' },
    yellow: { bar: 'from-yellow-400 to-orange-400', text: 'text-yellow-400', icon: 'text-yellow-400' },
    red: { bar: 'from-red-400 to-orange-400', text: 'text-red-400', icon: 'text-red-400' },
    cyan: { bar: 'from-cyan-400 to-blue-400', text: 'text-cyan-400', icon: 'text-cyan-400' }
  };

  const colors = colorClasses[colorScheme] || colorClasses.green;

  return (
    <motion.div
      className="summary-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.02, y: -4 }}
    >
      <div className="card-header mb-4">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <i className={`${icon} ${colors.icon}`}></i>
          {title}
        </h3>
        <span className={`text-2xl font-bold ${colors.text} ml-auto`}>{percentageUsed}% used</span>
      </div>
      <div className="mb-3">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-gray-400">{currentValue}</span>
          <span className="text-gray-400">Limit: {limitValue}</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-4 overflow-hidden">
          <motion.div
            className={`h-4 rounded-full bg-gradient-to-r ${colors.bar} shadow-lg`}
            initial={{ width: 0 }}
            animate={{ width: `${percentageUsed}%` }}
            transition={{ duration: 1, delay: delay + 0.3 }}
          />
        </div>
      </div>
      {subtext && <div className={`text-xs ${colors.text}`}>{subtext}</div>}
    </motion.div>
  );
};

export const RiskMetrics = () => {
  const { selectedAccount } = useAccount();

  const profitTargetPercent = (selectedAccount.profit / selectedAccount.profitTarget) * 100;
  const dailyLossPercent = (selectedAccount.dailyLoss / selectedAccount.maxDailyLoss) * 100;
  const drawdownPercent = (selectedAccount.drawdown / selectedAccount.maxDrawdown) * 100;

  return (
    <>
      <h2 className="text-2xl font-bold mb-6 mt-8 flex items-center gap-3">
        <i className="fas fa-shield-alt text-yellow-400"></i>
        Risk & Progress Indicators
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <RiskCard
          icon="fas fa-bullseye"
          title="Profit Target Progress"
          currentValue={`$${selectedAccount.profit}`}
          limitValue={`$${selectedAccount.profitTarget} (${selectedAccount.profitTargetPercent}%)`}
          percentageUsed={profitTargetPercent}
          colorScheme="green"
          subtext={profitTargetPercent >= 100 ? "🎉 Target reached!" : "You're making good progress! Keep it up."}
          delay={0.8}
        />

        <RiskCard
          icon="fas fa-shield-alt"
          title="Daily Loss Monitor"
          currentValue={`$${selectedAccount.dailyLoss}`}
          limitValue={`$${selectedAccount.maxDailyLoss} (5%)`}
          percentageUsed={dailyLossPercent}
          colorScheme={dailyLossPercent > 80 ? 'yellow' : 'green'}
          subtext={`Safe - $${(selectedAccount.maxDailyLoss - selectedAccount.dailyLoss).toFixed(0)} remaining today`}
          delay={0.9}
        />

        <RiskCard
          icon="fas fa-chart-area"
          title="Maximum Drawdown"
          currentValue={`$${selectedAccount.drawdown}`}
          limitValue={`$${selectedAccount.maxDrawdown} (10%)`}
          percentageUsed={drawdownPercent}
          colorScheme={drawdownPercent > 80 ? 'yellow' : 'cyan'}
          subtext={drawdownPercent < 50 ? "Healthy drawdown level" : "Warning: Approaching drawdown limit"}
          delay={1.0}
        />

        <RuleComplianceCard delay={1.1} />
      </div>
    </>
  );
};

const RuleComplianceCard = ({ delay }) => {
  const { selectedAccount } = useAccount();

  return (
    <motion.div
      className="summary-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ scale: 1.02, y: -4 }}
    >
      <div className="card-header mb-4">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <i className="fas fa-clipboard-check text-purple-400"></i>
          Rule Compliance Status
        </h3>
        <span className="text-2xl font-bold text-green-400 ml-auto">
          {Object.values(selectedAccount.ruleCompliance).every(v => v) ? '100%' : 'Warning'}
        </span>
      </div>
      <div className="space-y-3">
        <div className="flex items-center justify-between p-3 bg-gray-900/50 rounded-lg">
          <span className="text-sm">Minimum Trading Days</span>
          <span className={`font-semibold flex items-center gap-2 ${selectedAccount.ruleCompliance.minTradingDays ? 'text-green-400' : 'text-red-400'}`}>
            {selectedAccount.ruleCompliance.minTradingDays ? (
              <><i className="fas fa-check-circle"></i> Compliant</>
            ) : (
              <><i className="fas fa-exclamation-circle"></i> Not Met</>
            )}
          </span>
        </div>
        <div className="flex items-center justify-between p-3 bg-gray-900/50 rounded-lg">
          <span className="text-sm">Daily Loss Limit</span>
          <span className={`font-semibold flex items-center gap-2 ${selectedAccount.ruleCompliance.dailyLossLimit ? 'text-green-400' : 'text-red-400'}`}>
            {selectedAccount.ruleCompliance.dailyLossLimit ? (
              <><i className="fas fa-check-circle"></i> Safe</>
            ) : (
              <><i className="fas fa-exclamation-circle"></i> Violated</>
            )}
          </span>
        </div>
        <div className="flex items-center justify-between p-3 bg-gray-900/50 rounded-lg">
          <span className="text-sm">Max Drawdown</span>
          <span className={`font-semibold flex items-center gap-2 ${selectedAccount.ruleCompliance.maxDrawdown ? 'text-green-400' : 'text-red-400'}`}>
            {selectedAccount.ruleCompliance.maxDrawdown ? (
              <><i className="fas fa-check-circle"></i> Safe</>
            ) : (
              <><i className="fas fa-exclamation-circle"></i> Violated</>
            )}
          </span>
        </div>
      </div>
    </motion.div>
  );
};
