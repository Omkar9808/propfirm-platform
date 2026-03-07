/* ========================================
   Dashboard Dummy Data System
   Easy to replace with backend API calls
   ======================================== */

const dashboardData = {
    // Account Overview Data
    account: {
        id: '#12345',
        name: 'Account #12345 - $10K Challenge',
        balance: 10000,
        equity: 10420,
        profitTarget: 8, // percentage
        dailyLossLimit: 5, // percentage
        maxDrawdown: 10, // percentage
        minimumTradingDays: 5,
        currentTradingDays: 3,
        phase: 'Phase 1',
        challengeType: '$10K Challenge'
    },

    // Trading Analytics Data
    analytics: {
        totalTrades: 47,
        winRate: 68,
        averageRR: '1:2.3',
        profitFactor: 2.15,
        largestWin: 450,
        largestLoss: 180,
        wins: 32,
        losses: 15
    },

    // Equity Curve Data (for Chart.js)
    equityCurve: {
        labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        data: [10000, 10120, 10250, 10180, 10420, 10380, 10420]
    },

    // Win Rate Distribution
    winRateDistribution: {
        wins: 68,
        losses: 32
    },

    // Recent Trades Data
    recentTrades: [
        {
            id: 1,
            date: '2026-03-07',
            pair: 'EURUSD',
            direction: 'BUY',
            lotSize: 0.5,
            entry: 1.0850,
            exit: 1.0870,
            profit: 120,
            rr: '1:2',
            status: 'Closed',
            notes: 'BOS entry on H1'
        },
        {
            id: 2,
            date: '2026-03-06',
            pair: 'GBPUSD',
            direction: 'SELL',
            lotSize: 0.3,
            entry: 1.2650,
            exit: 1.2680,
            profit: -60,
            rr: '1:1',
            status: 'Closed',
            notes: 'Stopped out'
        },
        {
            id: 3,
            date: '2026-03-05',
            pair: 'XAUUSD',
            direction: 'BUY',
            lotSize: 0.2,
            entry: 2035.50,
            exit: 2045.80,
            profit: 210,
            rr: '1:3',
            status: 'Closed',
            notes: 'Perfect breakout'
        },
        {
            id: 4,
            date: '2026-03-04',
            pair: 'USDJPY',
            direction: 'SELL',
            lotSize: 0.4,
            entry: 149.50,
            exit: 149.20,
            profit: 95,
            rr: '1:1.5',
            status: 'Closed',
            notes: 'Resistance rejection'
        },
        {
            id: 5,
            date: '2026-03-03',
            pair: 'AUDUSD',
            direction: 'BUY',
            lotSize: 0.25,
            entry: 0.6520,
            exit: 0.6540,
            profit: 75,
            rr: '1:2',
            status: 'Closed',
            notes: 'Trend continuation'
        }
    ],

    // Leaderboard Data
    leaderboard: [
        {
            rank: 1,
            trader: 'TradingMaster',
            profit: 12.5,
            winRate: 78,
            trades: 156,
            avatar: null
        },
        {
            rank: 2,
            trader: 'ForexKing',
            profit: 9.8,
            winRate: 72,
            trades: 203,
            avatar: null
        },
        {
            rank: 3,
            trader: 'RiskTaker',
            profit: 8.2,
            winRate: 65,
            trades: 189,
            avatar: null
        },
        {
            rank: 4,
            trader: 'PipHunter',
            profit: 7.9,
            winRate: 69,
            trades: 142,
            avatar: null
        },
        {
            rank: 5,
            trader: 'MarketWizard',
            profit: 6.5,
            winRate: 71,
            trades: 178,
            avatar: null
        }
    ],

    // Challenge Progress Data
    challengeProgress: {
        profitTarget: {
            current: 70,
            target: 100,
            percentage: 70
        },
        dailyDrawdown: {
            current: 20,
            limit: 100,
            percentage: 20
        },
        maxDrawdown: {
            current: 15,
            limit: 100,
            percentage: 15
        },
        tradingDays: {
            current: 3,
            required: 5,
            percentage: 60
        }
    },

    // Account Settings Data
    userSettings: {
        name: 'John Doe',
        email: 'john.doe@example.com',
        phone: '+1 234 567 8900',
        country: 'United States',
        timezone: 'UTC-5 (EST)'
    },

    // Support FAQ Data
    faqData: [
        {
            question: 'How do I request a payout?',
            answer: 'Navigate to the Payout section in your dashboard and submit a withdrawal request. Payouts are processed within 24-48 hours.'
        },
        {
            question: 'What is the maximum lot size?',
            answer: 'The maximum lot size varies by account type. For $10K accounts, it\'s 3.0 lots. For larger accounts, it scales proportionally.'
        },
        {
            question: 'Can I hold trades over the weekend?',
            answer: 'Yes, you can hold trades over the weekend. However, ensure you have sufficient margin to cover any potential gaps.'
        },
        {
            question: 'How do I upgrade my account?',
            answer: 'Once you reach your profit target, you become eligible for an account upgrade. Contact support to initiate the process.'
        }
    ]
};

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
}

// Helper function to format percentage
function formatPercentage(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2
    }).format(value / 100);
}

// Export for use in other files (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = dashboardData;
}
