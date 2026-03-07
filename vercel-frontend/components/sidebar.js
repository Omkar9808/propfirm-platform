/**
 * Sidebar Component
 * Handles sidebar navigation, collapse functionality, and mobile menu
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
 * Navigate to different sections
 * @param {string} page - Page identifier
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
    
    // Update page title
    const titles = {
        'dashboard': 'Dashboard Overview',
        'challenges': 'My Challenges',
        'metrics': 'Trading Metrics',
        'journal': 'Trade Journal',
        'simulator': 'Equity Simulator',
        'risk': 'Risk Calculator',
        'leaderboard': 'Leaderboard',
        'rules': 'Platform Rules',
        'settings': 'Account Settings',
        'support': 'Support Center'
    };
    
    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
        pageTitle.textContent = titles[page] || 'Dashboard';
    }
    
    // Close mobile sidebar after navigation
    if (window.innerWidth < 1024) {
        closeMobileSidebar();
    }
    
    // For demo purposes, show notification for non-dashboard pages
    if (page !== 'dashboard') {
        setTimeout(() => {
            showNotification(`${page.charAt(0).toUpperCase() + page.slice(1)} page coming soon!`, 'info');
        }, 300);
    }
}

/**
 * Logout function
 */
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear session
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userToken');
        
        // Redirect to login page
        window.location.href = '/login';
    }
}

/**
 * Show notification toast
 * @param {string} message - Notification message
 * @param {string} type - Type: 'success', 'error', 'info', 'warning'
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transform transition-all duration-300 translate-x-full`;
    
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-blue-600',
        warning: 'bg-yellow-600'
    };
    
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle'
    };
    
    notification.innerHTML = `
        <div class="${colors[type]} text-white px-4 py-3 rounded-lg flex items-center gap-3">
            <i class="fas ${icons[type]}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
