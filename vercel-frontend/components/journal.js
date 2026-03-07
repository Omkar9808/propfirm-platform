/**
 * Trade Journal Component
 * Handles trade journal functionality including add, edit, and display trades
 */

// Sample journal data
let journalTrades = [
    { id: 1, date: '2026-03-07', pair: 'EURUSD', direction: 'BUY', lotSize: 0.5, entry: 1.0850, exit: 1.0870, profit: 120, rr: '1:2', notes: 'Clean breakout retest' },
    { id: 2, date: '2026-03-06', pair: 'GBPUSD', direction: 'SELL', lotSize: 0.3, entry: 1.2650, exit: 1.2630, profit: 85, rr: '1:1.5', notes: 'Trend continuation' },
    { id: 3, date: '2026-03-06', pair: 'USDJPY', direction: 'BUY', lotSize: 0.4, entry: 149.50, exit: 149.80, profit: 95, rr: '1:2', notes: 'Support bounce' },
    { id: 4, date: '2026-03-05', pair: 'XAUUSD', direction: 'SELL', lotSize: 0.2, entry: 2035.50, exit: 2042.00, profit: -150, rr: '1:1', notes: 'Reversal attempt - stopped out' },
    { id: 5, date: '2026-03-04', pair: 'AUDUSD', direction: 'BUY', lotSize: 0.6, entry: 0.6550, exit: 0.6570, profit: 145, rr: '1:2.5', notes: 'Perfect setup' }
];

/**
 * Initialize journal when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    if (typeof AOS !== 'undefined') {
        AOS.init({ duration: 600, easing: 'ease-out-cubic', once: true });
    }
    
    // Load journal trades
    loadJournalTrades();
    updateJournalStats();
    
    // Setup form submission
    const form = document.getElementById('add-trade-form');
    if (form) {
        form.addEventListener('submit', handleAddTrade);
    }
    
    // Setup search and filter
    const searchInput = document.getElementById('search-trades');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearchTrades);
    }
    
    const filterPair = document.getElementById('filter-pair');
    if (filterPair) {
        filterPair.addEventListener('change', handleFilterTrades);
    }
});

/**
 * Load all journal trades into table
 */
function loadJournalTrades(tradesToLoad = journalTrades) {
    const tbody = document.getElementById('journal-trades-body');
    
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    tradesToLoad.forEach((trade, index) => {
        const row = document.createElement('tr');
        row.className = 'border-b border-gray-700 hover:bg-white/5 transition-colors';
        row.style.animationDelay = `${index * 0.05}s`;
        
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
            <td class="py-3 pr-4 text-sm">${trade.entry}</td>
            <td class="py-3 pr-4 text-sm">${trade.exit}</td>
            <td class="py-3 pr-4 ${profitClass} font-semibold">${profitSign}$${trade.profit.toFixed(2)}</td>
            <td class="py-3 pr-4 text-sm text-gray-400">${trade.rr || '-'}</td>
            <td class="py-3 pr-4 text-sm text-gray-400 max-w-xs truncate" title="${trade.notes || ''}">${trade.notes || '-'}</td>
        `;
        
        tbody.appendChild(row);
    });
}

/**
 * Update journal statistics
 */
function updateJournalStats() {
    const totalTrades = journalTrades.length;
    const wins = journalTrades.filter(t => t.profit > 0).length;
    const losses = Math.abs(journalTrades.filter(t => t.profit < 0).length);
    const totalPL = journalTrades.reduce((sum, t) => sum + t.profit, 0);
    const grossProfit = journalTrades.filter(t => t.profit > 0).reduce((sum, t) => sum + t.profit, 0);
    const grossLoss = Math.abs(journalTrades.filter(t => t.profit < 0).reduce((sum, t) => sum + t.profit, 0));
    
    const winRate = totalTrades > 0 ? ((wins / totalTrades) * 100).toFixed(1) : 0;
    const profitFactor = grossLoss > 0 ? (grossProfit / grossLoss).toFixed(2) : grossProfit.toFixed(2);
    
    // Animate counters
    animateCounter(document.getElementById('total-trades'), 0, totalTrades, 1000);
    
    const winRateEl = document.getElementById('win-rate');
    if (winRateEl) {
        winRateEl.textContent = winRate + '%';
        winRateEl.className = `text-2xl font-bold ${winRate >= 50 ? 'text-success' : 'text-danger'}`;
    }
    
    const totalPLEl = document.getElementById('total-pl');
    if (totalPLEl) {
        totalPLEl.textContent = '$' + totalPL.toFixed(2);
        totalPLEl.className = `text-2xl font-bold ${totalPL >= 0 ? 'text-success' : 'text-danger'}`;
    }
    
    const profitFactorEl = document.getElementById('profit-factor');
    if (profitFactorEl) {
        profitFactorEl.textContent = profitFactor;
    }
}

/**
 * Handle add trade form submission
 */
function handleAddTrade(e) {
    e.preventDefault();
    
    const newTrade = {
        id: Date.now(),
        date: document.getElementById('trade-date').value,
        pair: document.getElementById('trade-pair').value.toUpperCase(),
        direction: document.getElementById('trade-direction').value,
        lotSize: parseFloat(document.getElementById('trade-lot-size').value),
        entry: parseFloat(document.getElementById('trade-entry').value),
        exit: parseFloat(document.getElementById('trade-exit').value),
        profit: parseFloat(document.getElementById('trade-profit').value) || 0,
        rr: document.getElementById('trade-rr').value,
        notes: document.getElementById('trade-notes').value
    };
    
    journalTrades.unshift(newTrade); // Add to beginning
    
    loadJournalTrades();
    updateJournalStats();
    closeAddTradeModal();
    
    showNotification('Trade added successfully!', 'success');
    
    // Reset form
    e.target.reset();
}

/**
 * Handle search trades
 */
function handleSearchTrades(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    const filtered = journalTrades.filter(trade => 
        trade.pair.toLowerCase().includes(searchTerm) ||
        trade.notes.toLowerCase().includes(searchTerm)
    );
    
    loadJournalTrades(filtered);
}

/**
 * Handle filter by pair
 */
function handleFilterTrades(e) {
    const pair = e.target.value;
    
    if (!pair) {
        loadJournalTrades(journalTrades);
    } else {
        const filtered = journalTrades.filter(trade => trade.pair === pair);
        loadJournalTrades(filtered);
    }
}

/**
 * Open add trade modal
 */
function openAddTradeModal() {
    const modal = document.getElementById('add-trade-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Set default date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('trade-date').value = today;
    }
}

/**
 * Close add trade modal
 */
function closeAddTradeModal() {
    const modal = document.getElementById('add-trade-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { month: 'short', day: 'numeric', year: 'numeric' };
    return date.toLocaleDateString('en-US', options);
}

// Make functions globally available
window.openAddTradeModal = openAddTradeModal;
window.closeAddTradeModal = closeAddTradeModal;
window.loadJournalTrades = loadJournalTrades;
