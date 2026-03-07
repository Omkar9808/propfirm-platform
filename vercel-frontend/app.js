import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from public directory
app.use('/public', express.static(path.join(__dirname, 'public')));

// API Routes
app.get('/api', (req, res) => {
  res.json({ 
    message: "Prop Firm API Running", 
    version: "1.0.0",
    status: "healthy"
  });
});

// Route handler for all pages
app.get(/.*/, (req, res) => {
  // Redirect to admin login if trying to access admin pages without authentication
  if (req.path.startsWith('/admin') && req.path !== '/admin/login' && !req.path.startsWith('/public') && !req.path.startsWith('/api')) {
    // For demo purposes, we'll allow access but in production you'd check authentication
    // This is a simplified version for demonstration
  }
  
  let filePath;
  
  // Determine the file path based on the route
  switch(req.path) {
    case '/':
      filePath = path.join(__dirname, 'views', 'index.html');
      break;
    case '/pricing':
      filePath = path.join(__dirname, 'views', 'pricing.html');
      break;
    case '/rules':
      filePath = path.join(__dirname, 'views', 'rules.html');
      break;
    case '/leaderboard':
      filePath = path.join(__dirname, 'views', 'leaderboard.html');
      break;
    case '/login':
      filePath = path.join(__dirname, 'views', 'auth', 'login.html');
      break;
    case '/register':
      filePath = path.join(__dirname, 'views', 'auth', 'register.html');
      break;
    case '/dashboard':
      filePath = path.join(__dirname, 'dashboard', 'dashboard.html');
      break;
    case '/dashboard/journal':
      filePath = path.join(__dirname, 'dashboard', 'journal.html');
      break;
    case '/dashboard/simulator':
      filePath = path.join(__dirname, 'dashboard', 'simulator.html');
      break;
    case '/dashboard/risk':
      filePath = path.join(__dirname, 'dashboard', 'risk.html');
      break;
    case '/accounts':
      filePath = path.join(__dirname, 'views', 'dashboard', 'accounts.html');
      break;
    case '/buy':
      filePath = path.join(__dirname, 'views', 'dashboard', 'buy.html');
      break;
    case '/certificates':
      filePath = path.join(__dirname, 'views', 'dashboard', 'certificates.html');
      break;
    case '/settings':
      filePath = path.join(__dirname, 'views', 'dashboard', 'settings.html');
      break;
    case '/affiliate':
      filePath = path.join(__dirname, 'views', 'dashboard', 'affiliate.html');
      break;
    case '/checkout':
      filePath = path.join(__dirname, 'views', 'checkout.html');
      break;
    case '/account/12345':
    case '/account/67890':
    case '/account/11111':
      filePath = path.join(__dirname, 'views', 'dashboard', 'account-detail.html');
      break;
    case '/admin/users':
      filePath = path.join(__dirname, 'views', 'admin', 'users.html');
      break;
    case '/admin/accounts':
      filePath = path.join(__dirname, 'views', 'admin', 'accounts.html');
      break;
    case '/admin/challenges':
      filePath = path.join(__dirname, 'views', 'admin', 'challenges.html');
      break;
    case '/admin/payments':
      filePath = path.join(__dirname, 'views', 'admin', 'payments.html');
      break;
    case '/admin/violations':
      filePath = path.join(__dirname, 'views', 'admin', 'violations.html');
      break;
    case '/admin/risk-monitor':
      filePath = path.join(__dirname, 'views', 'admin', 'risk-monitor.html');
      break;
    case '/admin/analytics':
      filePath = path.join(__dirname, 'views', 'admin', 'analytics.html');
      break;
    case '/admin/settings':
      filePath = path.join(__dirname, 'views', 'admin', 'settings.html');
      break;
    case '/admin':
      filePath = path.join(__dirname, 'views', 'admin', 'overview.html');
      break;
    case '/admin/login':
      filePath = path.join(__dirname, 'views', 'admin', 'login.html');
      break;
    default:
      // For any other route, try to find a matching HTML file
      filePath = path.join(__dirname, 'views', req.path.slice(1) + '.html');
      break;
  }
  
  // Check if file exists, if not, serve index.html (for SPA routing)
  res.sendFile(filePath, (err) => {
    if (err) {
      // If file not found, serve the main index.html
      res.sendFile(path.join(__dirname, 'views', 'index.html'));
    }
  });
});

export default app;