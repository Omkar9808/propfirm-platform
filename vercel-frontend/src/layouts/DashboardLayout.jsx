import React from 'react'
import { Outlet } from 'react-router-dom'
import DashboardNavbar from '../components/DashboardNavbar'
import DashboardSidebar from '../components/DashboardSidebar'

const DashboardLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <DashboardNavbar />
      <div className="flex">
        <DashboardSidebar />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout
