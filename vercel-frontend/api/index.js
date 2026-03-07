import app from '../app.js';

export default function handler(req, res) {
  // Let the Express app handle the request
  app(req, res);
}
