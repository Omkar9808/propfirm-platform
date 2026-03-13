import React, { useEffect } from 'react'
import { useScrollReveal, useProgressBars, useCounters, useHoverEffects, useNavigation } from '../hooks/useAnimations'

const Home = () => {
  useEffect(() => {
    // Initialize all animations with timing
    const timer = setTimeout(() => {
      useScrollReveal()
      useProgressBars()
      useCounters()
      useHoverEffects()
      useNavigation()
      
      // Check auth state and update UI
      const isLoggedIn = localStorage.getItem('isLoggedIn')
      
      // Update UI based on auth state
      if (isLoggedIn) {
        const loginLink = document.querySelector('a[href="/login"]')
        if (loginLink) {
          loginLink.textContent = 'Dashboard'
          loginLink.href = '/dashboard'
        }
      } else {
        const dashboardLink = document.querySelector('a[href="/dashboard"]')
        if (dashboardLink) {
          dashboardLink.textContent = 'Login'
          dashboardLink.href = '/login'
        }
      }
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])

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

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="trust-indicator">
            <i className="fas fa-users"></i>
            <span>Join 1,000+ Traders Practicing Today</span>
          </div>
          <h1 className="hero-headline">Prove You Can Trade. Get Funded.</h1>
          <p className="hero-subheadline">Real prop firm rules. Real-time risk tracking. No hidden conditions.</p>
          <div className="hero-buttons">
            <a href="/pricing" className="btn btn-primary btn-glow">Start $5K Challenge Now</a>
            <a href="/rules" className="btn btn-secondary">View Rules</a>
          </div>
        </div>
        <div className="hero-animation">
          <div className="chart-placeholder">
            <div className="floating-stats">
              <div className="stat-item">
                <span className="stat-number">8%</span>
                <span className="stat-label">Profit Target</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">5%</span>
                <span className="stat-label">Daily Loss</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">10%</span>
                <span className="stat-label">Max DD</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <div className="container">
          <h2>How It Works</h2>
          <div className="steps">
            <div className="step-card">
              <div className="step-number">01</div>
              <div className="step-icon">
                <i className="fas fa-shopping-cart"></i>
              </div>
              <h3>Purchase Your Challenge</h3>
              <p>Select your challenge size and get instant access to your trading account</p>
              <a href="/pricing">Learn More</a>
            </div>
            <div className="step-card">
              <div className="step-number">02</div>
              <div className="step-icon">
                <i className="fas fa-chart-line"></i>
              </div>
              <h3>Trade Under Strict Risk Rules</h3>
              <p>Follow real prop firm risk parameters including daily loss limits and drawdown rules</p>
              <a href="/rules">Learn More</a>
            </div>
            <div className="step-card">
              <div className="step-number">03</div>
              <div className="step-icon">
                <i className="fas fa-trophy"></i>
              </div>
              <h3>Pass & Unlock Certification</h3>
              <p>Complete your challenge successfully and unlock certification for funded accounts</p>
              <a href="/dashboard">Get Started</a>
            </div>
          </div>
        </div>
      </section>

      {/* Challenge Models */}
      <section className="challenge-models">
        <div className="container">
          <h2>Challenge Models</h2>
          <div className="models-grid">
            <div className="model-card">
              <h3>$5K Practice</h3>
              <ul>
                <li>Profit Target: <strong>8%</strong></li>
                <li>Max DD: <strong>10%</strong></li>
                <li>Daily Loss: <strong>5%</strong></li>
                <li>Min Trading Days: <strong>3</strong></li>
                <li>Price: <strong>$1</strong></li>
              </ul>
              <button className="btn btn-primary" onClick={() => window.location.href='/pricing'}>Start $5K Challenge</button>
            </div>
            <div className="model-card featured-card">
              <div className="popular-badge">Most Popular</div>
              <h3>$10K Practice</h3>
              <p className="capital-info">$10K simulated capital</p>
              <ul>
                <li>Profit Target: <strong>8%</strong></li>
                <li>Max DD: <strong>10%</strong></li>
                <li>Daily Loss: <strong>5%</strong></li>
                <li>Min Trading Days: <strong>5</strong></li>
                <li>Price: <strong>$2</strong></li>
                <li className="comparison-row"><i className="fas fa-check"></i> Fastest Path to Certification</li>
              </ul>
              <button className="btn btn-primary" onClick={() => window.location.href='/pricing'}>Start $10K Challenge</button>
            </div>
            <div className="model-card">
              <h3>$25K Practice</h3>
              <ul>
                <li>Profit Target: <strong>8%</strong></li>
                <li>Max DD: <strong>10%</strong></li>
                <li>Daily Loss: <strong>5%</strong></li>
                <li>Min Trading Days: <strong>10</strong></li>
                <li>Price: <strong>$5</strong></li>
              </ul>
              <button className="btn btn-primary" onClick={() => window.location.href='/pricing'}>Start $25K Challenge</button>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="why-choose-us">
        <div className="container">
          <h2>Why Choose Us</h2>
          <p className="section-intro">Built for serious traders who want real prop discipline.</p>
          <div className="features-grid">
            <div className="feature-item scroll-reveal">
              <div className="feature-icon">
                <i className="fas fa-ruler-combined"></i>
              </div>
              <h3>Real Prop Rules</h3>
              <p>Experience actual prop firm rules and regulations used by top trading firms worldwide</p>
            </div>
            <div className="feature-item scroll-reveal">
              <div className="feature-icon">
                <i className="fas fa-chart-network"></i>
              </div>
              <h3>Live Dashboard Tracking</h3>
              <p>Monitor your progress in real-time with advanced analytics and performance metrics</p>
            </div>
            <div className="feature-item scroll-reveal">
              <div className="feature-icon">
                <i className="fas fa-bell"></i>
              </div>
              <h3>Instant Rule Detection</h3>
              <p>Get immediate alerts for rule violations so you can adjust your trading strategy instantly</p>
            </div>
            <div className="feature-item scroll-reveal">
              <div className="feature-icon">
                <i className="fas fa-eye-slash"></i>
              </div>
              <h3>No Hidden Conditions</h3>
              <p>Transparent rules with no surprises - what you see is exactly what you get</p>
            </div>
            <div className="feature-item scroll-reveal">
              <div className="feature-icon">
                <i className="fas fa-trophy"></i>
              </div>
              <h3>Leaderboard System</h3>
              <p>Compete with other traders and track your ranking on our global leaderboard</p>
            </div>
            <div className="feature-item scroll-reveal">
              <div className="feature-icon">
                <i className="fas fa-certificate"></i>
              </div>
              <h3>Certification</h3>
              <p>Get certified upon passing your challenge and unlock opportunities for funded accounts</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="testimonials">
        <div className="container">
          <h2>What Our Traders Say</h2>
          <div className="testimonial-carousel">
            <div className="testimonial-track">
              <div className="testimonial-card">
                <div className="rating">
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                </div>
                <p>"Passed my $5K challenge in just 2 weeks! The real-time tracking helped me stay disciplined."</p>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="fas fa-user"></i>
                  </div>
                  <div className="author-info">
                    <h4>John D. <i className="fas fa-check-circle verified-badge"></i></h4>
                    <p className="author-stat">Passed $5K Challenge in 14 days</p>
                  </div>
                </div>
              </div>
              <div className="testimonial-card">
                <div className="rating">
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                </div>
                <p>"The best simulation of a real prop firm. The rules are challenging but fair."</p>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="fas fa-user"></i>
                  </div>
                  <div className="author-info">
                    <h4>Sarah M. <i className="fas fa-check-circle verified-badge"></i></h4>
                    <p className="author-stat">Passed $10K Challenge in 21 days</p>
                  </div>
                </div>
              </div>
              <div className="testimonial-card">
                <div className="rating">
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star-half-alt"></i>
                </div>
                <p>"Great platform to practice risk management. Highly recommend for serious traders."</p>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="fas fa-user"></i>
                  </div>
                  <div className="author-info">
                    <h4>Mike R. <i className="fas fa-check-circle verified-badge"></i></h4>
                    <p className="author-stat">Passed $25K Challenge in 30 days</p>
                  </div>
                </div>
              </div>
              <div className="testimonial-card">
                <div className="rating">
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                  <i className="fas fa-star"></i>
                </div>
                <p>"The transparency and real-time feedback made all the difference in my trading journey."</p>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    <i className="fas fa-user"></i>
                  </div>
                  <div className="author-info">
                    <h4>Emily K. <i className="fas fa-check-circle verified-badge"></i></h4>
                    <p className="author-stat">Passed $5K Challenge in 10 days</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Preview */}
      <section className="faq-preview">
        <div className="container">
          <h2>Frequently Asked Questions</h2>
          <div className="faq-list">
            <div className="faq-item">
              <div className="faq-header">
                <h3>What are the challenge rules?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>All challenges follow real prop firm rules including profit targets, daily loss limits, and max drawdown restrictions.</p>
              </div>
            </div>
            <div className="faq-item">
              <div className="faq-header">
                <h3>Is this a real funded account?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>This is a simulated trading platform designed to prepare you for real prop firm challenges. Upon passing, you'll receive certification that can help you transition to funded accounts.</p>
              </div>
            </div>
            <div className="faq-item">
              <div className="faq-header">
                <h3>How long do I have to complete a challenge?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>You have unlimited time to complete your challenge, but must meet minimum trading days requirements.</p>
              </div>
            </div>
            <div className="faq-item">
              <div className="faq-header">
                <h3>Is challenge refundable?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>Challenge fees are non-refundable once purchased. However, you can retake the challenge at a discounted rate if needed.</p>
              </div>
            </div>
            <div className="faq-item">
              <div className="faq-header">
                <h3>Can I trade any market?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>You can trade most forex pairs and major indices, with some restrictions on exotic pairs and news events.</p>
              </div>
            </div>
            <div className="faq-item">
              <div className="faq-header">
                <h3>Who is this for?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>This platform is designed for aspiring prop traders who want to practice under real prop firm conditions before risking significant capital.</p>
              </div>
            </div>
            <div className="faq-item">
              <div className="faq-header">
                <h3>What happens after I pass?</h3>
                <i className="fas fa-chevron-down faq-icon"></i>
              </div>
              <div className="faq-content">
                <p>Upon passing, you'll receive a certification and can move to higher-tier challenges or funded accounts.</p>
              </div>
            </div>
          </div>
          <button className="btn btn-secondary" onClick={() => window.location.href='/faq'}>View All FAQs</button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card scroll-reveal">
              <div className="stat-number" data-target="1000">0</div>
              <div className="stat-label">Active Traders</div>
            </div>
            <div className="stat-card scroll-reveal">
              <div className="stat-number" data-target="87">0</div>
              <div className="stat-label">Success Rate %</div>
            </div>
            <div className="stat-card scroll-reveal">
              <div className="stat-number" data-target="50000">0</div>
              <div className="stat-label">Total Trades</div>
            </div>
            <div className="stat-card scroll-reveal">
              <div className="stat-number" data-target="24">0</div>
              <div className="stat-label">Countries</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2>Ready to Prove Your Trading Skills?</h2>
          <p>Join thousands of traders who have successfully passed their challenges and are now trading with real capital</p>
          <a href="/pricing" className="btn btn-primary btn-large">Start Your Challenge Today</a>
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
                <li><a href="/refund-policy">Refund Policy</a></li>
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
              <p className="contact-email">support@propfirmchallenge.com</p>
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

export default Home
