/**
 * Main Dashboard JavaScript
 * Handles dashboard initialization, data loading, and interactions
 */

// Mock data for demonstration (will be replaced by backend API calls)
const mockAccountData = {
    account1: {
        id: '#12345',
        name: 'Account #12345 - $10K Challenge',
        balance: 10245.00,
        equity: 10310.00,
        dailyLossLimit: 500.00,
        maxDrawdown: 1000.00,
        profitTarget: 1000.00,
        profitProgress: 70,
        winRate: 78,
        wins: 18,
        losses: 5,
        recentTrades: [
            { date: '2026-03-07', pair: 'EURUSD', direction: 'BUY', lotSize: 0.5, profit: 120, rr: '1:2', status: 'Closed' },
            { date: '2026-03-06', pair: 'GBPUSD', direction: 'SELL', lotSize: 0.3, profit: -85, rr: '1:1.5', status: 'Closed' },
            { date: '2026-03-06', pair: 'USDJPY', direction: 'BUY', lotSize: 0.4, profit: 95, rr: '1:2', status: 'Closed' },
            { date: '2026-03-05', pair: 'XAUUSD', direction: 'SELL', lotSize: 0.2, profit: 150, rr: '1:3', status: 'Closed' },
            { date: '2026-03-04', pair: 'AUDUSD', direction: 'BUY', lotSize: 0.6, profit: -45, rr: '1:1', status: 'Closed' }
        ]
    },
    account2: {
        id: '#67890',
        name: 'Account #67890 - $25K Challenge',
        balance: 25680.00,
        equity: 25720.00,
        dailyLossLimit: 1250.00,
        maxDrawdown: 2500.00,
        profitTarget: 2000.00,
        profitProgress: 65,
        winRate: 82,
        wins: 23,
        losses: 5,
        recentTrades: []
    },
    account3: {
        id: '#11111',
        name: 'Account #11111 - $5K Challenge',
        balance: 5120.00,
        equity: 5095.00,
        dailyLossLimit: 250.00,
        maxDrawdown: 500.00,
        profitTarget: 400.00,
        profitProgress: 45,
        winRate: 65,
        wins: 11,
        losses: 6,
        recentTrades: []
    }
};

/**
 * Initialize dashboard when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 600,
            easing: 'ease-out-cubic',
            once: true
        });
    }
    
    // Load initial data
    loadDashboardData('account1');
    
    // Setup account selector
    setupAccountSelector();
    
    // Load recent trades
    loadRecentTrades(mockAccountData.account1.recentTrades);
    
    // Remove loading screen
    setTimeout(() => {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }
    }, 1000);
});

/**
 * Load dashboard data for selected account
 * @param {string} accountId - Account identifier
 */
function loadDashboardData(accountId) {
    const account = mockAccountData[accountId];
    
    if (!account) {
        console.error('Account not found:', accountId);
        return;
    }
    
    // Update statistics
    updateAccountStats(account);
    
    // Update charts
    updateCharts(account);
    
    // Update progress bars
    updateProgressBars(account);
    
    // Update win rate chart
    if (typeof updateWinRateChart === 'function') {
        updateWinRateChart(account.wins, account.losses);
    }
}

/**
 * Setup account selector dropdown
 */
function setupAccountSelector() {
    const selector = document.getElementById('account-selector');
    
    if (!selector) return;
    
    selector.addEventListener('change', function(e) {
        const accountId = e.target.value;
        loadDashboardData(accountId);
        
        // Show notification
        showNotification(`Switched to ${mockAccountData[accountId].name}`, 'success');
    });
}

/**
 * Update charts with account data
 * @param {Object} account - Account data
 */
function updateCharts(account) {
    // Generate sample equity curve data based on account balance
    const days = 7;
    const labels = [];
    const equityData = [];
    
    const baseBalance = account.balance;
    const variation = baseBalance * 0.02; // 2% variation
    
    for (let i = 0; i < days; i++) {
        labels.push(`Day ${i + 1}`);
        const randomVariation = (Math.random() - 0.4) * variation;
        equityData.push(baseBalance + randomVariation);
    }
    
    // Update equity chart if function exists
    if (typeof updateEquityChart === 'function') {
        updateEquityChart(equityData, labels);
    }
}

/**
 * Update progress bars with account data
 * @param {Object} account - Account data
 */
function updateProgressBars(account) {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach((bar, index) => {
        const percentages = [
            account.profitProgress,
            ((account.dailyLossLimit - 100) / account.dailyLossLimit) * 100,
            ((account.maxDrawdown - 200) / account.maxDrawdown) * 100,
            50 // Trading days placeholder
        ];
        
        if (percentages[index]) {
            animateProgressBar(bar, percentages[index]);
        }
    });
}

/**
 * Load recent trades into table
 * @param {Array} trades - Array of trade objects
 */
function loadRecentTrades(trades) {
    const tbody = document.getElementById('recent-trades-body');
    
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    trades.forEach((trade, index) => {
        const row = document.createElement('tr');
        row.className = 'border-b border-gray-700 hover:bg-white/5 transition-colors';
        row.style.animationDelay = `${index * 0.1}s`;
        
        const profitClass = trade.profit >= 0 ? 'text-green-400' : 'text-red-400';
        const profitSign = trade.profit >= 0 ? '+' : '';
        
        const directionClass = trade.direction === 'BUY' ? 'text-green-400' : 'text-red-400';
        
        row.innerHTML = `
            <td class="py-3 pr-4 text-sm">${formatDate(trade.date)}</td>
            <td class="py-3 pr-4 font-medium">${trade.pair}</td>
            <td class="py-3 pr-4">
                <span class="${directionClass} px-2 py-1 rounded text-xs font-semibold">${trade.direction}</span>
            </td>
            <td class="py-3 pr-4 text-sm">${trade.lotSize}</td>
            <td class="py-3 pr-4 ${profitClass} font-semibold">${profitSign}$${trade.profit}</td>
            <td class="py-3 pr-4 text-sm text-gray-400">${trade.rr}</td>
            <td class="py-3">
                <span class="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs font-semibold">${trade.status}</span>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

/**
 * Format date for display
 * @param {string} dateString - Date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { month: 'short', day: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

/**
 * Refresh dashboard data
 */
function refreshDashboard() {
    const accountId = document.getElementById('account-selector').value;
    loadDashboardData(accountId);
    showNotification('Dashboard refreshed', 'success');
}

// Make functions available globally
window.loadDashboardData = loadDashboardData;
window.refreshDashboard = refreshDashboard;
