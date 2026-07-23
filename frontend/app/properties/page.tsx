'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
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
  company: number
  company_name: string
  created_at: string
}

export default function PropertiesPage() {
  const router = useRouter()
  const [properties, setProperties] = useState<Property[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const data = await apiClient.getProperties()
        setProperties(data.results ?? data)
      } catch (err: any) {
        if (err.response?.status === 401) {
          router.push('/login')
        } else {
          setError('Failed to load properties.')
        }
      } finally {
        setIsLoading(false)
      }
    }
    fetchProperties()
  }, [router])

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this property?')) return
    try {
      await apiClient.deleteProperty(id)
      setProperties((prev) => prev.filter((p) => p.id !== id))
    } catch {
      alert('Failed to delete property.')
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
            <h1 className="text-2xl font-bold text-gray-900">Properties</h1>
          </div>
          <Link
            href="/properties/new"
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
          >
            + New Property
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
                {['Address', 'City', 'Prov.', 'Company', 'Domus Score', 'Status', 'Actions'].map(
                  (h) => (
                    <th
                      key={h}
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {h}
                    </th>
                  )
                )}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {properties.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                    No properties found.
                  </td>
                </tr>
              ) : (
                properties.map((property) => (
                  <tr key={property.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {property.indirizzo}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {property.comune}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {property.provincia}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {property.company_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {property.domus_score != null ? (
                        <span className="font-semibold text-indigo-700">
                          {Number(property.domus_score).toFixed(2)}
                        </span>
                      ) : (
                        <span className="text-gray-400">—</span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          property.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : property.status === 'archived'
                            ? 'bg-gray-100 text-gray-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {property.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium flex gap-3">
                      <Link
                        href={`/properties/${property.id}`}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        View
                      </Link>
                      <button
                        onClick={() => handleDelete(property.id)}
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
