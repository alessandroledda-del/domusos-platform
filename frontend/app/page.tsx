'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { useAuthStore } from '@/store/authStore'

export default function Home() {
  const router = useRouter()
  const accessToken = useAuthStore((state) => state.accessToken)

  useEffect(() => {
    router.replace(accessToken ? '/dashboard' : '/login')
  }, [accessToken, router])

  return (
    <div className="flex min-h-screen items-center justify-center">
      <LoadingSpinner label="Loading workspace..." />
    </div>
  )
}
