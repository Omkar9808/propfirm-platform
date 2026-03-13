import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const AccountDetail = () => {
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

        {/* Account Detail Content */}
        <div className="dashboard-container">
          <h1>Account Details - #12345</h1>
          
          <div className="account-overview">
            <div className="overview-card">
              <h3>Account Information</h3>
              <div className="info-grid">
                <div className="info-item">
                  <span className="label">Account ID:</span>
                  <span className="value">#12345</span>
                </div>
                <div className="info-item">
                  <span className="label">Challenge Type:</span>
                  <span className="value">$5K Practice</span>
                </div>
                <div className="info-item">
                  <span className="label">Status:</span>
                  <span className="value status-badge active">Active</span>
                </div>
                <div className="info-item">
                  <span className="label">Start Date:</span>
                  <span className="value">March 1, 2026</span>
                </div>
              </div>
            </div>

            <div className="overview-card">
              <h3>Performance Metrics</h3>
              <div className="metrics-grid">
                <div className="metric-item">
                  <span className="label">Current Balance:</span>
                  <span className="value">$5,000.00</span>
                </div>
                <div className="metric-item">
                  <span className="label">Current Equity:</span>
                  <span className="value positive">$5,123.45</span>
                </div>
                <div className="metric-item">
                  <span className="label">Floating P&L:</span>
                  <span className="value positive">+$123.45</span>
                </div>
                <div className="metric-item">
                  <span className="label">Daily Loss:</span>
                  <span className="value">2.3% / 5%</span>
                </div>
                <div className="metric-item">
                  <span className="label">Max Drawdown:</span>
                  <span className="value">1.8% / 10%</span>
                </div>
                <div className="metric-item">
                  <span className="label">Profit Target:</span>
                  <span className="value">2.5% / 8%</span>
                </div>
                <div className="metric-item">
                  <span className="label">Days Traded:</span>
                  <span className="value">7 / 3 min</span>
                </div>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="charts-section">
            <h2>Performance Charts</h2>
            <div className="charts-grid">
              <div className="chart-container">
                <h3>Equity Curve</h3>
                <div className="chart-placeholder">
                  <canvas width="400" height="200"></canvas>
                </div>
              </div>
              <div className="chart-container">
                <h3>Balance History</h3>
                <div className="chart-placeholder">
                  <canvas width="400" height="200"></canvas>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Trades */}
          <div className="trades-section">
            <h2>Recent Trades</h2>
            <div className="trades-table-container">
              <table className="trades-table">
                <thead>
                  <tr>
                    <th>Ticket</th>
                    <th>Symbol</th>
                    <th>Lot</th>
                    <th>Profit</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>#1234567</td>
                    <td>EURUSD</td>
                    <td>0.1</td>
                    <td className="positive">+$23.45</td>
                    <td>10:23:45</td>
                  </tr>
                  <tr>
                    <td>#1234566</td>
                    <td>GBPUSD</td>
                    <td>0.1</td>
                    <td className="negative">-$12.34</td>
                    <td>09:45:12</td>
                  </tr>
                  <tr>
                    <td>#1234565</td>
                    <td>USDJPY</td>
                    <td>0.2</td>
                    <td className="positive">+$34.56</td>
                    <td>08:32:10</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="actions-section">
            <div className="actions-grid">
              <button className="btn btn-primary">Continue Trading</button>
              <button className="btn btn-secondary">Download Statement</button>
              <button className="btn btn-secondary">View Certificate</button>
            </div>
          </div>
        </div>
      </div>

      {/* Scripts */}
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </div>
  )
}

export default AccountDetail
