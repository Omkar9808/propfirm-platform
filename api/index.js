import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(path.join(__dirname, '../vercel-frontend/public')));

// API Routes
app.get('/api', (req, res) => {
  res.json({ 
    message: "Prop Firm API Running", 
    version: "1.0.0",
    status: "healthy"
  });
});

// Serve HTML files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/index.html'));
});

app.get('/pricing', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/pricing.html'));
});

app.get('/rules', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/rules.html'));
});

app.get('/leaderboard', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/leaderboard.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/auth/login.html'));
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/auth/register.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/dashboard/index.html'));
});

app.get('/checkout', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/checkout.html'));
});

// Admin routes
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/admin/overview.html'));
});

app.get('/admin/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/admin/login.html'));
});

// Catch all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../vercel-frontend/views/index.html'));
});

export default function handler(req, res) {
  app(req, res);
}
