import React, { useState, useEffect } from 'react'
import { useNavigation, useScrollReveal, useHoverEffects } from '../hooks/useAnimations'

const Leaderboard = () => {
  const [filter, setFilter] = useState('all')
  const [sortBy, setSortBy] = useState('rank')

  useEffect(() => {
    const timer = setTimeout(() => {
      useNavigation()
      useScrollReveal()
      useHoverEffects()
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])

  const handleFilterChange = (e) => {
    setFilter(e.target.value)
    console.log('Filtering by challenge type:', e.target.value)
  }

  const handleSortChange = (e) => {
    setSortBy(e.target.value)
    console.log('Sorting by:', e.target.value)
  }

  const leaderboardData = [
    {
      rank: 1,
      username: 'TradingMaster',
      challenge: '$25K',
      profit: '+12.5%',
      winRate: '78%',
      status: 'Passed',
      trades: 142
    },
    {
      rank: 2,
      username: 'ForexKing',
      challenge: '$10K',
      profit: '+9.8%',
      winRate: '72%',
      status: 'Passed',
      trades: 98
    },
    {
      rank: 3,
      username: 'RiskTaker',
      challenge: '$5K',
      profit: '+8.7%',
      winRate: '65%',
      status: 'Passed',
      trades: 76
    },
    {
      rank: 4,
      username: 'CryptoQueen',
      challenge: '$10K',
      profit: '+7.2%',
      winRate: '69%',
      status: 'Active',
      trades: 124
    },
    {
      rank: 5,
      username: 'ScalperPro',
      challenge: '$5K',
      profit: '+6.9%',
      winRate: '75%',
      status: 'Active',
      trades: 201
    },
    {
      rank: 6,
      username: 'SwingTradr',
      challenge: '$25K',
      profit: '-3.2%',
      winRate: '58%',
      status: 'Active',
      trades: 87
    },
    {
      rank: 7,
      username: 'DayTraderX',
      challenge: '$5K',
      profit: '+4.5%',
      winRate: '62%',
      status: 'Active',
      trades: 65
    },
    {
      rank: 8,
      username: 'OptionsGuru',
      challenge: '$10K',
      profit: '+2.1%',
      winRate: '55%',
      status: 'Active',
      trades: 54
    },
    {
      rank: 9,
      username: 'MarketWizard',
      challenge: '$25K',
      profit: '+1.8%',
      winRate: '71%',
      status: 'Active',
      trades: 112
    },
    {
      rank: 10,
      username: 'PipHunter',
      challenge: '$5K',
      profit: '+0.9%',
      winRate: '68%',
      status: 'Active',
      trades: 89
    }
  ]

  const getRankBadge = (rank) => {
    if (rank === 1) return <span className="rank-badge gold">{rank}</span>
    if (rank === 2) return <span className="rank-badge silver">{rank}</span>
    if (rank === 3) return <span className="rank-badge bronze">{rank}</span>
    return rank
  }

  const getStatusBadge = (status) => {
    const className = status === 'Passed' ? 'status-badge passed' : 'status-badge active'
    return <span className={className}>{status}</span>
  }

  const getProfitClass = (profit) => {
    return profit.startsWith('+') ? 'positive' : 'negative'
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

      {/* Leaderboard Banner */}
      <section className="leaderboard-banner">
        <div className="container">
          <h1>Top Traders</h1>
          <p>See how you rank against other challenge participants</p>
        </div>
      </section>

      {/* Leaderboard Filters */}
      <section className="leaderboard-filters">
        <div className="container">
          <div className="filter-options">
            <select id="challengeFilter" value={filter} onChange={handleFilterChange}>
              <option value="all">All Challenges</option>
              <option value="5k">$5K Challenge</option>
              <option value="10k">$10K Challenge</option>
              <option value="25k">$25K Challenge</option>
            </select>
            <select id="sortBy" value={sortBy} onChange={handleSortChange}>
              <option value="profit">Sort by Profit %</option>
              <option value="winrate">Sort by Win Rate</option>
              <option value="rank">Sort by Rank</option>
            </select>
          </div>
        </div>
      </section>

      {/* Leaderboard Table */}
      <section className="leaderboard-section">
        <div className="container">
          <div className="leaderboard-table-container">
            <table className="leaderboard-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Username</th>
                  <th>Challenge</th>
                  <th>Profit %</th>
                  <th>Win Rate</th>
                  <th>Status</th>
                  <th>Trades</th>
                </tr>
              </thead>
              <tbody>
                {leaderboardData.map((trader, index) => (
                  <tr key={index}>
                    <td>{getRankBadge(trader.rank)}</td>
                    <td>{trader.username}</td>
                    <td>{trader.challenge}</td>
                    <td className={getProfitClass(trader.profit)}>{trader.profit}</td>
                    <td>{trader.winRate}</td>
                    <td>{getStatusBadge(trader.status)}</td>
                    <td>{trader.trades}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="leaderboard-stats">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-trophy"></i>
              </div>
              <div className="stat-info">
                <h3>Total Challenges</h3>
                <span className="stat-number">1,247</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-chart-line"></i>
              </div>
              <div className="stat-info">
                <h3>Success Rate</h3>
                <span className="stat-number">68%</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-users"></i>
              </div>
              <div className="stat-info">
                <h3>Active Traders</h3>
                <span className="stat-number">892</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">
                <i className="fas fa-dollar-sign"></i>
              </div>
              <div className="stat-info">
                <h3>Total Profits</h3>
                <span className="stat-number">$45.2K</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tips Section */}
      <section className="tips-section">
        <div className="container">
          <h2>Challenge Success Tips</h2>
          <div className="tips-grid">
            <div className="tip-card">
              <div className="tip-icon">
                <i className="fas fa-shield-alt"></i>
              </div>
              <h3>Manage Risk</h3>
              <p>Always stay within the 5% daily loss limit and 10% maximum drawdown</p>
            </div>
            <div className="tip-card">
              <div className="tip-icon">
                <i className="fas fa-calendar-check"></i>
              </div>
              <h3>Meet Trading Days</h3>
              <p>Ensure you meet the minimum trading days requirement before hitting profit target</p>
            </div>
            <div className="tip-card">
              <div className="tip-icon">
                <i className="fas fa-newspaper"></i>
              </div>
              <h3>Avoid News Trading</h3>
              <p>Stay away from high-impact news events to avoid rule violations</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2>Ready to Join the Leaderboard?</h2>
          <p>Start your challenge today and compete with traders worldwide</p>
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

export default Leaderboard
