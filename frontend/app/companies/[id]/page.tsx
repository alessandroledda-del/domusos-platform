'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { apiClient } from '@/lib/api-client'

interface Company {
  id: number
  ragione_sociale: string
  partita_iva: string
  tipo_cliente: string
  email: string
  telefono?: string
}

const CLIENT_TYPES = ['enterprise', 'pme', 'freelance', 'other']

export default function CompanyDetailPage() {
  const router = useRouter()
  const params = useParams()
  const id = Number(params.id)

  const [company, setCompany] = useState<Company | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [form, setForm] = useState<Partial<Company>>({})
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchCompany = async () => {
      try {
        const data = await apiClient.getCompanyById(id)
        setCompany(data)
        setForm(data)
      } catch (err: any) {
        if (err.response?.status === 401) router.push('/login')
        else setError('Failed to load company.')
      } finally {
        setIsLoading(false)
      }
    }
    fetchCompany()
  }, [id, router])

  const handleSave = async () => {
    try {
      const updated = await apiClient.updateCompany(id, form)
      setCompany(updated)
      setForm(updated)
      setIsEditing(false)
    } catch {
      setError('Failed to update company.')
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
            <Link href="/companies" className="text-gray-500 hover:text-gray-900 text-sm">
              ← Companies
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Company Detail</h1>
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
            { label: 'Company Name', key: 'ragione_sociale' },
            { label: 'VAT Number', key: 'partita_iva' },
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
                <p className="text-gray-900">{(company as any)?.[key] ?? '—'}</p>
              )}
            </div>
          ))}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Client Type</label>
            {isEditing ? (
              <select
                value={form.tipo_cliente ?? ''}
                onChange={(e) => setForm({ ...form, tipo_cliente: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                {CLIENT_TYPES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            ) : (
              <p className="text-gray-900">{company?.tipo_cliente}</p>
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
                onClick={() => { setIsEditing(false); setForm(company ?? {}) }}
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
