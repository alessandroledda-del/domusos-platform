'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useToast } from '@/hooks/useToast'
import { apiClient } from '@/lib/api-client'
import { useAuthStore, type AuthUser } from '@/store/authStore'

export default function DashboardPage() {
  const router = useRouter()
  const toast = useToast()
  const [isLoading, setIsLoading] = useState(true)
  const user = useAuthStore((state) => state.user)
  const setUser = useAuthStore((state) => state.setUser)
  const clearAuth = useAuthStore((state) => state.clearAuth)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser: AuthUser = await apiClient.getCurrentUser()
        setUser(currentUser)
      } catch {
        clearAuth()
        router.push('/login')
      } finally {
        setIsLoading(false)
      }
    }

    fetchUser()
  }, [clearAuth, router, setUser])

  const handleLogout = () => {
    clearAuth()
    toast.success('Signed out.')
    router.push('/login')
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <LoadingSpinner label="Loading dashboard..." />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <header className="bg-white shadow dark:bg-slate-900 dark:shadow-slate-900/50">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">DOMUSOS</h1>
          <div className="flex items-center gap-4">
            <span className="text-slate-600 dark:text-slate-300">
              {user?.nome} {user?.cognome}
            </span>
            <button
              onClick={handleLogout}
              className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          <Link href="/users">
            <div className="cursor-pointer rounded-lg bg-white p-6 shadow transition hover:shadow-lg dark:bg-slate-900">
              <div className="mb-2 text-sm font-medium text-slate-500 dark:text-slate-400">USERS</div>
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white">Manage Users</h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Create, edit, and manage user accounts.</p>
            </div>
          </Link>

          <Link href="/companies">
            <div className="cursor-pointer rounded-lg bg-white p-6 shadow transition hover:shadow-lg dark:bg-slate-900">
              <div className="mb-2 text-sm font-medium text-slate-500 dark:text-slate-400">COMPANIES</div>
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white">Manage Companies</h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Create, edit, and manage company information.</p>
            </div>
          </Link>

          <Link href="/properties">
            <div className="cursor-pointer rounded-lg bg-white p-6 shadow transition hover:shadow-lg dark:bg-slate-900">
              <div className="mb-2 text-sm font-medium text-slate-500 dark:text-slate-400">PROPERTIES</div>
              <h3 className="text-2xl font-bold text-slate-900 dark:text-white">Manage Properties</h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Create, edit, and verify property listings.</p>
            </div>
          </Link>
        </div>
      </main>
    </div>
  )
}
