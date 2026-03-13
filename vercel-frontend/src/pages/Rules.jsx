import React, { useState, useEffect } from 'react'
import { useNavigation, useScrollReveal } from '../hooks/useAnimations'

const Rules = () => {
  const [activeAccordion, setActiveAccordion] = useState(null)

  useEffect(() => {
    const timer = setTimeout(() => {
      useNavigation()
      useScrollReveal()
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])

  const toggleAccordion = (index) => {
    const newActive = activeAccordion === index ? null : index
    setActiveAccordion(newActive)
    
    // Handle accordion toggle - use setTimeout to ensure DOM is ready
    setTimeout(() => {
      const content = document.querySelectorAll('.accordion-content')[index]
      const icon = document.querySelectorAll('.accordion-header i')[index]
      
      if (content && icon) {
        if (newActive !== null) {
          content.style.display = 'block'
          icon.style.transform = 'rotate(180deg)'
        } else {
          content.style.display = 'none'
          icon.style.transform = 'rotate(0deg)'
        }
      }
      
      // Close all other accordions
      document.querySelectorAll('.accordion-content').forEach((otherContent, otherIndex) => {
        if (otherIndex !== index) {
          otherContent.style.display = 'none'
        }
      })
      
      document.querySelectorAll('.accordion-header i').forEach((otherIcon, otherIndex) => {
        if (otherIndex !== index) {
          otherIcon.style.transform = 'rotate(0deg)'
        }
      })
    }, 50)
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

      {/* Rules Banner */}
      <section className="rules-banner">
        <div className="container">
          <h1>Challenge Rules</h1>
          <p>Understand the rules and guidelines for successful challenge completion</p>
        </div>
      </section>

      {/* Rules Sections */}
      <section className="rules-section">
        <div className="container">
          <div className="rules-accordion">
            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(0)}>
                <h3>Profit Target</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>All challenges require achieving an 8% profit target based on your account balance.</p>
                <ul>
                  <li>Profit must be calculated based on floating P&L at the end of each trading day</li>
                  <li>Minimum trading days must be met before profit target can be achieved</li>
                  <li>Profit target is calculated as (Equity - Initial Balance) / Initial Balance * 100</li>
                  <li>Once profit target is reached, the challenge is considered passed</li>
                </ul>
              </div>
            </div>

            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(1)}>
                <h3>Daily Drawdown</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>Daily drawdown limit is 5% of your account balance.</p>
                <ul>
                  <li>Daily drawdown is calculated as (Highest Equity of Day - Current Equity) / Highest Equity of Day * 100</li>
                  <li>If daily drawdown exceeds 5%, the challenge is failed</li>
                  <li>Daily drawdown resets at the start of each trading day</li>
                  <li>Highest equity of the day is tracked from 00:00 to 23:59 server time</li>
                </ul>
              </div>
            </div>

            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(2)}>
                <h3>Maximum Drawdown</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>Maximum drawdown limit is 10% of your account balance.</p>
                <ul>
                  <li>Max drawdown is calculated as (Initial Balance - Lowest Equity) / Initial Balance * 100</li>
                  <li>If max drawdown exceeds 10%, the challenge is failed</li>
                  <li>This is measured from account opening until challenge completion</li>
                  <li>Max drawdown is not reset during the challenge period</li>
                </ul>
              </div>
            </div>

            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(3)}>
                <h3>Lot Size Rules</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>Adhere to maximum lot size restrictions for each instrument.</p>
                <ul>
                  <li>Major currency pairs (EURUSD, GBPUSD, USDJPY, etc.): Maximum 1.0 lot per position</li>
                  <li>Minor currency pairs: Maximum 0.5 lot per position</li>
                  <li>Indices: Maximum 0.2 lot per position</li>
                  <li>Commodities: Maximum 0.5 lot per position</li>
                  <li>No hedging allowed (opening opposite positions on the same instrument)</li>
                </ul>
              </div>
            </div>

            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(4)}>
                <h3>News Trading Restrictions</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>Certain high-impact news events are restricted for trading.</p>
                <ul>
                  <li>No trading 30 minutes before and after major economic news releases</li>
                  <li>Restricted news events include NFP, CPI, FOMC decisions, ECB meetings</li>
                  <li>Full list of restricted events available in the trader portal</li>
                  <li>Violating news restrictions results in immediate challenge failure</li>
                </ul>
              </div>
            </div>

            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(5)}>
                <h3>Prohibited Strategies</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>These strategies are not allowed during the challenge:</p>
                <ul>
                  <li>Copying trades from other traders or using copy trading services</li>
                  <li>Using automated trading systems or expert advisors</li>
                  <li>Hedging the same instrument with opposing positions</li>
                  <li>Opening multiple positions that net to zero risk</li>
                  <li>Intentionally causing losses to reset daily drawdown</li>
                  <li>Trading during restricted news times</li>
                </ul>
              </div>
            </div>

            <div className="accordion-item">
              <div className="accordion-header" onClick={() => toggleAccordion(6)}>
                <h3>Account Termination</h3>
                <i className="fas fa-chevron-down"></i>
              </div>
              <div className="accordion-content">
                <p>Conditions that lead to account termination:</p>
                <ul>
                  <li>Exceeding daily drawdown limit (5%)</li>
                  <li>Exceeding maximum drawdown limit (10%)</li>
                  <li>Using prohibited trading strategies</li>
                  <li>Trading during restricted news periods</li>
                  <li>Violating lot size restrictions</li>
                  <li>Any form of account manipulation or cheating</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Reference */}
      <section className="quick-reference">
        <div className="container">
          <h2>Quick Reference</h2>
          <div className="reference-grid">
            <div className="reference-card">
              <h3>Profit Target</h3>
              <div className="ref-value">8%</div>
            </div>
            <div className="reference-card">
              <h3>Daily Loss Limit</h3>
              <div className="ref-value">5%</div>
            </div>
            <div className="reference-card">
              <h3>Max Drawdown</h3>
              <div className="ref-value">10%</div>
            </div>
            <div className="reference-card">
              <h3>Min Trading Days</h3>
              <div className="ref-value">3-10</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2>Ready to Start Your Challenge?</h2>
          <p>Review the rules carefully and begin your journey to becoming a funded trader</p>
          <a href="/pricing" className="btn btn-primary btn-large">Start Your Challenge</a>
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

export default Rules
