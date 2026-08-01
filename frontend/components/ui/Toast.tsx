'use client'

import { Toaster } from 'react-hot-toast'

export function Toast() {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          borderRadius: '0.75rem',
          background: '#0f172a',
          color: '#f8fafc',
        },
      }}
    />
  )
}
