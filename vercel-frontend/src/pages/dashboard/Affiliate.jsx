import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const Affiliate = () => {
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
          <li className="active"><a href="/affiliate"><i className="fas fa-users"></i> Affiliate</a></li>
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

        {/* Affiliate Content */}
        <div className="dashboard-container">
          <h1>Affiliate Program</h1>
          
          <div className="affiliate-overview">
            <div className="overview-card">
              <h3>Your Affiliate Stats</h3>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="label">Total Referrals:</span>
                  <span className="value">15</span>
                </div>
                <div className="stat-item">
                  <span className="label">Active Referrals:</span>
                  <span className="value">8</span>
                </div>
                <div className="stat-item">
                  <span className="label">Total Earnings:</span>
                  <span className="value">$750.00</span>
                </div>
                <div className="stat-item">
                  <span className="label">Pending Payouts:</span>
                  <span className="value">$125.00</span>
                </div>
              </div>
            </div>

            <div className="overview-card">
              <h3>Affiliate Links</h3>
              <div className="affiliate-links">
                <div className="link-item">
                  <span className="link-url">https://propfirm.com/ref/johndoe</span>
                  <button className="btn btn-secondary">Copy Link</button>
                </div>
                <div className="link-item">
                  <span className="link-url">https://propfirm.com/ref/johndoe-premium</span>
                  <button className="btn btn-secondary">Copy Link</button>
                </div>
              </div>
            </div>

            <div className="overview-card">
              <h3>Commission Structure</h3>
              <div className="commission-table">
                <table>
                  <thead>
                    <tr>
                      <th>Challenge Type</th>
                      <th>Commission Rate</th>
                      <th>Your Earning</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>$5K Challenge</td>
                      <td>10%</td>
                      <td>$0.10</td>
                    </tr>
                    <tr>
                      <td>$10K Challenge</td>
                      <td>10%</td>
                      <td>$0.20</td>
                    </tr>
                    <tr>
                      <td>$25K Challenge</td>
                      <td>10%</td>
                      <td>$0.50</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="affiliate-actions">
            <button className="btn btn-primary">Request Payout</button>
            <button className="btn btn-secondary">View History</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Affiliate
