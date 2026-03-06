import React from 'react';
import { motion } from 'framer-motion';
import { useAccount } from '../../contexts/AccountContext';

const sampleTrades = [
  { ticket: '#1234567', symbol: 'EURUSD', lot: 0.1, profit: 23.45, time: '10:23:45' },
  { ticket: '#1234566', symbol: 'GBPUSD', lot: 0.1, profit: -12.34, time: '09:45:12' },
  { ticket: '#1234565', symbol: 'USDJPY', lot: 0.2, profit: 34.56, time: '08:32:10' },
  { ticket: '#1234564', symbol: 'AUDUSD', lot: 0.1, profit: 8.90, time: '07:15:22' },
  { ticket: '#1234563', symbol: 'USDCAD', lot: 0.1, profit: -5.67, time: '06:45:33' }
];

export const RecentTradesTable = () => {
  const { selectedAccount } = useAccount();

  return (
    <motion.div
      className="summary-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 1.9 }}
    >
      <div className="card-header mb-4">
        <h3 className="text-lg font-bold flex items-center gap-2">
          <i className="fas fa-history text-blue-400"></i>
          Recent Trading Activity
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="border-b border-gray-800 text-gray-400 text-sm">
            <tr>
              <th className="py-3 px-4">Ticket</th>
              <th className="py-3 px-4">Symbol</th>
              <th className="py-3 px-4">Lot</th>
              <th className="py-3 px-4">Profit</th>
              <th className="py-3 px-4">Time</th>
            </tr>
          </thead>
          <tbody>
            {sampleTrades.map((trade, index) => (
              <motion.tr
                key={trade.ticket}
                className="border-t border-gray-800 hover:bg-gray-900/50 transition-colors"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 2.0 + (index * 0.1) }}
              >
                <td className="py-4 px-4 text-sm">{trade.ticket}</td>
                <td className="py-4 px-4">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{trade.symbol}</span>
                  </div>
                </td>
                <td className="py-4 px-4 text-sm text-gray-400">{trade.lot}</td>
                <td className={`py-4 px-4 font-semibold ${trade.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {trade.profit >= 0 ? '+' : ''}${Math.abs(trade.profit).toFixed(2)}
                </td>
                <td className="py-4 px-4 text-sm text-gray-400">{trade.time}</td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};
