'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { apiClient, User } from '@/lib/api-client'
import Link from 'next/link'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await apiClient.getCurrentUser()
        setUser(currentUser)
      } catch (error) {
        router.push('/login')
      } finally {
        setIsLoading(false)
      }
    }

    fetchUser()
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">DOMUSOS</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">{user?.nome} {user?.cognome}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Users Card */}
          <Link href="/users">
            <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg cursor-pointer transition">
              <div className="text-gray-500 text-sm font-medium mb-2">USERS</div>
              <h3 className="text-2xl font-bold text-gray-900">Manage Users</h3>
              <p className="text-gray-600 text-sm mt-2">Create, edit, and manage user accounts</p>
            </div>
          </Link>

          {/* Companies Card */}
          <Link href="/companies">
            <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg cursor-pointer transition">
              <div className="text-gray-500 text-sm font-medium mb-2">COMPANIES</div>
              <h3 className="text-2xl font-bold text-gray-900">Manage Companies</h3>
              <p className="text-gray-600 text-sm mt-2">Create, edit, and manage company information</p>
            </div>
          </Link>

          {/* Properties Card */}
          <Link href="/properties">
            <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg cursor-pointer transition">
              <div className="text-gray-500 text-sm font-medium mb-2">PROPERTIES</div>
              <h3 className="text-2xl font-bold text-gray-900">Manage Properties</h3>
              <p className="text-gray-600 text-sm mt-2">Create, edit, and verify property listings</p>
            </div>
          </Link>
        </div>
      </main>
    </div>
  )
}
