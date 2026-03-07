/**
 * Equity Simulator Component
 * Simulates account growth based on trading parameters
 */

let simulatorChartInstance = null;

/**
 * Initialize simulator when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({ duration: 600, easing: 'ease-out-cubic', once: true });
    }
    
    // Setup form submission
    const form = document.getElementById('simulator-form');
    if (form) {
        form.addEventListener('submit', runSimulation);
    }
    
    // Run initial simulation with defaults
    setTimeout(runSimulation, 500);
});

/**
 * Run equity simulation
 */
function runSimulation(e) {
    if (e) e.preventDefault();
    
    // Get input values
    const initialBalance = parseFloat(document.getElementById('initial-balance').value) || 10000;
    const riskPercent = (parseFloat(document.getElementById('risk-per-trade').value) || 1) / 100;
    const winRate = (parseFloat(document.getElementById('win-rate').value) || 60) / 100;
    const rrRatioText = document.getElementById('rr-ratio').value || '1:2';
    const numTrades = parseInt(document.getElementById('num-trades').value) || 100;
    
    // Parse RR ratio
    const rrParts = rrRatioText.split(':');
    const riskReward = rrParts.length === 2 ? parseFloat(rrParts[1]) / parseFloat(rrParts[0]) : 2;
    
    // Calculate expected wins and losses
    const expectedWins = Math.round(numTrades * winRate);
    const expectedLosses = numTrades - expectedWins;
    
    // Calculate average win and loss amounts
    const avgRiskAmount = initialBalance * riskPercent;
    const avgWinAmount = avgRiskAmount * riskReward;
    const avgLossAmount = avgRiskAmount;
    
    // Simulate trades
    let balance = initialBalance;
    const equityCurve = [balance];
    const labels = ['Start'];
    
    for (let i = 1; i <= numTrades; i++) {
        const isWin = Math.random() < winRate;
        
        if (isWin) {
            balance += avgRiskAmount * riskReward;
        } else {
            balance -= avgRiskAmount;
        }
        
        equityCurve.push(balance);
        
        // Add label every 10 trades
        if (i % 10 === 0 || i === numTrades) {
            labels.push(`Trade ${i}`);
        } else {
            labels.push('');
        }
    }
    
    // Update results
    const finalBalance = balance;
    const totalProfit = finalBalance - initialBalance;
    const growthPercent = ((totalProfit / initialBalance) * 100).toFixed(2);
    const grossProfit = expectedWins * avgWinAmount;
    const grossLoss = expectedLosses * avgLossAmount;
    const profitFactor = grossLoss > 0 ? (grossProfit / grossLoss) : grossProfit;
    
    // Display results
    document.getElementById('final-balance').textContent = formatCurrency(finalBalance);
    document.getElementById('total-profit').textContent = formatCurrency(totalProfit);
    document.getElementById('expected-wins').textContent = expectedWins;
    document.getElementById('expected-losses').textContent = expectedLosses;
    document.getElementById('growth-percent').textContent = growthPercent + '%';
    document.getElementById('avg-win').textContent = formatCurrency(avgWinAmount);
    document.getElementById('avg-loss').textContent = formatCurrency(avgLossAmount);
    document.getElementById('sim-profit-factor').textContent = profitFactor.toFixed(2);
    
    // Color code results
    const profitEl = document.getElementById('total-profit');
    profitEl.className = `font-bold ${totalProfit >= 0 ? 'text-success' : 'text-danger'}`;
    
    const growthEl = document.getElementById('growth-percent');
    growthEl.className = `text-xl font-bold ${growthPercent >= 0 ? 'text-success' : 'text-danger'}`;
    
    // Update chart
    updateSimulatorChart(labels.filter(l => l !== ''), equityCurve);
}

/**
 * Update simulator chart
 */
function updateSimulatorChart(labels, data) {
    const ctx = document.getElementById('equity-simulator-chart');
    
    if (!ctx) return;
    
    // Destroy existing chart
    if (simulatorChartInstance) {
        simulatorChartInstance.destroy();
    }
    
    const config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Equity ($)',
                data: data,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(30, 41, 59, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#9ca3af',
                    callbacks: {
                        label: function(context) {
                            return '$' + context.parsed.y.toLocaleString('en-US', {minimumFractionDigits: 2});
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    },
                    ticks: {
                        color: '#9ca3af',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(71, 85, 105, 0.3)'
                    },
                    ticks: {
                        color: '#9ca3af',
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    };
    
    simulatorChartInstance = new Chart(ctx, config);
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return '$' + value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
