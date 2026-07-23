'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { apiClient, User } from '@/lib/api-client'

export default function UserDetailPage() {
  const router = useRouter()
  const params = useParams()
  const id = Number(params.id)

  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [form, setForm] = useState<Partial<User>>({})
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await apiClient.getUserById(id)
        setUser(data)
        setForm(data)
      } catch (err: any) {
        if (err.response?.status === 401) router.push('/login')
        else setError('Failed to load user.')
      } finally {
        setIsLoading(false)
      }
    }
    fetchUser()
  }, [id, router])

  const handleSave = async () => {
    try {
      const updated = await apiClient.updateUser(id, form)
      setUser(updated)
      setForm(updated)
      setIsEditing(false)
    } catch {
      setError('Failed to update user.')
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
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/users" className="text-gray-500 hover:text-gray-900 text-sm">
              ← Users
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">User Detail</h1>
          </div>
          {!isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
            >
              Edit
            </button>
          )}
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        <div className="bg-white shadow rounded-lg p-6 space-y-4">
          {[
            { label: 'First Name', key: 'nome' },
            { label: 'Last Name', key: 'cognome' },
            { label: 'Email', key: 'email' },
            { label: 'Phone', key: 'telefono' },
          ].map(({ label, key }) => (
            <div key={key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
              {isEditing ? (
                <input
                  type="text"
                  value={(form as any)[key] ?? ''}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              ) : (
                <p className="text-gray-900">{(user as any)?.[key] ?? '—'}</p>
              )}
            </div>
          ))}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
            {isEditing ? (
              <select
                value={form.ruolo ?? 'user'}
                onChange={(e) => setForm({ ...form, ruolo: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="admin">admin</option>
                <option value="user">user</option>
                <option value="guest">guest</option>
              </select>
            ) : (
              <p className="text-gray-900">{user?.ruolo}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            {isEditing ? (
              <select
                value={form.stato ?? 'active'}
                onChange={(e) => setForm({ ...form, stato: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="active">active</option>
                <option value="inactive">inactive</option>
                <option value="suspended">suspended</option>
              </select>
            ) : (
              <p className="text-gray-900">{user?.stato}</p>
            )}
          </div>

          {isEditing && (
            <div className="flex gap-3 pt-2">
              <button
                onClick={handleSave}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
              >
                Save
              </button>
              <button
                onClick={() => { setIsEditing(false); setForm(user ?? {}) }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
