import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const Accounts = () => {
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
          <li className="active"><a href="/accounts"><i className="fas fa-wallet"></i> My Accounts</a></li>
          <li><a href="/buy"><i className="fas fa-shopping-cart"></i> Buy Challenge</a></li>
          <li><a href="/leaderboard"><i className="fas fa-trophy"></i> Leaderboard</a></li>
          <li><a href="/affiliate"><i className="fas fa-users"></i> Affiliate</a></li>
          <li><a href="/certificates"><i className="fas fa-certificate"></i> Certificates</a></li>
          <li><a href="/settings"><i className="fas fa-cog"></i> Settings</a></li>
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

        {/* Accounts Content */}
        <div className="dashboard-container">
          <h1>My Accounts</h1>
          <div className="accounts-grid">
            <div className="account-card">
              <div className="account-header">
                <h3>Account #12345</h3>
                <span className="status-badge active">Active</span>
              </div>
              <div className="account-details">
                <div className="detail-row">
                  <span>Challenge Type:</span>
                  <span>$5K Practice</span>
                </div>
                <div className="detail-row">
                  <span>Balance:</span>
                  <span>$5,000.00</span>
                </div>
                <div className="detail-row">
                  <span>Equity:</span>
                  <span className="positive">$5,123.45</span>
                </div>
                <div className="detail-row">
                  <span>Profit/Loss:</span>
                  <span className="positive">+$123.45</span>
                </div>
                <div className="detail-row">
                  <span>Days Traded:</span>
                  <span>7</span>
                </div>
              </div>
              <div className="account-actions">
                <button className="btn btn-secondary">View Details</button>
                <button className="btn btn-primary">Continue Trading</button>
              </div>
            </div>

            <div className="account-card">
              <div className="account-header">
                <h3>Account #67890</h3>
                <span className="status-badge passed">Passed</span>
              </div>
              <div className="account-details">
                <div className="detail-row">
                  <span>Challenge Type:</span>
                  <span>$10K Practice</span>
                </div>
                <div className="detail-row">
                  <span>Balance:</span>
                  <span>$10,000.00</span>
                </div>
                <div className="detail-row">
                  <span>Equity:</span>
                  <span className="positive">$10,800.00</span>
                </div>
                <div className="detail-row">
                  <span>Profit/Loss:</span>
                  <span className="positive">+$800.00</span>
                </div>
                <div className="detail-row">
                  <span>Days Traded:</span>
                  <span>12</span>
                </div>
              </div>
              <div className="account-actions">
                <button className="btn btn-secondary">View Certificate</button>
                <button className="btn btn-primary">Get Funded</button>
              </div>
            </div>

            <div className="account-card">
              <div className="account-header">
                <h3>Account #11111</h3>
                <span className="status-badge active">Active</span>
              </div>
              <div className="account-details">
                <div className="detail-row">
                  <span>Challenge Type:</span>
                  <span>$25K Practice</span>
                </div>
                <div className="detail-row">
                  <span>Balance:</span>
                  <span>$25,000.00</span>
                </div>
                <div className="detail-row">
                  <span>Equity:</span>
                  <span className="negative">$24,500.00</span>
                </div>
                <div className="detail-row">
                  <span>Profit/Loss:</span>
                  <span className="negative">-$500.00</span>
                </div>
                <div className="detail-row">
                  <span>Days Traded:</span>
                  <span>5</span>
                </div>
              </div>
              <div className="account-actions">
                <button className="btn btn-secondary">View Details</button>
                <button className="btn btn-primary">Continue Trading</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Accounts
