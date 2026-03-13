import React, { useState, useEffect } from 'react'
import { useNavigation, useScrollReveal } from '../hooks/useAnimations'

const Checkout = () => {
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState('card')
  const [cardNumber, setCardNumber] = useState('')
  const [expiryDate, setExpiryDate] = useState('')
  const [cvv, setCvv] = useState('')
  const [cardName, setCardName] = useState('')
  const [saveCard, setSaveCard] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      useNavigation()
      useScrollReveal()
    }, 100)
    
    return () => clearTimeout(timer)
  }, [])

  // Get challenge type from URL if present
  const urlParams = new URLSearchParams(window.location.search)
  const challengeType = urlParams.get('challenge') || '5k'
  
  const challengeDetails = {
    '5k': {
      name: '$5K Practice Challenge',
      balance: '$5,000',
      profitTarget: '8%',
      dailyLoss: '5%',
      maxDrawdown: '10%',
      minDays: '3',
      price: '$1.00'
    },
    '10k': {
      name: '$10K Practice Challenge',
      balance: '$10,000',
      profitTarget: '8%',
      dailyLoss: '5%',
      maxDrawdown: '10%',
      minDays: '5',
      price: '$2.00'
    },
    '25k': {
      name: '$25K Practice Challenge',
      balance: '$25,000',
      profitTarget: '8%',
      dailyLoss: '5%',
      maxDrawdown: '10%',
      minDays: '10',
      price: '$5.00'
    }
  }

  const currentChallenge = challengeDetails[challengeType] || challengeDetails['5k']

  const handlePaymentMethodChange = (method) => {
    setSelectedPaymentMethod(method)
  }

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '')
    const matches = v.match(/\d{4,16}/g)
    const match = matches && matches[0] || ''
    const parts = []
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4))
    }
    if (parts.length) {
      return parts.join(' ')
    } else {
      return v
    }
  }

  const formatExpiryDate = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '')
    if (v.length >= 2) {
      return v.slice(0, 2) + '/' + v.slice(2, 4)
    }
    return v
  }

  const handleCardNumberChange = (e) => {
    const formatted = formatCardNumber(e.target.value)
    setCardNumber(formatted)
  }

  const handleExpiryDateChange = (e) => {
    const formatted = formatExpiryDate(e.target.value)
    setExpiryDate(formatted)
  }

  const handlePurchase = async () => {
    if (isProcessing) return
    
    setIsProcessing(true)
    
    // Simulate payment processing
    setTimeout(() => {
      setIsProcessing(false)
      setShowSuccess(true)
      
      // Redirect to dashboard after success
      setTimeout(() => {
        window.location.href = '/dashboard'
      }, 3000)
    }, 2000)
  }

  return (
    <div>
      {/* Simple Navigation for Checkout */}
      <nav className="checkout-navbar">
        <div className="nav-container">
          <div className="logo">
            <h2>PropFirm<span className="highlight">Challenge</span></h2>
          </div>
        </div>
      </nav>

      {/* Checkout Section */}
      <section className="checkout-section">
        <div className="container">
          <div className="checkout-container">
            <div className="checkout-header">
              <h1>Complete Your Purchase</h1>
              <p>Securely complete your challenge purchase</p>
            </div>
            
            <div className="checkout-content">
              <div className="order-summary">
                <h2>Order Summary</h2>
                <div className="order-item">
                  <div className="item-info">
                    <h3>{currentChallenge.name}</h3>
                    <p className="item-desc">Account balance: {currentChallenge.balance}</p>
                    <p className="item-desc">Profit target: {currentChallenge.profitTarget}</p>
                    <p className="item-desc">Daily loss limit: {currentChallenge.dailyLoss}</p>
                    <p className="item-desc">Max drawdown: {currentChallenge.maxDrawdown}</p>
                    <p className="item-desc">Min trading days: {currentChallenge.minDays}</p>
                  </div>
                  <div className="item-price">{currentChallenge.price}</div>
                </div>
                
                <div className="order-details">
                  <div className="detail-row">
                    <span>Subtotal:</span>
                    <span>{currentChallenge.price}</span>
                  </div>
                  <div className="detail-row">
                    <span>Tax:</span>
                    <span>$0.00</span>
                  </div>
                  <div className="detail-row total">
                    <span>Total:</span>
                    <span className="total-price">{currentChallenge.price}</span>
                  </div>
                </div>
              </div>
              
              <div className="payment-form">
                <h2>Payment Information</h2>
                
                <div className="payment-methods">
                  <div 
                    className={`payment-method ${selectedPaymentMethod === 'card' ? 'active' : ''}`} 
                    onClick={() => handlePaymentMethodChange('card')}
                  >
                    <i className="fab fa-cc-visa"></i>
                    <span>Credit/Debit Card</span>
                  </div>
                  <div 
                    className={`payment-method ${selectedPaymentMethod === 'paypal' ? 'active' : ''}`} 
                    onClick={() => handlePaymentMethodChange('paypal')}
                  >
                    <i className="fab fa-paypal"></i>
                    <span>PayPal</span>
                  </div>
                  <div 
                    className={`payment-method ${selectedPaymentMethod === 'stripe' ? 'active' : ''}`} 
                    onClick={() => handlePaymentMethodChange('stripe')}
                  >
                    <i className="fab fa-cc-stripe"></i>
                    <span>Stripe</span>
                  </div>
                </div>
                
                {selectedPaymentMethod === 'card' && (
                  <div className="payment-fields">
                    <div className="form-group">
                      <label htmlFor="cardNumber">Card Number</label>
                      <input 
                        type="text" 
                        id="cardNumber" 
                        placeholder="1234 5678 9012 3456" 
                        maxLength="19"
                        value={cardNumber}
                        onChange={handleCardNumberChange}
                      />
                    </div>
                    
                    <div className="form-row">
                      <div className="form-group half">
                        <label htmlFor="expiryDate">Expiry Date</label>
                        <input 
                          type="text" 
                          id="expiryDate" 
                          placeholder="MM/YY" 
                          maxLength="5"
                          value={expiryDate}
                          onChange={handleExpiryDateChange}
                        />
                      </div>
                      <div className="form-group half">
                        <label htmlFor="cvv">CVV</label>
                        <input 
                          type="text" 
                          id="cvv" 
                          placeholder="123" 
                          maxLength="3"
                          value={cvv}
                          onChange={(e) => setCvv(e.target.value.replace(/[^0-9]/g, ''))}
                        />
                      </div>
                    </div>
                    
                    <div className="form-group">
                      <label htmlFor="cardName">Name on Card</label>
                      <input 
                        type="text" 
                        id="cardName" 
                        placeholder="John Doe"
                        value={cardName}
                        onChange={(e) => setCardName(e.target.value)}
                      />
                    </div>
                    
                    <div className="form-group checkbox-group">
                      <input 
                        type="checkbox" 
                        id="saveCard"
                        checked={saveCard}
                        onChange={(e) => setSaveCard(e.target.checked)}
                      />
                      <label htmlFor="saveCard">Save card details for future purchases</label>
                    </div>
                  </div>
                )}
                
                {selectedPaymentMethod === 'paypal' && (
                  <div className="payment-fields">
                    <div className="paypal-info">
                      <i className="fab fa-paypal"></i>
                      <p>You will be redirected to PayPal to complete your purchase</p>
                    </div>
                  </div>
                )}
                
                {selectedPaymentMethod === 'stripe' && (
                  <div className="payment-fields">
                    <div className="stripe-info">
                      <i className="fab fa-cc-stripe"></i>
                      <p>You will be redirected to Stripe to complete your purchase</p>
                    </div>
                  </div>
                )}
                
                <button 
                  className="btn btn-primary btn-full" 
                  onClick={handlePurchase}
                  disabled={isProcessing}
                >
                  {isProcessing ? 'Processing...' : `Complete Purchase - ${currentChallenge.price}`}
                </button>
                
                <div className="secure-payment">
                  <i className="fas fa-lock"></i>
                  <p>Your payment is secured with 256-bit SSL encryption</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Rules Summary */}
      <section className="rules-summary">
        <div className="container">
          <h2>Challenge Rules Summary</h2>
          <div className="summary-grid">
            <div className="summary-card">
              <i className="fas fa-percentage"></i>
              <h3>8% Profit Target</h3>
              <p>Required for challenge completion</p>
            </div>
            <div className="summary-card">
              <i className="fas fa-exclamation-triangle"></i>
              <h3>5% Daily Loss</h3>
              <p>Maximum daily drawdown limit</p>
            </div>
            <div className="summary-card">
              <i className="fas fa-times-circle"></i>
              <h3>10% Max DD</h3>
              <p>Overall maximum drawdown limit</p>
            </div>
            <div className="summary-card">
              <i className="fas fa-calendar-day"></i>
              <h3>Min {currentChallenge.minDays} Trading Days</h3>
              <p>Required before profit target</p>
            </div>
          </div>
        </div>
      </section>

      {/* Success Modal */}
      {showSuccess && (
        <div className="success-modal">
          <div className="modal-content">
            <div className="success-icon">
              <i className="fas fa-check-circle"></i>
            </div>
            <h2>Payment Successful!</h2>
            <p>Your challenge has been activated. Redirecting to dashboard...</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
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

export default Checkout
