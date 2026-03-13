import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const Settings = () => {
  useEffect(() => {
    useNavigation()
  }, [])

  return (
    <div>
      {/* Sidebar Navigation */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>PropFirm<span className="highlight">Challenge</span></h2>
        </div>
        <ul className="sidebar-menu">
          <li><a href="/dashboard"><i className="fas fa-home"></i> Dashboard</a></li>
          <li><a href="/accounts"><i className="fas fa-wallet"></i> My Accounts</a></li>
          <li><a href="/buy"><i className="fas fa-shopping-cart"></i> Buy Challenge</a></li>
          <li><a href="/leaderboard"><i className="fas fa-trophy"></i> Leaderboard</a></li>
          <li><a href="/affiliate"><i className="fas fa-users"></i> Affiliate</a></li>
          <li><a href="/certificates"><i className="fas fa-certificate"></i> Certificates</a></li>
          <li className="active"><a href="/settings"><i className="fas fa-cog"></i> Settings</a></li>
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
          <div className="account-selector">
            <select>
              <option>Account #12345 - $5K Challenge</option>
              <option>Account #67890 - $10K Challenge</option>
              <option>Account #11111 - $25K Challenge</option>
            </select>
          </div>
          <div className="user-info">
            <i className="fas fa-user-circle"></i>
            <span>John Doe</span>
          </div>
        </div>

        {/* Settings Content */}
        <div className="dashboard-container">
          <h1>Account Settings</h1>
          
          <div className="settings-grid">
            <div className="settings-card">
              <h3>Profile Information</h3>
              <div className="form-group">
                <label>First Name</label>
                <input type="text" defaultValue="John" />
              </div>
              <div className="form-group">
                <label>Last Name</label>
                <input type="text" defaultValue="Doe" />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input type="email" defaultValue="john.doe@example.com" />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input type="tel" defaultValue="+1-555-0123" />
              </div>
            </div>

            <div className="settings-card">
              <h3>Trading Preferences</h3>
              <div className="form-group">
                <label>Default Lot Size</label>
                <select defaultValue="0.1">
                  <option value="0.01">0.01</option>
                  <option value="0.1">0.1</option>
                  <option value="0.5">0.5</option>
                  <option value="1.0">1.0</option>
                </select>
              </div>
              <div className="form-group">
                <label>Stop Loss %</label>
                <input type="number" defaultValue="5" />
              </div>
              <div className="form-group">
                <label>Take Profit %</label>
                <input type="number" defaultValue="10" />
              </div>
            </div>

            <div className="settings-card">
              <h3>Notifications</h3>
              <div className="form-group checkbox-group">
                <input type="checkbox" defaultChecked />
                <label>Email notifications for trades</label>
              </div>
              <div className="form-group checkbox-group">
                <input type="checkbox" defaultChecked />
                <label>Email notifications for account changes</label>
              </div>
              <div className="form-group checkbox-group">
                <input type="checkbox" />
                <label>SMS notifications</label>
              </div>
            </div>
          </div>

          <div className="settings-actions">
            <button className="btn btn-primary">Save Settings</button>
            <button className="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
