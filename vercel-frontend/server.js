import app from './app.js';

// For local development
if (process.env.NODE_ENV !== 'production') {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`🚀 Server is running on http://localhost:${PORT}`);
    console.log(`📡 API available at http://localhost:${PORT}/api`);
    console.log('Press Ctrl+C to stop the server');
  });
}

// For Vercel deployment
export default function handler(req, res) {
  return app(req, res);
}