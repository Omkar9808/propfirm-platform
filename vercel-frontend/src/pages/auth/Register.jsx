import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const Register = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    terms: false,
    newsletter: false
  })

  const navigate = useNavigate()

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Basic validation
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!')
      return
    }
    
    if (!formData.terms) {
      alert('You must agree to Terms of Service and Privacy Policy!')
      return
    }
    
    // Simulate registration process
    setTimeout(() => {
      // Set login status in localStorage
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('userEmail', formData.email)
      localStorage.setItem('userName', `${formData.firstName} ${formData.lastName}`)
      
      // Redirect to dashboard
      navigate('/dashboard')
    }, 1000)
  }

  const handleGoogleRegister = () => {
    // Simulate Google registration
    localStorage.setItem('isLoggedIn', 'true')
    localStorage.setItem('userEmail', 'google-user@example.com')
    localStorage.setItem('userName', 'Google User')
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

      {/* Registration Section */}
      <section className="auth-section">
        <div className="container">
          <div className="auth-card">
            <div className="auth-header">
              <h2>Create Account</h2>
              <p>Join thousands of traders practicing prop firm challenges</p>
            </div>
            
            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-row">
                <div className="form-group half">
                  <label htmlFor="firstName">First Name</label>
                  <input 
                    type="text" 
                    id="firstName" 
                    name="firstName" 
                    placeholder="Enter your first name" 
                    value={formData.firstName}
                    onChange={handleChange}
                    required 
                  />
                </div>
                <div className="form-group half">
                  <label htmlFor="lastName">Last Name</label>
                  <input 
                    type="text" 
                    id="lastName" 
                    name="lastName" 
                    placeholder="Enter your last name" 
                    value={formData.lastName}
                    onChange={handleChange}
                    required 
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email" 
                  placeholder="Enter your email" 
                  value={formData.email}
                  onChange={handleChange}
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  name="password" 
                  placeholder="Create a password" 
                  value={formData.password}
                  onChange={handleChange}
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  name="confirmPassword" 
                  placeholder="Confirm your password" 
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required 
                />
              </div>
              
              <div className="form-group checkbox-group">
                <input 
                  type="checkbox" 
                  id="terms" 
                  name="terms" 
                  checked={formData.terms}
                  onChange={handleChange}
                  required 
                />
                <label htmlFor="terms">
                  I agree to <a href="/terms">Terms of Service</a> and <a href="/privacy">Privacy Policy</a>
                </label>
              </div>
              
              <div className="form-group checkbox-group">
                <input 
                  type="checkbox" 
                  id="newsletter" 
                  name="newsletter"
                  checked={formData.newsletter}
                  onChange={handleChange}
                />
                <label htmlFor="newsletter">Subscribe to our newsletter for trading tips and updates</label>
              </div>
              
              <button type="submit" className="btn btn-primary btn-full">Create Account</button>
              
              <div className="divider">or continue with</div>
              
              <button type="button" className="btn btn-google" onClick={handleGoogleRegister}>
                <i className="fab fa-google"></i>
                {' Continue with Google'}
              </button>
            </form>
            
            <div className="auth-footer">
              <p>Already have an account? <a href="/login">Login now</a></p>
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

export default Register
