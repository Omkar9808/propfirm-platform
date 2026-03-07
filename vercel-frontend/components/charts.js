/**
 * Charts Component
 * Handles all Chart.js visualizations using pure JavaScript
 */

let equityChartInstance = null;
let winrateChartInstance = null;

/**
 * Initialize all charts when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    initEquityChart();
    initWinRateChart();
});

/**
 * Initialize Equity Performance Chart
 */
function initEquityChart() {
    const ctx = document.getElementById('equity-chart');
    
    if (!ctx) return;
    
    // Sample equity data
    const equityData = {
        labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
        datasets: [{
            label: 'Equity ($)',
            data: [10000, 10150, 10080, 10250, 10180, 10320, 10310],
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointBackgroundColor: '#3b82f6',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 6
        }]
    };
    
    const config = {
        type: 'line',
        data: equityData,
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
                    borderColor: 'rgba(59, 130, 246, 0.5)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
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
                        color: '#9ca3af'
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
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    };
    
    equityChartInstance = new Chart(ctx, config);
}

/**
 * Initialize Win Rate Pie Chart
 */
function initWinRateChart() {
    const ctx = document.getElementById('winrate-chart');
    
    if (!ctx) return;
    
    // Sample win rate data
    const winrateData = {
        labels: ['Wins', 'Losses'],
        datasets: [{
            data: [18, 5],
            backgroundColor: [
                'rgba(16, 185, 129, 0.8)',
                'rgba(239, 68, 68, 0.8)'
            ],
            borderColor: [
                'rgb(16, 185, 129)',
                'rgb(239, 68, 68)'
            ],
            borderWidth: 2
        }]
    };
    
    const config = {
        type: 'doughnut',
        data: winrateData,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#9ca3af',
                        padding: 20,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#9ca3af',
                    borderColor: 'rgba(71, 85, 105, 0.5)',
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    };
    
    winrateChartInstance = new Chart(ctx, config);
}

/**
 * Update equity chart with new data
 * @param {Array} newData - New equity data points
 * @param {Array} newLabels - New labels
 */
function updateEquityChart(newData, newLabels) {
    if (!equityChartInstance) return;
    
    equityChartInstance.data.datasets[0].data = newData;
    equityChartInstance.data.labels = newLabels;
    equityChartInstance.update('default');
}

/**
 * Update win rate chart
 * @param {number} wins - Number of wins
 * @param {number} losses - Number of losses
 */
function updateWinRateChart(wins, losses) {
    if (!winrateChartInstance) return;
    
    winrateChartInstance.data.datasets[0].data = [wins, losses];
    winrateChartInstance.update('default');
}

/**
 * Destroy all charts (for cleanup)
 */
function destroyCharts() {
    if (equityChartInstance) {
        equityChartInstance.destroy();
        equityChartInstance = null;
    }
    
    if (winrateChartInstance) {
        winrateChartInstance.destroy();
        winrateChartInstance = null;
    }
}
