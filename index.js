const fs = require('fs');
const path = require('path');

module.exports = function handler(req, res) {
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const url = req.url || '/';
    
    // API endpoint
    if (url === '/api' || url.startsWith('/api/')) {
      res.status(200).json({
        message: "Prop Firm API Running",
        version: "1.0.0",
        status: "healthy",
        timestamp: new Date().toISOString()
      });
      return;
    }
    
    // Serve HTML files
    let filePath;
    switch(url) {
      case '/':
        filePath = path.join(__dirname, 'vercel-frontend/views/index.html');
        break;
      case '/pricing':
        filePath = path.join(__dirname, 'vercel-frontend/views/pricing.html');
        break;
      case '/rules':
        filePath = path.join(__dirname, 'vercel-frontend/views/rules.html');
        break;
      case '/leaderboard':
        filePath = path.join(__dirname, 'vercel-frontend/views/leaderboard.html');
        break;
      case '/login':
        filePath = path.join(__dirname, 'vercel-frontend/views/auth/login.html');
        break;
      case '/register':
        filePath = path.join(__dirname, 'vercel-frontend/views/auth/register.html');
        break;
      case '/dashboard':
        filePath = path.join(__dirname, 'vercel-frontend/views/dashboard/index.html');
        break;
      case '/checkout':
        filePath = path.join(__dirname, 'vercel-frontend/views/checkout.html');
        break;
      case '/admin':
        filePath = path.join(__dirname, 'vercel-frontend/views/admin/overview.html');
        break;
      case '/admin/login':
        filePath = path.join(__dirname, 'vercel-frontend/views/admin/login.html');
        break;
      default:
        filePath = path.join(__dirname, 'vercel-frontend/views/index.html');
        break;
    }
    
    // Check if file exists
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8');
      res.setHeader('Content-Type', 'text/html');
      res.status(200).send(content);
    } else {
      res.status(404).json({ error: 'Page not found' });
    }
    
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
