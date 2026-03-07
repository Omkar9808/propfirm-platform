import React from 'react';
import { motion } from 'framer-motion';

const Topbar = ({ toggleSidebar, toggleMobileMenu, account }) => {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatPercent = (value) => {
    return `${value.toFixed(2)}%`;
  };

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="sticky top-0 z-20 bg-[#0a0a0c]/95 backdrop-blur-sm border-b border-white/10"
    >
      <div className="px-6 py-4">
        {/* Top Bar - Account Info */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            {/* Mobile Menu Toggle */}
            <button
              onClick={toggleMobileMenu}
              className="lg:hidden text-gray-400 hover:text-white transition-colors"
            >
              <i className="fas fa-bars text-xl"></i>
            </button>

            {/* Desktop Sidebar Toggle */}
            <button
              onClick={toggleSidebar}
              className="hidden lg:block text-gray-400 hover:text-white transition-colors"
            >
              <i className={`fas ${account.sidebarOpen ? 'fa-chevron-left' : 'fa-bars'} text-lg`}></i>
            </button>

            {/* Account Selector */}
            <div className="flex items-center gap-3">
              <select
                value={account.id}
                onChange={(e) => account.switchAccount(e.target.value)}
                className="bg-gray-900 border border-gray-800 rounded-lg px-4 py-2 text-sm focus:border-[#00ff9d] focus:outline-none transition-colors cursor-pointer"
              >
                {Object.entries(account.accounts).map(([key, acc]) => (
                  <option key={key} value={key}>{acc.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* User Info */}
          <div className="flex items-center gap-4">
            {/* Notifications */}
            <button className="relative text-gray-400 hover:text-white transition-colors">
              <i className="fas fa-bell text-xl"></i>
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs flex items-center justify-center">
                3
              </span>
            </button>

            {/* Profile Avatar */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#00ff9d] to-[#0ea5e9] flex items-center justify-center text-black font-bold">
                JD
              </div>
              <span className="hidden md:block font-medium">John Doe</span>
            </div>
          </div>
        </div>

        {/* Key Metrics Bar */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 pt-4 border-t border-white/10">
          {/* Balance */}
          <div className="text-center">
            <div className="text-xs text-gray-400 mb-1">Balance</div>
            <div className="text-lg font-bold text-white">{formatCurrency(account.balance)}</div>
          </div>

          {/* Daily Drawdown */}
          <div className="text-center">
            <div className="text-xs text-gray-400 mb-1">Daily DD</div>
            <div className="text-lg font-bold text-[#00ff9d]">{formatCurrency(account.maxDailyLoss - account.dailyLoss)}</div>
          </div>

          {/* Max Drawdown */}
          <div className="text-center">
            <div className="text-xs text-gray-400 mb-1">Max DD</div>
            <div className="text-lg font-bold text-[#0ea5e9]">{formatCurrency(account.maxDrawdown - account.drawdown)}</div>
          </div>

          {/* Profit Target */}
          <div className="text-center">
            <div className="text-xs text-gray-400 mb-1">Profit Target</div>
            <div className="text-lg font-bold text-[#fbbf24]">{formatPercent(((account.profit / account.profitTarget) * 100))}</div>
          </div>

          {/* Phase */}
          <div className="text-center col-span-2 md:col-span-1 lg:col-span-1">
            <div className="text-xs text-gray-400 mb-1">Phase</div>
            <div className="inline-block px-3 py-1 bg-gradient-to-r from-[#00ff9d]/20 to-[#0ea5e9]/20 rounded-full text-sm font-semibold text-[#00ff9d]">
              {account.status}
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  );
};

export default Topbar;
