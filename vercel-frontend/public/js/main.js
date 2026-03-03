// Main JavaScript file for PropFirm Challenge website

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    initNavigation();
    initProgressBars();
    initAnimations();
    checkAuthState();
    initAdvancedVisualizations();
    initSmoothScrolling();
    initHoverEffects();
    initFAQAccordion();
    initScrollReveal();
    initTestimonials(); // Initialize testimonial slider with pagination sync
});

// Advanced Visualizations
function initAdvancedVisualizations() {
    // Enhanced chart initialization
    if (typeof Chart !== 'undefined') {
        // Set default chart options for smoother animations
        Chart.defaults.animation.duration = 2000;
        Chart.defaults.animation.easing = 'easeOutQuart';
    }
    
    // Enhanced sparkline charts for dashboard
    initSparklines();
}

// Sparkline charts
function initSparklines() {
    const sparklineContainers = document.querySelectorAll('.sparkline');
    sparklineContainers.forEach(container => {
        const data = JSON.parse(container.dataset.values);
        const ctx = container.getContext('2d');
        
        // Create a small line chart
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(data.length).fill(''),
                datasets: [{
                    data: data,
                    borderColor: container.dataset.color || '#00ff9d',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { x: { display: false }, y: { display: false } }
            }
        });
    });
}

// Smooth scrolling
function initSmoothScrolling() {
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Hover effects
function initHoverEffects() {
    // Add enhanced hover effects to cards
    const hoverableElements = document.querySelectorAll('.card, .step-card, .model-card, .pricing-card, .account-card');
    
    hoverableElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            // Add subtle scale effect
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s ease';
            
            // Enhance shadow
            this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.3)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // Enhanced button effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 255, 157, 0.2)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
        
        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(1px)';
        });
    });
}

// FAQ Accordion
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const header = item.querySelector('.faq-header');
        if (header) {
            header.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Close all other items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current item
                item.classList.toggle('active', !isActive);
            });
        }
    });
}

// Scroll Reveal Animation
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.scroll-reveal');
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
}

// Enhanced counter animations
function animateCounters() {
    // Animate counters when they come into view
    const counters = document.querySelectorAll('[data-target]');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const duration = parseInt(entry.target.getAttribute('data-duration')) || 2000;
                const increment = target / (duration / 16); // 60fps approximation
                let current = 0;
                
                entry.target.dataset.animated = true;
                
                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        entry.target.textContent = Math.ceil(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        entry.target.textContent = target;
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// Navigation Functions
function initNavigation() {
    // Premium Mobile Navigation Overlay
    const hamburger = document.querySelector('.hamburger');
    const mobileNavOverlay = document.getElementById('mobileNavOverlay');
    const mobileNavClose = document.getElementById('mobileNavClose');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    
    // Ensure body scroll is restored on initial page load
    document.body.style.overflow = 'auto';
    
    // Open mobile menu
    if (hamburger && mobileNavOverlay) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileNavOverlay.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scroll
        });
    }
    
    // Close mobile menu with close button
    if (mobileNavClose && mobileNavOverlay) {
        mobileNavClose.addEventListener('click', function() {
            mobileNavOverlay.classList.remove('active');
            document.body.style.overflow = 'auto'; // Restore scroll
        });
    }
    
    // Close mobile menu when clicking on overlay background
    if (mobileNavOverlay) {
        mobileNavOverlay.addEventListener('click', function(e) {
            if (e.target === mobileNavOverlay) {
                mobileNavOverlay.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    }
    
    // Close mobile menu when clicking a link AND reset after navigation
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileNavOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
            
            // Force reset after a short delay to ensure navigation completes
            setTimeout(() => {
                mobileNavOverlay.classList.remove('active');
                document.body.style.overflow = 'auto';
            }, 100);
        });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = hamburger.contains(event.target) || mobileNavOverlay.contains(event.target);
        
        if (!isClickInsideNav && mobileNavOverlay.classList.contains('active')) {
            mobileNavOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
    
    // Cleanup on page unload to prevent stuck state
    window.addEventListener('beforeunload', function() {
        document.body.style.overflow = 'auto';
        if (mobileNavOverlay) {
            mobileNavOverlay.classList.remove('active');
        }
    });
    
    // Sidebar toggle for desktop
    const menuToggle = document.querySelector('.menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('collapsed');
            document.querySelector('.main-content').classList.toggle('expanded');
        });
    }
}

// Progress Bar Animation
function initProgressBars() {
    // Animate progress bars when they come into view
    const progressBars = document.querySelectorAll('.progress-fill');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.style.width;
                entry.target.style.width = '0';
                
                setTimeout(() => {
                    entry.target.style.transition = 'width 1.5s ease-in-out';
                    entry.target.style.width = width;
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
}

// Animation Functions
function initAnimations() {
    // Fade in elements as they come into view
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-up, .zoom-in');
    
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    fadeElements.forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Counter animations for stats
    animateCounters();
}

function animateCounters() {
    // Animate counters when they come into view
    const counters = document.querySelectorAll('[data-target]');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                const increment = target / (duration / 16); // 60fps approximation
                let current = 0;
                
                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        entry.target.textContent = Math.ceil(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        entry.target.textContent = target;
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// Authentication State Check
function checkAuthState() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    // Update UI based on auth state
    if (isLoggedIn) {
        // Show logged-in navigation
        const loginLink = document.querySelector('a[href="/login"]');
        if (loginLink) {
            loginLink.textContent = 'Dashboard';
            loginLink.href = '/dashboard';
        }
    } else {
        // Ensure public navigation is shown
        const dashboardLink = document.querySelector('a[href="/dashboard"]');
        if (dashboardLink) {
            dashboardLink.textContent = 'Login';
            dashboardLink.href = '/login';
        }
    }
}

// Real-time Dashboard Updates
function initRealTimeUpdates() {
    // Simulate real-time data updates for dashboard
    setInterval(() => {
        if (window.location.pathname.includes('/dashboard')) {
            updateDashboardData();
        }
    }, 30000); // Update every 30 seconds
}

function updateDashboardData() {
    // In a real app, this would fetch data from the server
    console.log('Updating dashboard data...');
    
    // Example: Update floating P&L
    const floatingPnL = document.querySelector('.metric-value.positive');
    if (floatingPnL) {
        const currentValue = parseFloat(floatingPnL.textContent.replace(/[^\d.-]/g, ''));
        const randomChange = (Math.random() - 0.5) * 10; // Random change between -5 and +5
        const newValue = currentValue + randomChange;
        floatingPnL.textContent = newValue >= 0 ? `+${newValue.toFixed(2)}` : `${newValue.toFixed(2)}`;
        
        if (newValue >= 0) {
            floatingPnL.classList.add('positive');
            floatingPnL.classList.remove('negative');
        } else {
            floatingPnL.classList.add('negative');
            floatingPnL.classList.remove('positive');
        }
    }
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = '#ef4444';
        } else {
            input.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Smooth Scroll
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Style the toast
    Object.assign(toast.style, {
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        backgroundColor: type === 'success' ? '#10b981' : 
                         type === 'error' ? '#ef4444' : '#3b82f6',
        color: 'white',
        padding: '12px 20px',
        borderRadius: '8px',
        zIndex: '10000',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        maxWidth: '400px',
        wordWrap: 'break-word'
    });
    
    document.body.appendChild(toast);
    
    // Remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        showToast('Failed to copy!', 'error');
    });
}

// Password Strength Indicator
function checkPasswordStrength(password) {
    let strength = 0;
    const checks = {
        length: password.length >= 8,
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        numbers: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    Object.values(checks).forEach(check => {
        if (check) strength++;
    });
    
    return {
        strength,
        checks
    };
}

// Initialize tooltips if needed
function initTooltips() {
    // Add enhanced tooltip functionality
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(tooltip => {
        let timeoutId;
        
        tooltip.addEventListener('mouseenter', function() {
            // Delay tooltip appearance for better UX
            timeoutId = setTimeout(() => {
                const tooltipElement = document.createElement('div');
                tooltipElement.className = 'tooltip-element';
                tooltipElement.textContent = this.getAttribute('data-tooltip');
                
                // Add smooth entrance animation
                tooltipElement.style.opacity = '0';
                tooltipElement.style.transform = 'translateY(-10px)';
                
                Object.assign(tooltipElement.style, {
                    position: 'absolute',
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    color: 'white',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    fontSize: '14px',
                    zIndex: '10000',
                    pointerEvents: 'none',
                    top: this.getBoundingClientRect().bottom + 8 + 'px',
                    left: this.getBoundingClientRect().left + 'px',
                    maxWidth: '200px',
                    textAlign: 'center',
                    transition: 'opacity 0.3s ease, transform 0.3s ease',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
                });
                
                // Add arrow element
                const arrow = document.createElement('div');
                arrow.style.position = 'absolute';
                arrow.style.top = '-6px';
                arrow.style.left = '50%';
                arrow.style.marginLeft = '-6px';
                arrow.style.width = '0';
                arrow.style.height = '0';
                arrow.style.borderLeft = '6px solid transparent';
                arrow.style.borderRight = '6px solid transparent';
                arrow.style.borderBottom = '6px solid rgba(0, 0, 0, 0.9)';
                tooltipElement.appendChild(arrow);
                
                document.body.appendChild(tooltipElement);
                
                // Trigger entrance animation
                setTimeout(() => {
                    tooltipElement.style.opacity = '1';
                    tooltipElement.style.transform = 'translateY(0)';
                }, 10);
                
                this.tooltipElement = tooltipElement;
            }, 500); // 500ms delay
        });
        
        tooltip.addEventListener('mouseleave', function() {
            clearTimeout(timeoutId);
            if (this.tooltipElement) {
                // Animate exit
                this.tooltipElement.style.opacity = '0';
                this.tooltipElement.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    if (this.tooltipElement) {
                        this.tooltipElement.remove();
                        this.tooltipElement = null;
                    }
                }, 300);
            }
        });
    });
}

// Handle window resize for responsive elements
window.addEventListener('resize', debounce(() => {
    // Reinitialize responsive elements if needed
    if (window.innerWidth <= 768) {
        // Mobile-specific adjustments
    } else {
        // Desktop-specific adjustments
    }
}, 250));

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateForm,
        smoothScroll,
        showToast,
        copyToClipboard,
        checkPasswordStrength
    };
}

// Initialize real-time updates for dashboard
initRealTimeUpdates();

// Add event listeners for various interactive elements
document.addEventListener('click', function(e) {
    // Handle dynamic content interactions
    if (e.target.matches('.btn[data-action]')) {
        const action = e.target.getAttribute('data-action');
        handleAction(action, e.target);
    }
});

function handleAction(action, element) {
    switch(action) {
        case 'refresh-data':
            // Refresh data on dashboard
            updateDashboardData();
            break;
        case 'export-data':
            // Handle data export
            showToast('Exporting data...', 'info');
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Testimonial Slider with Dynamic Pagination Sync
function initTestimonials() {
    const track = document.getElementById('testimonialTrack');
    const dotsContainer = document.getElementById('testimonialDots');
    
    if (!track || !dotsContainer) return;
    
    const cards = track.querySelectorAll('.testimonial-card');
    const totalUniqueCards = 9; // We have 9 unique testimonials
    let currentSlide = 0;
    let autoplayInterval;
    const autoplayDelay = 2000; // 2 seconds between slides
    const animationSpeed = 400; // 0.4s transition speed
    
    // Add active class to track for animation
    track.classList.add('animate');
    
    // Update pagination dots
    function updatePagination(index) {
        const dots = dotsContainer.querySelectorAll('.testimonial-dot');
        dots.forEach((dot, i) => {
            dot.classList.remove('active');
            if (i === index % totalUniqueCards) {
                dot.classList.add('active');
            }
        });
    }
    
    // Pause animation on hover
    track.addEventListener('mouseenter', () => {
        track.style.animationPlayState = 'paused';
        clearInterval(autoplayInterval);
    });
    
    track.addEventListener('mouseleave', () => {
        track.style.animationPlayState = 'running';
        startAutoplay();
    });
    
    // Click on dots to navigate
    dotsContainer.querySelectorAll('.testimonial-dot').forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updatePagination(currentSlide);
            // Smooth scroll to specific card
            const cardWidth = cards[0].offsetWidth + 24; // card width + gap
            track.scrollTo({
                left: cardWidth * currentSlide,
                behavior: 'smooth'
            });
        });
    });
    
    // Auto-update pagination based on scroll position
    track.addEventListener('scroll', () => {
        const cardWidth = cards[0].offsetWidth + 24;
        const scrollPos = track.scrollLeft;
        const newIndex = Math.round(scrollPos / cardWidth);
        
        if (newIndex !== currentSlide && newIndex >= 0 && newIndex < totalUniqueCards) {
            currentSlide = newIndex;
            updatePagination(currentSlide);
        }
    });
    
    // Start autoplay
    function startAutoplay() {
        autoplayInterval = setInterval(() => {
            const cardWidth = cards[0].offsetWidth + 24;
            const maxScroll = track.scrollWidth - track.clientWidth;
            
            if (track.scrollLeft >= maxScroll - 10) {
                // Reset to beginning smoothly
                track.scrollTo({ left: 0, behavior: 'smooth' });
                currentSlide = 0;
            } else {
                track.scrollBy({
                    left: cardWidth,
                    behavior: 'smooth'
                });
                currentSlide++;
            }
            
            updatePagination(currentSlide);
        }, autoplayDelay);
    }
    
    startAutoplay();
    updatePagination(0);
}

// Initialize all components when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
});