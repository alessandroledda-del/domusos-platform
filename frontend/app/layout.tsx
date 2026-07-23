import type { Metadata } from 'next'

import { Toast } from '@/components/ui/Toast'

import './globals.css'

export const metadata: Metadata = {
  title: 'DOMUSOS - Real Estate Intelligence',
  description: 'PropTech platform for real estate management and verification',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased transition-colors dark:bg-slate-950 dark:text-slate-100">
        {children}
        <Toast />
      </body>
    </html>
  )
}
