/**
 * Risk Calculator Component
 * Calculates position size, risk amount, and stop loss
 */

let riskChartInstance = null;

/**
 * Initialize risk calculator when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({ duration: 600, easing: 'ease-out-cubic', once: true });
    }
    
    // Setup form inputs
    const inputs = ['account-balance', 'risk-percent', 'stop-loss-pips', 'lot-size'];
    
    inputs.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('input', calculateRisk);
        }
    });
    
    // Run initial calculation
    setTimeout(calculateRisk, 500);
});

/**
 * Calculate risk based on inputs
 */
function calculateRisk() {
    // Get input values
    const accountBalance = parseFloat(document.getElementById('account-balance').value) || 10000;
    const riskPercent = (parseFloat(document.getElementById('risk-percent').value) || 1) / 100;
    const stopLossPips = parseFloat(document.getElementById('stop-loss-pips').value) || 20;
    const lotSize = parseFloat(document.getElementById('lot-size').value) || 0.1;
    
    // Calculate risk amount
    const riskAmount = accountBalance * riskPercent;
    
    // Calculate pip value (simplified for forex - $10 per standard lot per pip)
    const pipValueStandard = 10;
    const pipValue = pipValueStandard * lotSize;
    
    // Calculate position size
    const positionSize = riskAmount / (stopLossPips * pipValueStandard);
    
    // Calculate risk reward scenarios
    const scenarios = [
        { rr: '1:1', profit: riskAmount, pips: stopLossPips },
        { rr: '1:1.5', profit: riskAmount * 1.5, pips: stopLossPips * 1.5 },
        { rr: '1:2', profit: riskAmount * 2, pips: stopLossPips * 2 },
        { rr: '1:3', profit: riskAmount * 3, pips: stopLossPips * 3 }
    ];
    
    // Update display
    document.getElementById('risk-amount').textContent = formatCurrency(riskAmount);
    document.getElementById('position-size').textContent = positionSize.toFixed(2) + ' lots';
    document.getElementById('pip-value').textContent = formatCurrency(pipValue);
    document.getElementById('risk-reward-table').innerHTML = generateRRTable(scenarios, riskAmount);
    
    // Update chart
    updateRiskChart(accountBalance, riskAmount, scenarios);
}

/**
 * Generate risk reward table HTML
 */
function generateRRTable(scenarios, riskAmount) {
    return scenarios.map(scenario => `
        <div class="flex justify-between items-center py-2 border-b border-gray-700 last:border-0">
            <span class="text-sm text-gray-400">${scenario.rr}</span>
            <span class="font-semibold text-success">+$${scenario.profit.toFixed(2)}</span>
            <span class="text-xs text-gray-500">${scenario.pips.toFixed(0)} pips</span>
        </div>
    `).join('');
}

/**
 * Update risk chart
 */
function updateRiskChart(balance, risk, scenarios) {
    const ctx = document.getElementById('risk-chart');
    
    if (!ctx) return;
    
    if (riskChartInstance) {
        riskChartInstance.destroy();
    }
    
    const config = {
        type: 'bar',
        data: {
            labels: ['Account', 'Risk', '1:1', '1:2', '1:3'],
            datasets: [{
                label: 'Amount ($)',
                data: [
                    balance,
                    -risk,
                    risk,
                    risk * 2,
                    risk * 3
                ],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(16, 185, 129, 0.6)',
                    'rgba(16, 185, 129, 0.7)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderColor: [
                    'rgb(59, 130, 246)',
                    'rgb(239, 68, 68)',
                    'rgb(16, 185, 129)',
                    'rgb(16, 185, 129)',
                    'rgb(16, 185, 129)'
                ],
                borderWidth: 2
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
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#9ca3af'
                    }
                }
            }
        }
    };
    
    riskChartInstance = new Chart(ctx, config);
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return '$' + value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
