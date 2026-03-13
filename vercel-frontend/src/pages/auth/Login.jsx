import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const Login = () => {
  const [email, setEmail] = useState('demo@propfirm.com')
  const [password, setPassword] = useState('demopass123')
  const [remember, setRemember] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    // Check auth state and update UI
    const isLoggedIn = localStorage.getItem('isLoggedIn')
    
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
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Demo credentials check
    if (email === 'demo@propfirm.com' && password === 'demopass123') {
      // Set login status in localStorage
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('userEmail', email)
      
      // Redirect to dashboard
      navigate('/dashboard')
    } else {
      // Simulate login process for any other credentials
      setTimeout(() => {
        // Set login status in localStorage
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('userEmail', email)
        
        // Redirect to dashboard
        navigate('/dashboard')
      }, 1000)
    }
  }

  const handleGoogleLogin = () => {
    // Simulate Google login
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userEmail', 'google-user@example.com')
    navigate('/dashboard')
  }

  return (
    <div>
      {/* Simple Navigation for Auth Pages */}
      <nav className="auth-navbar">
        <div className="nav-container">
          <div className="logo">
            <h2>PropFirm<span className="highlight">Challenge</span></h2>
          </div>
        </div>
      </nav>

      {/* Login Section */}
      <section className="auth-section">
        <div className="container">
          <div className="auth-card">
            <div className="auth-header">
              <h2>Welcome Back</h2>
              <p>Sign in to your account to continue</p>
            </div>
            
            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email" 
                  placeholder="Enter your email" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  name="password" 
                  placeholder="Enter your password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required 
                />
              </div>
              
              <div className="form-options">
                <div className="remember-me">
                  <input 
                    type="checkbox" 
                    id="remember" 
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                  />
                  <label htmlFor="remember">Remember me</label>
                </div>
                <a href="#" className="forgot-password">Forgot Password?</a>
              </div>
              
              <button type="submit" className="btn btn-primary btn-full">Login</button>
              
              <div className="divider">or continue with</div>
              
              <button type="button" className="btn btn-google" onClick={handleGoogleLogin}>
                <i className="fab fa-google"></i>
                {' Continue with Google'}
              </button>
            </form>
            
            <div className="auth-footer">
              <p>Don't have an account? <a href="/register">Register now</a></p>
              <p><i className="fas fa-info-circle"></i> Demo credentials: demo@propfirm.com / demopass123</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer auth-footer">
        <div className="container">
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

export default Login
