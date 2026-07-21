import type { Metadata } from 'next'
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
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
