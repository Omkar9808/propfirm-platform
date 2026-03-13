import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

const Dashboard = () => {
  const [selectedAccount, setSelectedAccount] = useState('account1')
  const equityChartRef = useRef(null)
  const balanceChartRef = useRef(null)
  const navigate = useNavigate()

  const accounts = [
    { id: 'account1', name: 'Account #12345 - $5K Challenge', status: 'Active' },
    { id: 'account2', name: 'Account #67890 - $10K Challenge', status: 'Active' },
    { id: 'account3', name: 'Account #11111 - $25K Challenge', status: 'Active' }
  ]

  const metrics = {
    balance: 5000.00,
    equity: 5123.45,
    floatingPL: 123.45,
    dailyLoss: 2.3,
    maxDD: 1.8,
    profitTarget: 2.5
  }

  const recentTrades = [
    { ticket: '#1234567', symbol: 'EURUSD', lot: '0.1', profit: '+$23.45', time: '10:23:45' },
    { ticket: '#1234566', symbol: 'GBPUSD', lot: '0.1', profit: '-$12.34', time: '09:45:12' },
    { ticket: '#1234565', symbol: 'USDJPY', lot: '0.2', profit: '+$34.56', time: '08:32:10' },
    { ticket: '#1234564', symbol: 'USDCAD', lot: '0.1', profit: '+$8.90', time: '07:15:22' },
    { ticket: '#1234563', symbol: 'AUDUSD', lot: '0.1', profit: '-$5.67', time: '06:45:33' }
  ]

  useEffect(() => {
    // Initialize charts when Chart.js is available
    if (typeof Chart !== 'undefined') {
      const equityCtx = equityChartRef.current?.getContext('2d')
      const balanceCtx = balanceChartRef.current?.getContext('2d')

      if (equityCtx) {
        new Chart(equityCtx, {
          type: 'line',
          data: {
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Today'],
            datasets: [{
              label: 'Equity',
              data: [5000, 5050, 5020, 5100, 5080, 5120, 5123],
              borderColor: '#00ff9d',
              backgroundColor: 'rgba(0, 255, 157, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: false,
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                  color: '#fff'
                }
              },
              x: {
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                  color: '#fff'
                }
              }
            }
          }
        })
      }

      if (balanceCtx) {
        new Chart(balanceCtx, {
          type: 'line',
          data: {
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Today'],
            datasets: [{
              label: 'Balance',
              data: [5000, 5000, 5000, 5000, 5000, 5000, 5000],
              borderColor: '#0ea5e9',
              backgroundColor: 'rgba(14, 165, 233, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: false,
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                  color: '#fff'
                }
              },
              x: {
                grid: {
                  color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                  color: '#fff'
                }
              }
            }
          }
        })
      }
    }

    // Simulate real-time updates
    const interval = setInterval(() => {
      console.log('Updating dashboard data...')
    }, 30000)

    return () => clearInterval(interval)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('userEmail')
    localStorage.removeItem('userName')
    navigate('/login')
  }

  return (
    <div>
      {/* Sidebar Navigation */}
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>PropFirm<span className="highlight">Challenge</span></h2>
        </div>
        <ul className="sidebar-menu">
          <li className="active"><a href="/dashboard"><i className="fas fa-home"></i> Dashboard</a></li>
          <li><a href="/accounts"><i className="fas fa-wallet"></i> My Accounts</a></li>
          <li><a href="/buy"><i className="fas fa-shopping-cart"></i> Buy Challenge</a></li>
          <li><a href="/leaderboard"><i className="fas fa-trophy"></i> Leaderboard</a></li>
          <li><a href="/affiliate"><i className="fas fa-users"></i> Affiliate</a></li>
          <li><a href="/certificates"><i className="fas fa-certificate"></i> Certificates</a></li>
          <li><a href="/settings"><i className="fas fa-cog"></i> Settings</a></li>
          <li><a href="#" onClick={handleLogout}><i className="fas fa-sign-out-alt"></i> Logout</a></li>
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
            <select 
              id="accountSelect" 
              value={selectedAccount}
              onChange={(e) => setSelectedAccount(e.target.value)}
            >
              <option value="account1">Account #12345 - $5K Challenge</option>
              <option value="account2">Account #67890 - $10K Challenge</option>
              <option value="account3">Account #11111 - $25K Challenge</option>
            </select>
          </div>
          <div className="user-info">
            <i className="fas fa-user-circle"></i>
            <span>John Doe</span>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="dashboard-container">
          <h1>Dashboard Overview</h1>
          
          {/* Account Summary Cards */}
          <div className="summary-grid">
            <div className="summary-card">
              <div className="card-header">
                <h3>Account ID</h3>
                <i className="fas fa-hashtag"></i>
              </div>
              <div className="card-value">#12345</div>
              <div className="card-status active">Active</div>
            </div>
            
            <div className="summary-card">
              <div className="card-header">
                <h3>Status</h3>
                <i className="fas fa-circle"></i>
              </div>
              <div className="card-value">Active</div>
              <div className="card-status active">Active</div>
            </div>
            
            <div className="summary-card">
              <div className="card-header">
                <h3>Days Traded</h3>
                <i className="fas fa-calendar"></i>
              </div>
              <div className="card-value">7</div>
              <div className="card-status">of 3 min</div>
            </div>
            
            <div className="summary-card">
              <div className="card-header">
                <h3>Start Date</h3>
                <i className="fas fa-clock"></i>
              </div>
              <div className="card-value">Mar 1, 2026</div>
              <div className="card-status">Started</div>
            </div>
          </div>

          {/* Metrics Section */}
          <div className="metrics-section">
            <div className="metric-cards">
              <div className="metric-card">
                <div className="metric-header">
                  <h3>Balance</h3>
                  <i className="fas fa-dollar-sign"></i>
                </div>
                <div className="metric-value">${metrics.balance.toLocaleString()}</div>
                <div className="progress-container">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{width: '100%'}}></div>
                  </div>
                </div>
              </div>
              
              <div className="metric-card">
                <div className="metric-header">
                  <h3>Equity</h3>
                  <i className="fas fa-chart-line"></i>
                </div>
                <div className="metric-value positive">${metrics.equity.toLocaleString()}</div>
                <div className="progress-container">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{width: '102.5%'}}></div>
                  </div>
                </div>
              </div>
              
              <div className="metric-card">
                <div className="metric-header">
                  <h3>Floating P&L</h3>
                  <i className="fas fa-coins"></i>
                </div>
                <div className="metric-value positive">+${metrics.floatingPL.toLocaleString()}</div>
                <div className="progress-container">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{width: '2.5%'}}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Progress Bars */}
            <div className="progress-section">
              <div className="progress-item">
                <div className="progress-header">
                  <h3>Daily Loss %</h3>
                  <span className="progress-percent">{metrics.dailyLoss}%</span>
                </div>
                <div className="progress-bar-large">
                  <div className="progress-fill daily-loss" style={{width: '46%'}}></div>
                </div>
                <div className="progress-limit">Limit: 5%</div>
              </div>
            
              <div className="progress-item">
                <div className="progress-header">
                  <h3>Max DD %</h3>
                  <span className="progress-percent">{metrics.maxDD}%</span>
                </div>
                <div className="progress-bar-large">
                  <div className="progress-fill max-dd" style={{width: '18%'}}></div>
                </div>
                <div className="progress-limit">Limit: 10%</div>
              </div>
            
              <div className="progress-item">
                <div className="progress-header">
                  <h3>Profit Target %</h3>
                  <span className="progress-percent">{metrics.profitTarget}%</span>
                </div>
                <div className="progress-bar-large">
                  <div className="progress-fill profit-target" style={{width: '31.25%'}}></div>
                </div>
                <div className="progress-limit">Target: 8%</div>
              </div>
            </div>

            {/* Chart Section */}
            <div className="chart-section">
              <div className="chart-container">
                <h3>Equity Curve</h3>
                <div className="chart-placeholder">
                  <canvas ref={equityChartRef} width="800" height="300"></canvas>
                </div>
              </div>
              
              <div className="chart-container">
                <h3>Balance History</h3>
                <div className="chart-placeholder">
                  <canvas ref={balanceChartRef} width="800" height="300"></canvas>
                </div>
              </div>
            </div>

            {/* Recent Trades */}
            <div className="trades-section">
              <h3>Recent Trades</h3>
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
                    {recentTrades.map((trade, index) => (
                      <tr key={index}>
                        <td>{trade.ticket}</td>
                        <td>{trade.symbol}</td>
                        <td>{trade.lot}</td>
                        <td className={trade.profit.startsWith('+') ? 'positive' : 'negative'}>{trade.profit}</td>
                        <td>{trade.time}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Rule Violations */}
            <div className="violations-section">
              <h3>Rule Violations</h3>
              <div className="violations-box clean">
                <i className="fas fa-check-circle"></i>
                <p>No violations detected. Keep up the good work!</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Chart.js Script */}
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </div>
  )
}

export default Dashboard
