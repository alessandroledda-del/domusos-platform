'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { apiClient } from '@/lib/api-client'

interface Property {
  id: number
  indirizzo: string
  comune: string
  provincia: string
  foglio: string
  particella: string
  subalterno?: string
  categoria_catastale: string
  domus_score?: number | null
  status: string
  company: number | { id: number; ragione_sociale: string }
}

const STATUS_OPTIONS = ['active', 'inactive', 'archived']

export default function PropertyDetailPage() {
  const router = useRouter()
  const params = useParams()
  const id = Number(params.id)

  const [property, setProperty] = useState<Property | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [form, setForm] = useState<Partial<Property>>({})
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchProperty = async () => {
      try {
        const data = await apiClient.getPropertyById(id)
        setProperty(data)
        setForm(data)
      } catch (err: any) {
        if (err.response?.status === 401) router.push('/login')
        else setError('Failed to load property.')
      } finally {
        setIsLoading(false)
      }
    }
    fetchProperty()
  }, [id, router])

  const handleSave = async () => {
    try {
      const updated = await apiClient.updateProperty(id, form)
      setProperty(updated)
      setForm(updated)
      setIsEditing(false)
    } catch {
      setError('Failed to update property.')
    }
  }

  const handleUpdateScore = async () => {
    const scoreStr = prompt('Enter new Domus Score (0 – 100):')
    if (scoreStr === null) return
    const score = parseFloat(scoreStr)
    if (isNaN(score) || score < 0 || score > 100) {
      alert('Invalid score. Must be a number between 0 and 100.')
      return
    }
    try {
      const updated = await apiClient.updatePropertyScore(id, score)
      setProperty(updated)
      setForm(updated)
    } catch {
      setError('Failed to update score.')
    }
  }

  const companyName =
    property?.company && typeof property.company === 'object'
      ? property.company.ragione_sociale
      : String(property?.company ?? '—')

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
            <Link href="/properties" className="text-gray-500 hover:text-gray-900 text-sm">
              ← Properties
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Property Detail</h1>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleUpdateScore}
              className="px-4 py-2 text-sm font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 rounded-lg"
            >
              Update Score
            </button>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
              >
                Edit
              </button>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
            {error}
          </div>
        )}

        <div className="bg-white shadow rounded-lg p-6 space-y-4">
          {/* Domus Score banner */}
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 flex items-center justify-between">
            <span className="text-sm font-medium text-indigo-700">Domus Score</span>
            <span className="text-3xl font-bold text-indigo-800">
              {property?.domus_score != null ? Number(property.domus_score).toFixed(2) : '—'}
            </span>
          </div>

          {[
            { label: 'Address', key: 'indirizzo' },
            { label: 'City', key: 'comune' },
            { label: 'Province', key: 'provincia' },
            { label: 'Foglio', key: 'foglio' },
            { label: 'Particella', key: 'particella' },
            { label: 'Subalterno', key: 'subalterno' },
            { label: 'Categoria Catastale', key: 'categoria_catastale' },
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
                <p className="text-gray-900">{(property as any)?.[key] ?? '—'}</p>
              )}
            </div>
          ))}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            {isEditing ? (
              <select
                value={(form.status as string) ?? 'active'}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                {STATUS_OPTIONS.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            ) : (
              <p className="text-gray-900">{property?.status}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
            <p className="text-gray-900">{companyName}</p>
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
                onClick={() => { setIsEditing(false); setForm(property ?? {}) }}
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
