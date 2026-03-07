/**
 * Statistics Cards Component
 * Handles animated number counters and progress bars
 */

/**
 * Animate number counting from start to end
 * @param {HTMLElement} element - Element to animate
 * @param {number} start - Starting value
 * @param {number} end - Ending value
 * @param {number} duration - Animation duration in ms
 */
function animateCounter(element, start, end, duration = 1500) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out-quad)
        const easeProgress = 1 - (1 - progress) * (1 - progress);
        
        const current = start + (end - start) * easeProgress;
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.value = current.toFixed(2);
        } else {
            element.textContent = '$' + current.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        }
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

/**
 * Animate progress bar to target percentage
 * @param {HTMLElement} progressBar - Progress bar element
 * @param {number} percentage - Target percentage (0-100)
 */
function animateProgressBar(progressBar, percentage) {
    setTimeout(() => {
        progressBar.style.width = percentage + '%';
    }, 100);
}

/**
 * Initialize all stat card animations
 */
function initStatCards() {
    // Animate balance counter
    const balanceEl = document.getElementById('balance');
    if (balanceEl) {
        const balanceValue = parseFloat(balanceEl.textContent.replace('$', '').replace(',', ''));
        balanceEl.textContent = '$0.00';
        animateCounter(balanceEl, 0, balanceValue, 1500);
    }
    
    // Animate equity counter
    const equityEl = document.getElementById('equity');
    if (equityEl) {
        const equityValue = parseFloat(equityEl.textContent.replace('$', '').replace(',', ''));
        equityEl.textContent = '$0.00';
        animateCounter(equityEl, 0, equityValue, 1500);
    }
    
    // Animate profit target counter
    const profitTargetEl = document.getElementById('profit-target');
    if (profitTargetEl) {
        const profitValue = parseFloat(profitTargetEl.textContent.replace('$', '').replace(',', ''));
        profitTargetEl.textContent = '$0.00';
        animateCounter(profitTargetEl, 0, profitValue, 1500);
    }
}

/**
 * Update account statistics with new data
 * @param {Object} accountData - Account data object
 */
function updateAccountStats(accountData) {
    if (!accountData) return;
    
    const fields = ['balance', 'equity', 'profit-target'];
    
    fields.forEach(field => {
        const element = document.getElementById(field);
        if (element && accountData[field]) {
            element.textContent = '$' + accountData[field].toLocaleString('en-US', {minimumFractionDigits: 2});
        }
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure elements are rendered
    setTimeout(() => {
        initStatCards();
    }, 500);
});
