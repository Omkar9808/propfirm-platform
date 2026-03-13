import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const Certificates = () => {
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
          <li className="active"><a href="/certificates"><i className="fas fa-certificate"></i> Certificates</a></li>
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

        {/* Certificates Content */}
        <div className="dashboard-container">
          <h1>Your Certificates</h1>
          
          <div className="certificates-grid">
            <div className="certificate-card">
              <div className="certificate-header">
                <h3>$10K Challenge Certificate</h3>
                <span className="status-badge passed">Passed</span>
              </div>
              <div className="certificate-details">
                <div className="detail-row">
                  <span>Certificate ID:</span>
                  <span>CERT-2026-001</span>
                </div>
                <div className="detail-row">
                  <span>Issue Date:</span>
                  <span>March 15, 2026</span>
                </div>
                <div className="detail-row">
                  <span>Account ID:</span>
                  <span>#67890</span>
                </div>
                <div className="detail-row">
                  <span>Final Profit:</span>
                  <span className="positive">+$800.00</span>
                </div>
                <div className="detail-row">
                  <span>Win Rate:</span>
                  <span>72%</span>
                </div>
              </div>
              <div className="certificate-actions">
                <button className="btn btn-primary">Download PDF</button>
                <button className="btn btn-secondary">Share</button>
              </div>
            </div>

            <div className="certificate-card">
              <div className="certificate-header">
                <h3>$5K Challenge Certificate</h3>
                <span className="status-badge passed">Passed</span>
              </div>
              <div className="certificate-details">
                <div className="detail-row">
                  <span>Certificate ID:</span>
                  <span>CERT-2026-002</span>
                </div>
                <div className="detail-row">
                  <span>Issue Date:</span>
                  <span>March 10, 2026</span>
                </div>
                <div className="detail-row">
                  <span>Account ID:</span>
                  <span>#12345</span>
                </div>
                <div className="detail-row">
                  <span>Final Profit:</span>
                  <span className="positive">+$400.00</span>
                </div>
                <div className="detail-row">
                  <span>Win Rate:</span>
                  <span>68%</span>
                </div>
              </div>
              <div className="certificate-actions">
                <button className="btn btn-primary">Download PDF</button>
                <button className="btn btn-secondary">Share</button>
              </div>
            </div>
          </div>

          <div className="certificates-info">
            <h3>About Your Certificates</h3>
            <p>Your certificates verify your successful completion of our prop firm challenges. Each certificate includes:</p>
            <ul>
              <li>Official certificate ID and verification code</li>
              <li>Challenge completion details and metrics</li>
              <li>Performance statistics and win rate</li>
              <li>Digital signature and issue date</li>
              <li>Shareable PDF format for LinkedIn and resume</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Certificates
