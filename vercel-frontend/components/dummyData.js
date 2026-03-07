/**
 * Simple Dummy Data for Dashboard
 * Embedded directly for performance
 */

const dashboardData = {
    account: {
        balance: 10000,
        equity: 10420,
        profitTarget: 8,
        dailyLossLimit: 5,
        maxDrawdown: 10
    },
    
    recentTrades: [
        { date: '2026-03-07', pair: 'EURUSD', direction: 'BUY', lotSize: 0.5, profit: 120, rr: '1:2' },
        { date: '2026-03-06', pair: 'GBPUSD', direction: 'SELL', lotSize: 0.3, profit: -60, rr: '1:1' },
        { date: '2026-03-05', pair: 'XAUUSD', direction: 'BUY', lotSize: 0.2, profit: 210, rr: '1:3' }
    ],
    
    analytics: {
        totalTrades: 47,
        winRate: 68,
        averageRR: '1:2.3',
        profitFactor: 2.15,
        largestWin: 450,
        largestLoss: 180
    },
    
    leaderboard: [
        { trader: 'TradingMaster', profit: 12, winRate: 78 },
        { trader: 'ForexKing', profit: 9, winRate: 72 },
        { trader: 'RiskTaker', profit: 8, winRate: 65 }
    ]
};
