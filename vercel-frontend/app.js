import express from 'express';

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// API Routes
app.get('/api', (req, res) => {
  res.json({ 
    message: "Prop Firm API Running", 
    version: "1.0.0",
    status: "healthy"
  });
});

// API health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

export default app;