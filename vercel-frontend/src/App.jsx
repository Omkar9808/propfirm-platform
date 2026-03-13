import React from 'react'
import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import DashboardLayout from './layouts/DashboardLayout'
import AdminLayout from './layouts/AdminLayout'
import ProtectedRoute from './components/ProtectedRoute'

// Public Pages
import Home from './pages/Home'
import Pricing from './pages/Pricing'
import Rules from './pages/Rules'
import Leaderboard from './pages/Leaderboard'
import Checkout from './pages/Checkout'

// Auth Pages
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'

// Dashboard Pages
import Dashboard from './pages/dashboard/Dashboard'
import Accounts from './pages/dashboard/Accounts'
import AccountDetail from './pages/dashboard/AccountDetail'
import Settings from './pages/dashboard/Settings'
import Affiliate from './pages/dashboard/Affiliate'
import Certificates from './pages/dashboard/Certificates'
import Buy from './pages/dashboard/Buy'

// Admin Pages
import AdminDashboard from './pages/admin/AdminDashboard'
import AdminUsers from './pages/admin/Users'
import AdminAccounts from './pages/admin/Accounts'
import AdminPayments from './pages/admin/Payments'
import AdminChallenges from './pages/admin/Challenges'
import AdminRiskMonitor from './pages/admin/RiskMonitor'
import AdminAnalytics from './pages/admin/Analytics'
import AdminSettings from './pages/admin/Settings'
import AdminViolations from './pages/admin/Violations'

function App() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Home />} />
        <Route path="pricing" element={<Pricing />} />
        <Route path="rules" element={<Rules />} />
        <Route path="leaderboard" element={<Leaderboard />} />
        <Route path="checkout" element={<Checkout />} />
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Route>

      {/* Dashboard Routes */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <DashboardLayout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="accounts" element={<Accounts />} />
        <Route path="account-detail" element={<AccountDetail />} />
        <Route path="settings" element={<Settings />} />
        <Route path="affiliate" element={<Affiliate />} />
        <Route path="certificates" element={<Certificates />} />
        <Route path="buy" element={<Buy />} />
      </Route>

      {/* Admin Routes */}
      <Route path="/admin" element={
        <ProtectedRoute>
          <AdminLayout />
        </ProtectedRoute>
      }>
        <Route index element={<AdminDashboard />} />
        <Route path="users" element={<AdminUsers />} />
        <Route path="accounts" element={<AdminAccounts />} />
        <Route path="payments" element={<AdminPayments />} />
        <Route path="challenges" element={<AdminChallenges />} />
        <Route path="risk-monitor" element={<AdminRiskMonitor />} />
        <Route path="analytics" element={<AdminAnalytics />} />
        <Route path="settings" element={<AdminSettings />} />
        <Route path="violations" element={<AdminViolations />} />
      </Route>
    </Routes>
  )
}

export default App
