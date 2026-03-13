export default function handler(req, res) {
  res.status(200).json({
    message: "Prop Firm API Running",
    version: "1.0.0",
    status: "healthy",
    timestamp: new Date().toISOString()
  });
}
