'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { apiClient, User } from '@/lib/api-client'

export default function UsersPage() {
  const router = useRouter()
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await apiClient.getUsers()
        setUsers(data.results ?? data)
      } catch (err: any) {
        if (err.response?.status === 401) {
          router.push('/login')
        } else {
          setError('Failed to load users.')
        }
      } finally {
        setIsLoading(false)
      }
    }
    fetchUsers()
  }, [router])

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this user?')) return
    try {
      await apiClient.deleteUser(id)
      setUsers((prev) => prev.filter((u) => u.id !== id))
    } catch {
      alert('Failed to delete user.')
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="text-gray-500 hover:text-gray-900 text-sm">
              ← Dashboard
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Users</h1>
          </div>
          <Link
            href="/users/new"
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
          >
            + New User
          </Link>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {['Name', 'Email', 'Role', 'Status', 'Actions'].map((h) => (
                  <th
                    key={h}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-gray-500">
                    No users found.
                  </td>
                </tr>
              ) : (
                users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {user.nome} {user.cognome}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {user.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          user.ruolo === 'admin'
                            ? 'bg-purple-100 text-purple-800'
                            : user.ruolo === 'guest'
                            ? 'bg-gray-100 text-gray-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}
                      >
                        {user.ruolo}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          user.stato === 'active'
                            ? 'bg-green-100 text-green-800'
                            : user.stato === 'suspended'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {user.stato}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium flex gap-3">
                      <Link
                        href={`/users/${user.id}`}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        View
                      </Link>
                      <button
                        onClick={() => handleDelete(user.id)}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}
