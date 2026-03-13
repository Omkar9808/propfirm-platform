import React, { useEffect } from 'react'
import { useNavigation } from '../../hooks/useAnimations'

const Buy = () => {
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
          <li className="active"><a href="/buy"><i className="fas fa-shopping-cart"></i> Buy Challenge</a></li>
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

        {/* Buy Challenge Content */}
        <div className="dashboard-container">
          <h1>Buy New Challenge</h1>
          
          <div className="buy-overview">
            <div className="overview-card">
              <h3>Available Challenges</h3>
              <p>Choose your next challenge level and continue your prop trading journey.</p>
              
              <div className="challenge-options">
                <div className="challenge-card">
                  <div className="challenge-header">
                    <h3>$5K Practice</h3>
                    <div className="challenge-price">$1.00</div>
                  </div>
                  <div className="challenge-features">
                    <ul>
                      <li><i className="fas fa-check"></i> $5,000 Account Balance</li>
                      <li><i className="fas fa-check"></i> 8% Profit Target</li>
                      <li><i className="fas fa-check"></i> 5% Daily Loss Limit</li>
                      <li><i className="fas fa-check"></i> 10% Max Drawdown</li>
                      <li><i className="fas fa-check"></i> 3 Minimum Trading Days</li>
                    </ul>
                  </div>
                  <div className="challenge-action">
                    <a href="/checkout?challenge=5k" className="btn btn-primary">Buy Now</a>
                  </div>
                </div>

                <div className="challenge-card featured">
                  <div className="popular-badge">POPULAR</div>
                  <div className="challenge-header">
                    <h3>$10K Practice</h3>
                    <div className="challenge-price">$2.00</div>
                  </div>
                  <div className="challenge-features">
                    <ul>
                      <li><i className="fas fa-check"></i> $10,000 Account Balance</li>
                      <li><i className="fas fa-check"></i> 8% Profit Target</li>
                      <li><i className="fas fa-check"></i> 5% Daily Loss Limit</li>
                      <li><i className="fas fa-check"></i> 10% Max Drawdown</li>
                      <li><i className="fas fa-check"></i> 5 Minimum Trading Days</li>
                    </ul>
                  </div>
                  <div className="challenge-action">
                    <a href="/checkout?challenge=10k" className="btn btn-primary">Buy Now</a>
                  </div>
                </div>

                <div className="challenge-card">
                  <div className="challenge-header">
                    <h3>$25K Practice</h3>
                    <div className="challenge-price">$5.00</div>
                  </div>
                  <div className="challenge-features">
                    <ul>
                      <li><i className="fas fa-check"></i> $25,000 Account Balance</li>
                      <li><i className="fas fa-check"></i> 8% Profit Target</li>
                      <li><i className="fas fa-check"></i> 5% Daily Loss Limit</li>
                      <li><i className="fas fa-check"></i> 10% Max Drawdown</li>
                      <li><i className="fas fa-check"></i> 10 Minimum Trading Days</li>
                    </ul>
                  </div>
                  <div className="challenge-action">
                    <a href="/checkout?challenge=25k" className="btn btn-primary">Buy Now</a>
                  </div>
                </div>
              </div>
            </div>

            <div className="overview-card">
              <h3>Payment Methods</h3>
              <div className="payment-methods">
                <div className="payment-method">
                  <i className="fab fa-cc-visa"></i>
                  <span>Credit/Debit Card</span>
                </div>
                <div className="payment-method">
                  <i className="fab fa-paypal"></i>
                  <span>PayPal</span>
                </div>
                <div className="payment-method">
                  <i className="fab fa-cc-stripe"></i>
                  <span>Stripe</span>
                </div>
                <div className="payment-method">
                  <i className="fab fa-bitcoin"></i>
                  <span>Cryptocurrency</span>
                </div>
              </div>
            </div>

            <div className="overview-card">
              <h3>Special Offers</h3>
              <div className="offers-grid">
                <div className="offer-item">
                  <div className="offer-badge">LIMITED TIME</div>
                  <h4>Bundle Deal</h4>
                  <p>Buy any 2 challenges, get 50% off the 3rd!</p>
                  <button className="btn btn-secondary">Learn More</button>
                </div>
                <div className="offer-item">
                  <div className="offer-badge">NEW</div>
                  <h4>Student Discount</h4>
                  <p>25% off for verified students</p>
                  <button className="btn btn-secondary">Verify Status</button>
                </div>
              </div>
            </div>
          </div>

          <div className="buy-actions">
            <button className="btn btn-primary btn-large">View All Pricing</button>
            <button className="btn btn-secondary">Contact Support</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Buy
