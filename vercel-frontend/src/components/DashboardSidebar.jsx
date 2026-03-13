import React from 'react'
import { NavLink } from 'react-router-dom'

const DashboardSidebar = () => {
  const navItems = [
    { path: '/dashboard', name: 'Overview', icon: '📊' },
    { path: '/dashboard/accounts', name: 'Accounts', icon: '💼' },
    { path: '/dashboard/account-detail', name: 'Account Detail', icon: '📈' },
    { path: '/dashboard/buy', name: 'Buy Challenge', icon: '🛒' },
    { path: '/dashboard/certificates', name: 'Certificates', icon: '🏆' },
    { path: '/dashboard/affiliate', name: 'Affiliate', icon: '🤝' },
    { path: '/dashboard/settings', name: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="w-64 bg-white shadow-sm h-screen sticky top-0">
      <nav className="mt-8">
        <div className="px-4 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-700'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
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

export default DashboardSidebar
