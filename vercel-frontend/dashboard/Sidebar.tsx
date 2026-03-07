import React from 'react';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = ({ isOpen, toggleSidebar, mobileOpen, setMobileOpen }) => {
  const location = useLocation();

  const menuItems = [
    { icon: 'fa-home', label: 'Dashboard', path: '/dashboard' },
    { icon: 'fa-chart-line', label: 'Practice Trading', path: '/dashboard/practice' },
    { icon: 'fa-trophy', label: 'My Challenges', path: '/dashboard/challenges' },
    { icon: 'fa-history', label: 'Trade History', path: '/dashboard/history' },
    { icon: 'fa-chart-bar', label: 'Analytics', path: '/dashboard/analytics' },
    { icon: 'fa-users', label: 'Leaderboard', path: '/leaderboard' },
    { icon: 'fa-book', label: 'Rules', path: '/rules' },
    { icon: 'fa-certificate', label: 'Certificates', path: '/dashboard/certificates' },
    { icon: 'fa-credit-card', label: 'Billing', path: '/dashboard/billing' },
    { icon: 'fa-cog', label: 'Settings', path: '/dashboard/settings' },
  ];

  const sidebarVariants = {
    open: { width: 256 },
    closed: { width: 80 },
  };

  const handleMenuItemClick = (path) => {
    if (window.location.pathname !== path) {
      window.location.href = path;
    }
    setMobileOpen(false);
  };

  return (
    <>
      {/* Desktop Sidebar */}
      <motion.aside
        initial={false}
        animate={isOpen ? 'open' : 'closed'}
        variants={sidebarVariants}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="hidden lg:flex fixed left-0 top-0 h-screen bg-[#0a0a0c] border-r border-white/10 z-30 overflow-hidden"
      >
        <div className="flex flex-col h-full w-full">
          {/* Logo Section */}
          <div className="p-4 flex items-center justify-center border-b border-white/10">
            <Link to="/" className="flex items-center gap-3">
              <div className="logo-symbol w-10 h-10 flex items-center justify-center">
                <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-[#00ff9d]">
                  <path d="M8 28L16 20L22 26L32 14" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="32" cy="14" r="3" fill="currentColor"/>
                </svg>
              </div>
              {isOpen && (
                <motion.span 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="logo-text text-xl font-bold"
                >
                  PropFirm<span className="text-[#00ff9d]">Challenge</span>
                </motion.span>
              )}
            </Link>
          </div>

          {/* Navigation Menu */}
          <nav className="flex-1 py-6 overflow-y-auto">
            <ul className="space-y-1 px-3">
              {menuItems.map((item, index) => {
                const isActive = location.pathname === item.path || 
                  (item.path !== '/dashboard' && location.pathname.startsWith(item.path));
                
                return (
                  <motion.li
                    key={item.label}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <button
                      onClick={() => handleMenuItemClick(item.path)}
                      className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all duration-200 group relative
                        ${isActive 
                          ? 'bg-gradient-to-r from-[#00ff9d]/20 to-[#0ea5e9]/10 text-[#00ff9d] border-l-4 border-[#00ff9d]' 
                          : 'text-gray-400 hover:bg-white/5 hover:text-white'
                        }`}
                    >
                      <i className={`fas ${item.icon} text-lg w-6 text-center`}></i>
                      {isOpen && (
                        <motion.span
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="font-medium"
                        >
                          {item.label}
                        </motion.span>
                      )}
                      {!isOpen && (
                        <div className="absolute left-full ml-2 px-3 py-2 bg-gray-900 border border-white/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none">
                          <span className="text-sm">{item.label}</span>
                        </div>
                      )}
                    </button>
                  </motion.li>
                );
              })}
            </ul>
          </nav>

          {/* Logout Button */}
          <div className="p-4 border-t border-white/10">
            <button
              onClick={() => {
                localStorage.removeItem('isLoggedIn');
                window.location.href = '/login';
              }}
              className="w-full flex items-center gap-3 px-3 py-3 rounded-lg text-red-400 hover:bg-red-500/10 transition-colors"
            >
              <i className="fas fa-sign-out-alt text-lg w-6 text-center"></i>
              {isOpen && <span className="font-medium">Logout</span>}
            </button>
          </div>
        </div>
      </motion.aside>

      {/* Mobile Sidebar */}
      <motion.div
        initial={{ x: '-100%' }}
        animate={{ x: mobileOpen ? 0 : '-100%' }}
        transition={{ type: 'tween', duration: 0.3 }}
        className="lg:hidden fixed left-0 top-0 h-screen w-64 bg-[#0a0a0c] border-r border-white/10 z-50"
      >
        <div className="flex flex-col h-full">
          {/* Logo with Close Button */}
          <div className="p-4 flex items-center justify-between border-b border-white/10">
            <Link to="/" className="flex items-center gap-3">
              <div className="logo-symbol w-10 h-10 flex items-center justify-center">
                <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-[#00ff9d]">
                  <path d="M8 28L16 20L22 26L32 14" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="32" cy="14" r="3" fill="currentColor"/>
                </svg>
              </div>
              <span className="logo-text text-xl font-bold">
                PropFirm<span className="text-[#00ff9d]">Challenge</span>
              </span>
            </Link>
            <button
              onClick={() => setMobileOpen(false)}
              className="text-gray-400 hover:text-white"
            >
              <i className="fas fa-times text-xl"></i>
            </button>
          </div>

          {/* Mobile Menu */}
          <nav className="flex-1 py-6 overflow-y-auto">
            <ul className="space-y-1 px-3">
              {menuItems.map((item) => {
                const isActive = location.pathname === item.path || 
                  (item.path !== '/dashboard' && location.pathname.startsWith(item.path));
                
                return (
                  <li key={item.label}>
                    <button
                      onClick={() => handleMenuItemClick(item.path)}
                      className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all
                        ${isActive 
                          ? 'bg-gradient-to-r from-[#00ff9d]/20 to-[#0ea5e9]/10 text-[#00ff9d] border-l-4 border-[#00ff9d]' 
                          : 'text-gray-400 hover:bg-white/5 hover:text-white'
                        }`}
                    >
                      <i className={`fas ${item.icon} text-lg w-6 text-center`}></i>
                      <span className="font-medium">{item.label}</span>
                    </button>
                  </li>
                );
              })}
            </ul>
          </nav>

          {/* Logout */}
          <div className="p-4 border-t border-white/10">
            <button
              onClick={() => {
                localStorage.removeItem('isLoggedIn');
                window.location.href = '/login';
              }}
              className="w-full flex items-center gap-3 px-3 py-3 rounded-lg text-red-400 hover:bg-red-500/10 transition-colors"
            >
              <i className="fas fa-sign-out-alt text-lg w-6 text-center"></i>
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </motion.div>
    </>
  );
};

export default Sidebar;
