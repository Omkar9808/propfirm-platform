import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const AdminDashboard = () => {
  useEffect(() => {
    useNavigation()
  }, [])

  return (
    <div>
      {/* Admin Sidebar Navigation */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>PropFirm<span className="highlight">Admin</span></h2>
        </div>
        <ul className="sidebar-menu">
          <li className="active"><a href="/admin"><i className="fas fa-tachometer-alt"></i> Dashboard</a></li>
          <li><a href="/admin/users"><i className="fas fa-users"></i> Users</a></li>
          <li><a href="/admin/accounts"><i className="fas fa-wallet"></i> Accounts</a></li>
          <li><a href="/admin/payments"><i className="fas fa-credit-card"></i> Payments</a></li>
          <li><a href="/admin/challenges"><i className="fas fa-trophy"></i> Challenges</a></li>
          <li><a href="/admin/risk-monitor"><i className="fas fa-exclamation-triangle"></i> Risk Monitor</a></li>
          <li><a href="/admin/analytics"><i className="fas fa-chart-line"></i> Analytics</a></li>
          <li><a href="/admin/violations"><i className="fas fa-times-circle"></i> Violations</a></li>
          <li><a href="/admin/settings"><i className="fas fa-cog"></i> Settings</a></li>
          <li><a href="#" onClick={() => {
            localStorage.removeItem('isLoggedIn')
            localStorage.removeItem('userEmail')
            localStorage.removeItem('userName')
            window.location.href = '/login'
          }}><i className="fas fa-sign-out-alt"></i> Logout</a></li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Top Bar */}
        <div className="top-bar">
          <div className="menu-toggle">
            <i className="fas fa-bars"></i>
          </div>
          <div className="user-info">
            <i className="fas fa-user-shield"></i>
            <span>Admin User</span>
          </div>
        </div>

        {/* Admin Dashboard Content */}
        <div className="dashboard-container">
          <h1>Admin Dashboard</h1>
          
          <div className="admin-stats">
            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-users"></i>
              </div>
              <div className="stat-info">
                <h3>Total Users</h3>
                <span className="stat-number">1,247</span>
                <span className="stat-change positive">+12.5%</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-wallet"></i>
              </div>
              <div className="stat-info">
                <h3>Active Challenges</h3>
                <span className="stat-number">892</span>
                <span className="stat-change positive">+8.3%</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-trophy"></i>
              </div>
              <div className="stat-info">
                <h3>Passed Challenges</h3>
                <span className="stat-number">342</span>
                <span className="stat-change positive">+15.7%</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-dollar-sign"></i>
              </div>
              <div className="stat-info">
                <h3>Total Revenue</h3>
                <span className="stat-number">$24,567</span>
                <span className="stat-change positive">+23.4%</span>
              </div>
            </div>
          </div>

          <div className="admin-grid">
            <div className="admin-card">
              <h3>Recent Users</h3>
              <div className="user-list">
                <div className="user-item">
                  <span className="user-name">John Doe</span>
                  <span className="user-email">john@example.com</span>
                  <span className="user-time">2 hours ago</span>
                </div>
                <div className="user-item">
                  <span className="user-name">Jane Smith</span>
                  <span className="user-email">jane@example.com</span>
                  <span className="user-time">5 hours ago</span>
                </div>
                <div className="user-item">
                  <span className="user-name">Mike Johnson</span>
                  <span className="user-email">mike@example.com</span>
                  <span className="user-time">1 day ago</span>
                </div>
              </div>
            </div>

            <div className="admin-card">
              <h3>System Alerts</h3>
              <div className="alert-list">
                <div className="alert-item warning">
                  <i className="fas fa-exclamation-triangle"></i>
                  <span>High server load detected</span>
                  <span className="alert-time">15 min ago</span>
                </div>
                <div className="alert-item info">
                  <i className="fas fa-info-circle"></i>
                  <span>New user registration spike</span>
                  <span className="alert-time">1 hour ago</span>
                </div>
                <div className="alert-item success">
                  <i className="fas fa-check-circle"></i>
                  <span>Payment processor working normally</span>
                  <span className="alert-time">2 hours ago</span>
                </div>
              </div>
            </div>

            <div className="admin-card">
              <h3>Quick Actions</h3>
              <div className="action-list">
                <button className="btn btn-secondary">View All Users</button>
                <button className="btn btn-secondary">Monitor Challenges</button>
                <button className="btn btn-secondary">Check Payments</button>
                <button className="btn btn-secondary">System Settings</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard
