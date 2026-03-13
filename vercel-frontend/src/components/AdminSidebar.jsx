import React from 'react'
import { NavLink } from 'react-router-dom'

const AdminSidebar = () => {
  const navItems = [
    { path: '/admin', name: 'Dashboard', icon: '📊' },
    { path: '/admin/users', name: 'Users', icon: '👥' },
    { path: '/admin/accounts', name: 'Accounts', icon: '💼' },
    { path: '/admin/payments', name: 'Payments', icon: '💳' },
    { path: '/admin/challenges', name: 'Challenges', icon: '🎯' },
    { path: '/admin/risk-monitor', name: 'Risk Monitor', icon: '⚠️' },
    { path: '/admin/analytics', name: 'Analytics', icon: '📈' },
    { path: '/admin/violations', name: 'Violations', icon: '🚫' },
    { path: '/admin/settings', name: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="w-64 bg-gray-900 text-white h-screen sticky top-0">
      <nav className="mt-8">
        <div className="px-4 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-red-600 text-white border-r-4 border-red-400'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              <span className="mr-3 text-lg">{item.icon}</span>
              {item.name}
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  )
}

export default AdminSidebar
