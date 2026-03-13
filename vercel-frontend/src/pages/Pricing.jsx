import React, { useEffect } from 'react'
import { useNavigation, useScrollReveal, useHoverEffects } from '../hooks/useAnimations'

const Pricing = () => {
  useEffect(() => {
    const timer = setTimeout(() => {
      useNavigation()
      useScrollReveal()
      useHoverEffects()
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])

  const buyChallenge = (type) => {
    // Check if user is logged in
    const isLoggedIn = localStorage.getItem('isLoggedIn')
    
    if (!isLoggedIn) {
      // Redirect to login if not logged in
      window.location.href = '/login'
    } else {
      // Redirect to checkout if logged in
      window.location.href = '/checkout?challenge=' + type
    }
  }

  return (
    <div>
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="logo">
            <h2>PropFirm<span className="highlight">Challenge</span></h2>
          </div>
          <ul className="nav-menu">
            <li><a href="/">Home</a></li>
            <li><a href="/pricing">Pricing</a></li>
            <li><a href="/rules">Rules</a></li>
            <li><a href="/leaderboard">Leaderboard</a></li>
            <li><a href="/login">Login</a></li>
          </ul>
          <div className="hamburger">
            <span className="bar"></span>
            <span className="bar"></span>
            <span className="bar"></span>
          </div>
        </div>
      </nav>

      {/* Pricing Banner */}
      <section className="pricing-banner">
        <div className="container">
          <h1>Choose Your Challenge</h1>
          <p>Select the perfect challenge level to start your prop trading journey</p>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="pricing-section">
        <div className="container">
          <div className="pricing-cards">
            <div className="pricing-card">
              <div className="pricing-header">
                <h3>$5K Practice</h3>
                <div className="price">$1</div>
              </div>
              <div className="pricing-details">
                <ul>
                  <li>Account Balance: <strong>$5,000</strong></li>
                  <li>Profit Target: <strong>8%</strong></li>
                  <li>Daily Loss Limit: <strong>5%</strong></li>
                  <li>Max Drawdown: <strong>10%</strong></li>
                  <li>Min Trading Days: <strong>3</strong></li>
                  <li>Account Type: <strong>Standard</strong></li>
                </ul>
              </div>
              <button className="btn btn-primary" onClick={() => buyChallenge('5k')}>Buy Now</button>
            </div>

            <div className="pricing-card featured">
              <div className="popular-tag">POPULAR</div>
              <div className="pricing-header">
                <h3>$10K Practice</h3>
                <div className="price">$2</div>
              </div>
              <div className="pricing-details">
                <ul>
                  <li>Account Balance: <strong>$10,000</strong></li>
                  <li>Profit Target: <strong>8%</strong></li>
                  <li>Daily Loss Limit: <strong>5%</strong></li>
                  <li>Max Drawdown: <strong>10%</strong></li>
                  <li>Min Trading Days: <strong>5</strong></li>
                  <li>Account Type: <strong>Advanced</strong></li>
                </ul>
              </div>
              <button className="btn btn-primary" onClick={() => buyChallenge('10k')}>Buy Now</button>
            </div>

            <div className="pricing-card">
              <div className="pricing-header">
                <h3>$25K Practice</h3>
                <div className="price">$5</div>
              </div>
              <div className="pricing-details">
                <ul>
                  <li>Account Balance: <strong>$25,000</strong></li>
                  <li>Profit Target: <strong>8%</strong></li>
                  <li>Daily Loss Limit: <strong>5%</strong></li>
                  <li>Max Drawdown: <strong>10%</strong></li>
                  <li>Min Trading Days: <strong>10</strong></li>
                  <li>Account Type: <strong>Professional</strong></li>
                </ul>
              </div>
              <button className="btn btn-primary" onClick={() => buyChallenge('25k')}>Buy Now</button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="comparison-section">
        <div className="container">
          <h2>Feature Comparison</h2>
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Features</th>
                  <th>$5K Challenge</th>
                  <th>$10K Challenge</th>
                  <th>$25K Challenge</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Account Balance</td>
                  <td>$5,000</td>
                  <td>$10,000</td>
                  <td>$25,000</td>
                </tr>
                <tr>
                  <td>Profit Target</td>
                  <td>8%</td>
                  <td>8%</td>
                  <td>8%</td>
                </tr>
                <tr>
                  <td>Daily Loss Limit</td>
                  <td>5%</td>
                  <td>5%</td>
                  <td>5%</td>
                </tr>
                <tr>
                  <td>Max Drawdown</td>
                  <td>10%</td>
                  <td>10%</td>
                  <td>10%</td>
                </tr>
                <tr>
                  <td>Min Trading Days</td>
                  <td>3</td>
                  <td>5</td>
                  <td>10</td>
                </tr>
                <tr>
                  <td>Advanced Analytics</td>
                  <td><i className="fas fa-times"></i></td>
                  <td><i className="fas fa-check"></i></td>
                  <td><i className="fas fa-check"></i></td>
                </tr>
                <tr>
                  <td>Priority Support</td>
                  <td><i className="fas fa-times"></i></td>
                  <td><i className="fas fa-check"></i></td>
                  <td><i className="fas fa-check"></i></td>
                </tr>
                <tr>
                  <td>Certificate of Completion</td>
                  <td><i className="fas fa-check"></i></td>
                  <td><i className="fas fa-check"></i></td>
                  <td><i className="fas fa-check"></i></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2>Ready to Start Your Challenge?</h2>
          <p>Choose your challenge level and begin your journey to becoming a funded trader</p>
          <a href="/pricing" className="btn btn-primary btn-large">Get Started Now</a>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h3>PropFirm<span className="highlight">Challenge</span></h3>
              <p>Practice like a real prop trader. Pass with confidence.</p>
            </div>
            <div className="footer-section">
              <h4>Quick Links</h4>
              <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/pricing">Pricing</a></li>
                <li><a href="/rules">Rules</a></li>
                <li><a href="/leaderboard">Leaderboard</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Support</h4>
              <ul>
                <li><a href="/faq">FAQ</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/terms">Terms</a></li>
                <li><a href="/privacy">Privacy</a></li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Social</h4>
              <div className="social-links">
                <a href="#" className="social-link"><i className="fab fa-discord"></i> Discord</a>
                <a href="#" className="social-link"><i className="fab fa-twitter"></i> Twitter</a>
                <a href="#" className="social-link"><i className="fab fa-youtube"></i> YouTube</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2026 PropFirmChallenge. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Scripts */}
      <script src="/public/js/main.js"></script>
    </div>
  )
}

export default Pricing
