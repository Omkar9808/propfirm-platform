/**
 * Main Dashboard JavaScript - COMPLETE REWRITE
 * Handles dashboard initialization, data loading, and dynamic content switching
 */

// Use dummyData from dummyData.js if available, otherwise use fallback
const dashboardDummyData = typeof dashboardData !== 'undefined' ? dashboardData : {
    account: { balance: 10000, equity: 10420, profitTarget: 8, dailyLossLimit: 5, maxDrawdown: 10 },
    recentTrades: [
        { date: '2026-03-07', pair: 'EURUSD', direction: 'BUY', lotSize: 0.5, profit: 120, rr: '1:2' },
        { date: '2026-03-06', pair: 'GBPUSD', direction: 'SELL', lotSize: 0.3, profit: -60, rr: '1:1' },
        { date: '2026-03-05', pair: 'XAUUSD', direction: 'BUY', lotSize: 0.2, profit: 210, rr: '1:3' }
    ],
    analytics: { totalTrades: 47, winRate: 68, averageRR: '1:2.3', profitFactor: 2.15, largestWin: 450, largestLoss: 180 },
    leaderboard: [
        { trader: 'TradingMaster', profit: 12, winRate: 78 },
        { trader: 'ForexKing', profit: 9, winRate: 72 },
        { trader: 'RiskTaker', profit: 8, winRate: 65 }
    ]
};

/**
 * Initialize dashboard when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    
    // Check if required elements exist
    const container = document.getElementById('dashboardContent');
    const loadingScreen = document.getElementById('loading-screen');
    
    if (!container) {
        console.error('ERROR: #dashboardContent container not found in HTML!');
    } else {
        console.log('✓ Container #dashboardContent found');
    }
    
    if (!loadingScreen) {
        console.error('ERROR: #loading-screen element not found in HTML!');
    } else {
        console.log('✓ Loading screen found');
    }
    
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({ duration: 600, easing: 'ease-out-cubic', once: true });
        console.log('✓ AOS initialized');
    }
    
    // Show loader for 800ms then load dashboard
    setTimeout(() => {
        console.log('Loading complete, rendering dashboard...');
        hideLoadingScreen();
        loadDashboardOverview();
    }, 800);
});

/**
 * Hide loading screen
 */
function hideLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.opacity = '0';
        loadingScreen.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 500);
    }
}

/**
 * Load Dashboard Overview - MAIN LANDING PAGE
 */
function loadDashboardOverview() {
    console.log('loadDashboardOverview() called');
    
    const container = document.getElementById('dashboardContent');
    if (!container) {
        console.error('CRITICAL ERROR: Cannot find #dashboardContent container');
        return;
    }
    
    try {
        container.innerHTML = `
            <!-- Welcome Section -->
            <div class="welcome-section mb-6" data-aos="fade-down">
                <h2 class="text-2xl font-bold mb-2">Welcome back, Trader 👋</h2>
                <p class="text-gray-400">Phase 1 Challenge • Account Type: Evaluation</p>
            </div>
            
            <!-- Statistics Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                ${generateBalanceCard()}
                ${generateEquityCard()}
                ${generateDailyLossCard()}
                ${generateProfitTargetCard()}
            </div>
            
            <!-- Charts Section -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div class="bg-secondary rounded-xl p-6 border border-gray-700" data-aos="fade-up">
                    <h3 class="text-lg font-semibold mb-4">Equity Curve</h3>
                    <canvas id="equity-chart" height="200"></canvas>
                </div>
                <div class="bg-secondary rounded-xl p-6 border border-gray-700" data-aos="fade-up" data-aos-delay="100">
                    <h3 class="text-lg font-semibold mb-4">Win Rate Distribution</h3>
                    <canvas id="winrate-chart" height="200"></canvas>
                </div>
            </div>
            
            <!-- Recent Trades Table -->
            <div class="bg-secondary rounded-xl p-6 border border-gray-700" data-aos="fade-up">
                <h3 class="text-lg font-semibold mb-4">Recent Trades</h3>
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead>
                            <tr class="text-left text-sm text-gray-400 border-b border-gray-700">
                                <th class="pb-3 pr-4">Date</th>
                                <th class="pb-3 pr-4">Pair</th>
                                <th class="pb-3 pr-4">Direction</th>
                                <th class="pb-3 pr-4">Lot Size</th>
                                <th class="pb-3 pr-4">Profit/Loss</th>
                                <th class="pb-3 pr-4">R:R</th>
                        </tr>
                    </thead>
                    <tbody id="recent-trades-body">
                        ${generateRecentTradesRows()}
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    console.log('Dashboard content rendered successfully');
    
    // Initialize charts after DOM update
    setTimeout(() => {
        initEquityChart();
        initWinRateChart();
    }, 100);
} catch (error) {
    console.error('ERROR in loadDashboardOverview():', error);
}
}

/**
 * Generate Balance Card HTML
 */
function generateBalanceCard() {
    const balance = dashboardDummyData.account.balance;
    return `
        <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up">
            <div class="flex items-center justify-between mb-3">
                <div class="icon-box w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center">
                    <i class="fas fa-wallet text-blue-400 text-xl"></i>
                </div>
                <div>
                    <p class="text-sm text-gray-400">Account Balance</p>
                    <h3 class="text-2xl font-bold counter" data-target="${balance}">$${balance.toLocaleString()}</h3>
                </div>
            </div>
            <div class="progress-bar bg-gray-700 rounded-full h-2">
                <div class="progress-fill bg-gradient-to-r from-blue-500 to-blue-400 h-full rounded-full" style="width: 100%"></div>
            </div>
        </div>
    `;
}

/**
 * Generate Equity Card HTML
 */
function generateEquityCard() {
    const equity = dashboardDummyData.account.equity;
    return `
        <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="100">
            <div class="flex items-center justify-between mb-3">
                <div class="icon-box w-12 h-12 rounded-lg bg-green-500/20 flex items-center justify-center">
                    <i class="fas fa-chart-line text-green-400 text-xl"></i>
                </div>
                <div>
                    <p class="text-sm text-gray-400">Current Equity</p>
                    <h3 class="text-2xl font-bold counter" data-target="${equity}">$${equity.toLocaleString()}</h3>
                </div>
            </div>
            <div class="progress-bar bg-gray-700 rounded-full h-2">
                <div class="progress-fill bg-gradient-to-r from-green-500 to-green-400 h-full rounded-full" style="width: 100%"></div>
            </div>
        </div>
    `;
}

/**
 * Generate Daily Loss Card HTML
 */
function generateDailyLossCard() {
    const limit = dashboardDummyData.account.dailyLossLimit;
    const amount = -(10000 * (limit / 100));
    return `
        <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="200">
            <div class="flex items-center justify-between mb-3">
                <div class="icon-box w-12 h-12 rounded-lg bg-red-500/20 flex items-center justify-center">
                    <i class="fas fa-arrow-down text-red-400 text-xl"></i>
                </div>
                <div>
                    <p class="text-sm text-gray-400">Daily Loss Limit</p>
                    <h3 class="text-2xl font-bold text-danger">$${amount.toLocaleString()}</h3>
                </div>
            </div>
            <div class="progress-bar bg-gray-700 rounded-full h-2">
                <div class="progress-fill bg-gradient-to-r from-red-500 to-red-400 h-full rounded-full" style="width: 20%"></div>
            </div>
        </div>
    `;
}

/**
 * Generate Profit Target Card HTML
 */
function generateProfitTargetCard() {
    const target = dashboardDummyData.account.profitTarget;
    return `
        <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="300">
            <div class="flex items-center justify-between mb-3">
                <div class="icon-box w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center">
                    <i class="fas fa-bullseye text-purple-400 text-xl"></i>
                </div>
                <div>
                    <p class="text-sm text-gray-400">Profit Target</p>
                    <h3 class="text-2xl font-bold">${target}%</h3>
                </div>
            </div>
            <div class="progress-bar bg-gray-700 rounded-full h-2">
                <div class="progress-fill bg-gradient-to-r from-purple-500 to-purple-400 h-full rounded-full" style="width: 70%"></div>
            </div>
        </div>
    `;
}

/**
 * Generate Recent Trades Rows
 */
function generateRecentTradesRows() {
    return dashboardDummyData.recentTrades.map(trade => {
        const profitClass = trade.profit >= 0 ? 'text-green-400' : 'text-red-400';
        const profitSign = trade.profit >= 0 ? '+' : '';
        const directionClass = trade.direction === 'BUY' ? 'text-green-400' : 'text-red-400';
        
        return `
            <tr class="border-b border-gray-700 hover:bg-white/5 transition-colors">
                <td class="py-3 pr-4 text-sm">${trade.date}</td>
                <td class="py-3 pr-4 font-medium">${trade.pair}</td>
                <td class="py-3 pr-4">
                    <span class="${directionClass} px-2 py-1 rounded text-xs font-semibold">${trade.direction}</span>
                </td>
                <td class="py-3 pr-4 text-sm">${trade.lotSize}</td>
                <td class="py-3 pr-4 ${profitClass} font-semibold">${profitSign}$${trade.profit}</td>
                <td class="py-3 pr-4 text-sm text-gray-400">${trade.rr}</td>
            </tr>
        `;
    }).join('');
}

/**
 * Initialize Equity Chart
 */
function initEquityChart() {
    const ctx = document.getElementById('equity-chart');
    if (!ctx || typeof Chart === 'undefined') return;
    
    const equityData = {
        labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        datasets: [{
            label: 'Equity ($)',
            data: [10000, 10120, 10250, 10180, 10420, 10380, 10420],
            borderColor: '#00ffa3',
            backgroundColor: 'rgba(0, 255, 163, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
        }]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: equityData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: 'rgba(71, 85, 105, 0.3)' }, ticks: { color: '#94a3b8' } },
                y: { grid: { color: 'rgba(71, 85, 105, 0.3)' }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}

/**
 * Initialize Win Rate Chart
 */
function initWinRateChart() {
    const ctx = document.getElementById('winrate-chart');
    if (!ctx || typeof Chart === 'undefined') return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Wins', 'Losses'],
            datasets: [{
                data: [68, 32],
                backgroundColor: ['#00ffa3', '#ff4757'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94a3b8' } }
            }
        }
    });
}

// Make functions globally available
window.loadDashboardOverview = loadDashboardOverview;
window.hideLoadingScreen = hideLoadingScreen;
