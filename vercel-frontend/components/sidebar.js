/**
 * Sidebar Component - COMPLETE VERSION
 * Handles navigation, dynamic content loading, and all page sections
 */

let sidebarCollapsed = false;
let sidebarOpen = false;

// Initialize sidebar
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggle-sidebar');
    const closeMobileBtn = document.getElementById('close-sidebar-mobile');
    const sidebar = document.getElementById('sidebar');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleSidebar);
    }
    
    if (closeMobileBtn) {
        closeMobileBtn.addEventListener('click', closeMobileSidebar);
    }
    
    // Load saved state from localStorage
    const savedState = localStorage.getItem('sidebarCollapsed');
    if (savedState === 'true') {
        collapseSidebar();
    }
});

/**
 * Toggle sidebar collapse state
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebarCollapsed = !sidebarCollapsed;
    
    if (sidebarCollapsed) {
        sidebar.classList.add('collapsed');
    } else {
        sidebar.classList.remove('collapsed');
    }
    
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed);
}

/**
 * Collapse sidebar
 */
function collapseSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebarCollapsed = true;
    sidebar.classList.add('collapsed');
    localStorage.setItem('sidebarCollapsed', 'true');
}

/**
 * Expand sidebar
 */
function expandSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebarCollapsed = false;
    sidebar.classList.remove('collapsed');
    localStorage.setItem('sidebarCollapsed', 'false');
}

/**
 * Open mobile sidebar
 */
function openMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebarOpen = true;
    sidebar.classList.add('active');
    
    // Create overlay if not exists
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay active';
        overlay.onclick = closeMobileSidebar;
        document.body.appendChild(overlay);
    } else {
        overlay.classList.add('active');
    }
    
    document.body.style.overflow = 'hidden';
}

/**
 * Close mobile sidebar
 */
function closeMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebarOpen = false;
    sidebar.classList.remove('active');
    
    const overlay = document.querySelector('.sidebar-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
    
    document.body.style.overflow = '';
}

/**
 * Navigate to different sections - DYNAMIC CONTENT LOADING
 */
function navigateTo(page) {
    console.log('Navigating to:', page);
    
    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeBtn = document.querySelector(`.nav-item[onclick="navigateTo('${page}')"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // Get main content area
    const mainContent = document.getElementById('main-content');
    if (!mainContent) return;
    
    // Add fade out effect
    mainContent.style.opacity = '0';
    mainContent.style.transition = 'opacity 0.3s ease';
    
    setTimeout(() => {
        // Load content based on page
        switch(page) {
            case 'dashboard': loadDashboardPage(); break;
            case 'challenges': loadChallengesPage(); break;
            case 'metrics': loadMetricsPage(); break;
            case 'journal': window.location.href = '/dashboard/journal'; return;
            case 'simulator': window.location.href = '/dashboard/simulator'; return;
            case 'risk': window.location.href = '/dashboard/risk'; return;
            case 'leaderboard': loadLeaderboardPage(); break;
            case 'rules': loadRulesPage(); break;
            case 'settings': loadSettingsPage(); break;
            case 'support': loadSupportPage(); break;
            default: loadDashboardPage();
        }
        
        // Fade in
        setTimeout(() => {
            mainContent.style.opacity = '1';
        }, 50);
        
        // Close mobile sidebar if open
        if (window.innerWidth < 1024) {
            closeMobileSidebar();
        }
    }, 300);
}

/**
 * Load Dashboard Overview Page
 */
function loadDashboardPage() {
    const pageTitle = document.getElementById('page-title');
    if (pageTitle) pageTitle.textContent = 'Dashboard Overview';
    
    // Reinitialize charts
    setTimeout(() => {
        if (typeof initEquityChart === 'function') initEquityChart();
        if (typeof initWinRateChart === 'function') initWinRateChart();
    }, 100);
}

/**
 * Logout function
 */
function logout() {
    showNotification('Logging out...', 'info');
    
    // Clear session
    localStorage.removeItem('selectedAccountId');
    sessionStorage.clear();
    
    // Redirect to login page
    setTimeout(() => {
        window.location.href = '/login';
    }, 1000);
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full opacity-0`;
    
    const colors = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        warning: 'bg-yellow-500 text-white',
        info: 'bg-blue-500 text-white'
    };
    
    notification.classList.add(...colors[type].split(' '));
    notification.innerHTML = `
        <div class="flex items-center gap-2">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    requestAnimationFrame(() => {
        notification.classList.remove('translate-x-full', 'opacity-0');
    });
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Load My Challenges Page
 */
function loadChallengesPage() {
    const pageTitle = document.getElementById('page-title');
    const mainContent = document.getElementById('main-content');
    
    if (pageTitle) pageTitle.textContent = 'My Challenges';
    
    const challenge = dashboardData.account;
    const progress = dashboardData.challengeProgress;
    
    mainContent.innerHTML = `
        <div class="space-y-6" data-aos="fade-up">
            <!-- Challenge Card -->
            <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                <div class="flex items-center justify-between mb-6">
                    <div>
                        <h3 class="text-2xl font-bold text-white">${challenge.challengeType}</h3>
                        <p class="text-gray-400">${challenge.phase}</p>
                    </div>
                    <div class="icon-box w-16 h-16 rounded-lg bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center">
                        <i class="fas fa-trophy text-green-400 text-2xl"></i>
                    </div>
                </div>
                
                <!-- Progress Bars -->
                <div class="space-y-4">
                    <div>
                        <div class="flex justify-between mb-2">
                            <span class="text-sm text-gray-400">Profit Target</span>
                            <span class="text-sm font-semibold text-green-400">${progress.profitTarget.percentage}%</span>
                        </div>
                        <div class="progress-bar bg-gray-700 rounded-full h-3">
                            <div class="progress-fill bg-gradient-to-r from-green-500 to-emerald-500 h-full rounded-full" style="width: ${progress.profitTarget.percentage}%"></div>
                        </div>
                    </div>
                    
                    <div>
                        <div class="flex justify-between mb-2">
                            <span class="text-sm text-gray-400">Daily Drawdown</span>
                            <span class="text-sm font-semibold text-blue-400">${progress.dailyDrawdown.percentage}% used</span>
                        </div>
                        <div class="progress-bar bg-gray-700 rounded-full h-3">
                            <div class="progress-fill bg-gradient-to-r from-blue-500 to-cyan-500 h-full rounded-full" style="width: ${progress.dailyDrawdown.percentage}%"></div>
                        </div>
                    </div>
                    
                    <div>
                        <div class="flex justify-between mb-2">
                            <span class="text-sm text-gray-400">Max Drawdown</span>
                            <span class="text-sm font-semibold text-purple-400">${progress.maxDrawdown.percentage}% used</span>
                        </div>
                        <div class="progress-bar bg-gray-700 rounded-full h-3">
                            <div class="progress-fill bg-gradient-to-r from-purple-500 to-pink-500 h-full rounded-full" style="width: ${progress.maxDrawdown.percentage}%"></div>
                        </div>
                    </div>
                    
                    <div>
                        <div class="flex justify-between mb-2">
                            <span class="text-sm text-gray-400">Trading Days</span>
                            <span class="text-sm font-semibold text-yellow-400">${challenge.currentTradingDays} / ${challenge.minimumTradingDays}</span>
                        </div>
                        <div class="progress-bar bg-gray-700 rounded-full h-3">
                            <div class="progress-fill bg-gradient-to-r from-yellow-500 to-orange-500 h-full rounded-full" style="width: ${progress.tradingDays.percentage}%"></div>
                        </div>
                    </div>
                </div>
                
                <!-- Metrics Grid -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                    <div class="text-center p-3 bg-gray-800/50 rounded-lg">
                        <p class="text-xs text-gray-400 mb-1">Profit Target</p>
                        <p class="text-lg font-bold text-green-400">${challenge.profitTarget}%</p>
                    </div>
                    <div class="text-center p-3 bg-gray-800/50 rounded-lg">
                        <p class="text-xs text-gray-400 mb-1">Daily Loss</p>
                        <p class="text-lg font-bold text-red-400">${challenge.dailyLossLimit}%</p>
                    </div>
                    <div class="text-center p-3 bg-gray-800/50 rounded-lg">
                        <p class="text-xs text-gray-400 mb-1">Max Drawdown</p>
                        <p class="text-lg font-bold text-orange-400">${challenge.maxDrawdown}%</p>
                    </div>
                    <div class="text-center p-3 bg-gray-800/50 rounded-lg">
                        <p class="text-xs text-gray-400 mb-1">Min Days</p>
                        <p class="text-lg font-bold text-blue-400">${challenge.minimumTradingDays}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Load Trading Metrics Page
 */
function loadMetricsPage() {
    const pageTitle = document.getElementById('page-title');
    const mainContent = document.getElementById('main-content');
    
    if (pageTitle) pageTitle.textContent = 'Trading Metrics';
    
    const analytics = dashboardData.analytics;
    
    mainContent.innerHTML = `
        <div class="space-y-6" data-aos="fade-up">
            <!-- Statistics Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up">
                    <div class="flex items-center justify-between mb-3">
                        <div class="icon-box w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center">
                            <i class="fas fa-chart-line text-blue-400 text-xl"></i>
                        </div>
                    </div>
                    <p class="text-sm text-gray-400 mb-1">Total Trades</p>
                    <h3 class="text-3xl font-bold text-white">${analytics.totalTrades}</h3>
                </div>
                
                <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="100">
                    <div class="flex items-center justify-between mb-3">
                        <div class="icon-box w-12 h-12 rounded-lg bg-green-500/20 flex items-center justify-center">
                            <i class="fas fa-check-circle text-green-400 text-xl"></i>
                        </div>
                    </div>
                    <p class="text-sm text-gray-400 mb-1">Win Rate</p>
                    <h3 class="text-3xl font-bold text-green-400">${analytics.winRate}%</h3>
                </div>
                
                <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="200">
                    <div class="flex items-center justify-between mb-3">
                        <div class="icon-box w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center">
                            <i class="fas fa-bullseye text-purple-400 text-xl"></i>
                        </div>
                    </div>
                    <p class="text-sm text-gray-400 mb-1">Average R:R</p>
                    <h3 class="text-3xl font-bold text-purple-400">${analytics.averageRR}</h3>
                </div>
                
                <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="300">
                    <div class="flex items-center justify-between mb-3">
                        <div class="icon-box w-12 h-12 rounded-lg bg-cyan-500/20 flex items-center justify-center">
                            <i class="fas fa-percent text-cyan-400 text-xl"></i>
                        </div>
                    </div>
                    <p class="text-sm text-gray-400 mb-1">Profit Factor</p>
                    <h3 class="text-3xl font-bold text-cyan-400">${analytics.profitFactor}</h3>
                </div>
                
                <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="400">
                    <div class="flex items-center justify-between mb-3">
                        <div class="icon-box w-12 h-12 rounded-lg bg-yellow-500/20 flex items-center justify-center">
                            <i class="fas fa-trophy text-yellow-400 text-xl"></i>
                        </div>
                    </div>
                    <p class="text-sm text-gray-400 mb-1">Largest Win</p>
                    <h3 class="text-3xl font-bold text-green-400">$${analytics.largestWin}</h3>
                </div>
                
                <div class="stat-card bg-secondary rounded-xl p-5 border border-gray-700 hover:border-accent transition-all" data-aos="fade-up" data-aos-delay="500">
                    <div class="flex items-center justify-between mb-3">
                        <div class="icon-box w-12 h-12 rounded-lg bg-red-500/20 flex items-center justify-center">
                            <i class="fas fa-arrow-down text-red-400 text-xl"></i>
                        </div>
                    </div>
                    <p class="text-sm text-gray-400 mb-1">Largest Loss</p>
                    <h3 class="text-3xl font-bold text-red-400">$${analytics.largestLoss}</h3>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                    <h4 class="text-lg font-semibold text-white mb-4">Win/Loss Distribution</h4>
                    <canvas id="metrics-winrate-chart" height="200"></canvas>
                </div>
                <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                    <h4 class="text-lg font-semibold text-white mb-4">Performance Breakdown</h4>
                    <div class="space-y-4">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-400">Winning Trades</span>
                            <span class="text-green-400 font-semibold">${analytics.wins}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-400">Losing Trades</span>
                            <span class="text-red-400 font-semibold">${analytics.losses}</span>
                        </div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-400">Win Percentage</span>
                            <span class="text-blue-400 font-semibold">${analytics.winRate}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Initialize win rate chart after DOM update
    setTimeout(() => {
        const ctx = document.getElementById('metrics-winrate-chart');
        if (ctx && typeof Chart !== 'undefined') {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Wins', 'Losses'],
                    datasets: [{
                        data: [analytics.wins, analytics.losses],
                        backgroundColor: ['#00ffa3', '#ff4757'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#94a3b8' }
                        }
                    }
                }
            });
        }
    }, 100);
}

/**
 * Load Leaderboard Page
 */
function loadLeaderboardPage() {
    const pageTitle = document.getElementById('page-title');
    const mainContent = document.getElementById('main-content');
    
    if (pageTitle) pageTitle.textContent = 'Leaderboard';
    
    const leaderboard = dashboardData.leaderboard;
    
    mainContent.innerHTML = `
        <div class="space-y-6" data-aos="fade-up">
            <!-- Top 3 Podium -->
            <div class="grid grid-cols-3 gap-4 mb-8">
                <div class="text-center">
                    <div class="bg-secondary rounded-xl p-4 border border-gray-700">
                        <div class="text-4xl mb-2">🥈</div>
                        <p class="font-bold text-white">${leaderboard[1].trader}</p>
                        <p class="text-green-400 font-semibold">+${leaderboard[1].profit}%</p>
                    </div>
                </div>
                <div class="text-center">
                    <div class="bg-gradient-to-br from-yellow-500/20 to-yellow-600/20 rounded-xl p-6 border border-yellow-500/50 transform scale-110">
                        <div class="text-5xl mb-2">🥇</div>
                        <p class="font-bold text-white text-lg">${leaderboard[0].trader}</p>
                        <p class="text-green-400 font-semibold text-xl">+${leaderboard[0].profit}%</p>
                    </div>
                </div>
                <div class="text-center">
                    <div class="bg-secondary rounded-xl p-4 border border-gray-700">
                        <div class="text-4xl mb-2">🥉</div>
                        <p class="font-bold text-white">${leaderboard[2].trader}</p>
                        <p class="text-green-400 font-semibold">+${leaderboard[2].profit}%</p>
                    </div>
                </div>
            </div>
            
            <!-- Full Leaderboard Table -->
            <div class="bg-secondary rounded-xl border border-gray-700 overflow-hidden">
                <div class="p-6 border-b border-gray-700">
                    <h3 class="text-xl font-bold text-white">Top Traders</h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-gray-800/50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Rank</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Trader</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Profit</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Win Rate</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Trades</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-700">
                            ${leaderboard.map((trader, index) => `
                                <tr class="hover:bg-gray-800/30 transition-colors">
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-lg font-bold ${index === 0 ? 'text-yellow-400' : index === 1 ? 'text-gray-400' : index === 2 ? 'text-orange-400' : 'text-gray-500'}">
                                            #${trader.rank}
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold mr-3">
                                                ${trader.trader.charAt(0)}
                                            </div>
                                            <span class="text-white font-medium">${trader.trader}</span>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-green-400 font-semibold">+${trader.profit}%</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-blue-400">${trader.winRate}%</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-gray-400">${trader.trades}</span>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `;
}

/**
 * Load Rules Page
 */
function loadRulesPage() {
    const pageTitle = document.getElementById('page-title');
    const mainContent = document.getElementById('main-content');
    
    if (pageTitle) pageTitle.textContent = 'Platform Rules';
    
    mainContent.innerHTML = `
        <div class="space-y-6" data-aos="fade-up">
            <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                <h3 class="text-2xl font-bold text-white mb-4">Trading Rules & Guidelines</h3>
                
                <div class="space-y-6">
                    <div>
                        <h4 class="text-lg font-semibold text-green-400 mb-2">📊 Profit Target Rules</h4>
                        <ul class="space-y-2 text-gray-400">
                            <li class="flex items-start">
                                <i class="fas fa-check text-green-400 mt-1 mr-2"></i>
                                <span>Achieve 8% profit target to pass Phase 1</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-check text-green-400 mt-1 mr-2"></i>
                                <span>Achieve 5% profit target to pass Phase 2</span>
                            </li>
                        </ul>
                    </div>
                    
                    <div>
                        <h4 class="text-lg font-semibold text-red-400 mb-2">⚠️ Risk Management Rules</h4>
                        <ul class="space-y-2 text-gray-400">
                            <li class="flex items-start">
                                <i class="fas fa-exclamation-triangle text-red-400 mt-1 mr-2"></i>
                                <span>Maximum daily loss: 5% of initial balance</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-exclamation-triangle text-red-400 mt-1 mr-2"></i>
                                <span>Maximum total drawdown: 10% of initial balance</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-exclamation-triangle text-red-400 mt-1 mr-2"></i>
                                <span>Minimum trading days: 5 days per phase</span>
                            </li>
                        </ul>
                    </div>
                    
                    <div>
                        <h4 class="text-lg font-semibold text-blue-400 mb-2">💡 Best Practices</h4>
                        <ul class="space-y-2 text-gray-400">
                            <li class="flex items-start">
                                <i class="fas fa-lightbulb text-blue-400 mt-1 mr-2"></i>
                                <span>Use proper risk management (1-2% per trade)</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-lightbulb text-blue-400 mt-1 mr-2"></i>
                                <span>Maintain a trading journal</span>
                            </li>
                            <li class="flex items-start">
                                <i class="fas fa-lightbulb text-blue-400 mt-1 mr-2"></i>
                                <span>Follow your trading plan consistently</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Load Account Settings Page
 */
function loadSettingsPage() {
    const pageTitle = document.getElementById('page-title');
    const mainContent = document.getElementById('main-content');
    
    if (pageTitle) pageTitle.textContent = 'Account Settings';
    
    const user = dashboardData.userSettings;
    
    mainContent.innerHTML = `
        <div class="space-y-6" data-aos="fade-up">
            <!-- Profile Settings -->
            <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                <h3 class="text-xl font-bold text-white mb-6">Profile Information</h3>
                
                <form class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-2">Full Name</label>
                            <input type="text" value="${user.name}" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-2">Email Address</label>
                            <input type="email" value="${user.email}" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-2">Phone Number</label>
                            <input type="tel" value="${user.phone}" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-2">Country</label>
                            <input type="text" value="${user.country}" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                        </div>
                    </div>
                    
                    <div class="pt-4">
                        <button type="button" onclick="showNotification('Settings saved successfully!', 'success')" class="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg hover:opacity-90 transition-opacity">
                            Save Changes
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- Change Password -->
            <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                <h3 class="text-xl font-bold text-white mb-6">Change Password</h3>
                
                <form class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-2">Current Password</label>
                        <input type="password" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-2">New Password</label>
                            <input type="password" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-400 mb-2">Confirm New Password</label>
                            <input type="password" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-accent">
                        </div>
                    </div>
                    
                    <div class="pt-4">
                        <button type="button" onclick="showNotification('Password updated successfully!', 'success')" class="px-6 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg hover:opacity-90 transition-opacity">
                            Update Password
                        </button>
                    </div>
                </form>
            </div>
        </div>
    `;
}

/**
 * Load Support Page
 */
function loadSupportPage() {
    const pageTitle = document.getElementById('page-title');
    const mainContent = document.getElementById('main-content');
    
    if (pageTitle) pageTitle.textContent = 'Support Center';
    
    const faq = dashboardData.faqData;
    
    mainContent.innerHTML = `
        <div class="space-y-6" data-aos="fade-up">
            <!-- Quick Actions -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-secondary rounded-xl p-6 border border-gray-700 hover:border-accent transition-all cursor-pointer" onclick="showNotification('Opening ticket system...', 'info')">
                    <div class="icon-box w-12 h-12 rounded-lg bg-blue-500/20 flex items-center justify-center mb-4">
                        <i class="fas fa-ticket-alt text-blue-400 text-xl"></i>
                    </div>
                    <h4 class="text-lg font-semibold text-white mb-2">Submit Ticket</h4>
                    <p class="text-gray-400 text-sm">Get help from our support team</p>
                </div>
                
                <div class="bg-secondary rounded-xl p-6 border border-gray-700 hover:border-accent transition-all cursor-pointer" onclick="showNotification('Opening email client...', 'info')">
                    <div class="icon-box w-12 h-12 rounded-lg bg-green-500/20 flex items-center justify-center mb-4">
                        <i class="fas fa-envelope text-green-400 text-xl"></i>
                    </div>
                    <h4 class="text-lg font-semibold text-white mb-2">Email Us</h4>
                    <p class="text-gray-400 text-sm">support@propfirm.com</p>
                </div>
                
                <div class="bg-secondary rounded-xl p-6 border border-gray-700 hover:border-accent transition-all cursor-pointer" onclick="showNotification('Opening FAQ...', 'info')">
                    <div class="icon-box w-12 h-12 rounded-lg bg-purple-500/20 flex items-center justify-center mb-4">
                        <i class="fas fa-question-circle text-purple-400 text-xl"></i>
                    </div>
                    <h4 class="text-lg font-semibold text-white mb-2">FAQ</h4>
                    <p class="text-gray-400 text-sm">Find answers to common questions</p>
                </div>
            </div>
            
            <!-- FAQ Section -->
            <div class="bg-secondary rounded-xl p-6 border border-gray-700">
                <h3 class="text-xl font-bold text-white mb-6">Frequently Asked Questions</h3>
                
                <div class="space-y-4">
                    ${faq.map((item, index) => `
                        <div class="border border-gray-700 rounded-lg p-4">
                            <h4 class="text-lg font-semibold text-white mb-2">${item.question}</h4>
                            <p class="text-gray-400">${item.answer}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}
