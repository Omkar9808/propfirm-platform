import { useEffect, useRef } from 'react'

// Animation hooks converted from main.js

export const useScrollReveal = () => {
  const observerRef = useRef(null)

  useEffect(() => {
    // Wait for DOM to be ready
    const timer = setTimeout(() => {
      const revealElements = document.querySelectorAll('.scroll-reveal')
      
      if (revealElements.length === 0) return
      
      const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animated')
            revealObserver.unobserve(entry.target)
          }
        })
      }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      })
      
      revealElements.forEach(el => {
        revealObserver.observe(el)
      })

      observerRef.current = revealObserver
    }, 100)

    return () => {
      clearTimeout(timer)
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [])
}

export const useProgressBars = () => {
  const observerRef = useRef(null)

  useEffect(() => {
    const timer = setTimeout(() => {
      const progressBars = document.querySelectorAll('.progress-fill')
      
      if (progressBars.length === 0) return
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const width = entry.target.style.width || entry.target.getAttribute('data-width') || '0%'
            entry.target.style.width = '0'
            
            setTimeout(() => {
              entry.target.style.transition = 'width 1.5s ease-in-out'
              entry.target.style.width = width
            }, 100)
            
            observer.unobserve(entry.target)
          }
        })
      }, {
        threshold: 0.5
      })
      
      progressBars.forEach(bar => {
        // Store original width
        if (bar.style.width && !bar.getAttribute('data-width')) {
          bar.setAttribute('data-width', bar.style.width)
        }
        observer.observe(bar)
      })

      observerRef.current = observer
    }, 100)

    return () => {
      clearTimeout(timer)
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [])
}

export const useCounters = () => {
  const observerRef = useRef(null)

  useEffect(() => {
    const timer = setTimeout(() => {
      const counters = document.querySelectorAll('[data-target]')
      
      if (counters.length === 0) return
      
      const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !entry.target.dataset.animated) {
            const target = parseInt(entry.target.getAttribute('data-target'))
            const duration = parseInt(entry.target.getAttribute('data-duration')) || 2000
            const increment = target / (duration / 16) // 60fps approximation
            let current = 0
            
            entry.target.dataset.animated = true
            
            const updateCounter = () => {
              current += increment
              if (current < target) {
                entry.target.textContent = Math.ceil(current)
                requestAnimationFrame(updateCounter)
              } else {
                entry.target.textContent = target
              }
            }
            
            updateCounter()
            counterObserver.unobserve(entry.target)
          }
        })
      }, {
        threshold: 0.5
      })
      
      counters.forEach(counter => {
        counterObserver.observe(counter)
      })

      observerRef.current = counterObserver
    }, 100)

    return () => {
      clearTimeout(timer)
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [])
}

export const useHoverEffects = () => {
  useEffect(() => {
    const timer = setTimeout(() => {
      // Add enhanced hover effects to cards
      const hoverableElements = document.querySelectorAll('.card, .step-card, .model-card, .pricing-card, .account-card')
      
      hoverableElements.forEach(element => {
        const handleMouseEnter = function() {
          // Add subtle scale effect
          this.style.transform = 'translateY(-8px) scale(1.02)'
          this.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s ease'
          
          // Enhance shadow
          this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.3)'
        }
        
        const handleMouseLeave = function() {
          this.style.transform = 'translateY(0) scale(1)'
          this.style.boxShadow = ''
        }
        
        element.addEventListener('mouseenter', handleMouseEnter)
        element.addEventListener('mouseleave', handleMouseLeave)
      })
      
      // Enhanced button effects
      const buttons = document.querySelectorAll('.btn')
      buttons.forEach(button => {
        const handleMouseEnter = function() {
          this.style.transform = 'translateY(-2px)'
          this.style.boxShadow = '0 10px 20px rgba(0, 255, 157, 0.2)'
        }
        
        const handleMouseLeave = function() {
          this.style.transform = 'translateY(0)'
          this.style.boxShadow = ''
        }
        
        const handleMouseDown = function() {
          this.style.transform = 'translateY(1px)'
        }
        
        button.addEventListener('mouseenter', handleMouseEnter)
        button.addEventListener('mouseleave', handleMouseLeave)
        button.addEventListener('mousedown', handleMouseDown)
      })

      return () => {
        // Cleanup event listeners
        hoverableElements.forEach(element => {
          element.removeEventListener('mouseenter', () => {})
          element.removeEventListener('mouseleave', () => {})
        })
        buttons.forEach(button => {
          button.removeEventListener('mouseenter', () => {})
          button.removeEventListener('mouseleave', () => {})
          button.removeEventListener('mousedown', () => {})
        })
      }
    }, 100)
  }, [])
}

export const useNavigation = () => {
  useEffect(() => {
    const timer = setTimeout(() => {
      // Mobile menu toggle
      const hamburger = document.querySelector('.hamburger')
      const navMenu = document.querySelector('.nav-menu')
      
      if (hamburger && navMenu) {
        const handleClick = function() {
          hamburger.classList.toggle('active')
          navMenu.classList.toggle('active')
        }
        
        hamburger.addEventListener('click', handleClick)
      }
      
      // Close mobile menu when clicking outside
      const handleOutsideClick = function(event) {
        const isClickInsideNav = hamburger && (hamburger.contains(event.target) || navMenu.contains(event.target))
        
        if (!isClickInsideNav && navMenu && navMenu.classList.contains('active')) {
          hamburger.classList.remove('active')
          navMenu.classList.remove('active')
        }
      }
      
      document.addEventListener('click', handleOutsideClick)
      
      // Sidebar toggle for desktop
      const menuToggle = document.querySelector('.menu-toggle')
      if (menuToggle) {
        const handleToggleClick = function() {
          const sidebar = document.querySelector('.sidebar')
          const mainContent = document.querySelector('.main-content')
          if (sidebar && mainContent) {
            sidebar.classList.toggle('collapsed')
            mainContent.classList.toggle('expanded')
          }
        }
        
        menuToggle.addEventListener('click', handleToggleClick)
      }

      return () => {
        clearTimeout(timer)
        if (hamburger) {
          hamburger.removeEventListener('click', () => {})
        }
        document.removeEventListener('click', handleOutsideClick)
        if (menuToggle) {
          menuToggle.removeEventListener('click', () => {})
        }
      }
    }, 100)
  }, [])
}
