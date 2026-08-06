import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "DomusOS",
  description: "Sistema operativo dell'immobile",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="it">
      <body>
        <nav className="nav">
          <strong>DomusOS</strong>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/onboarding">Onboarding</Link>
          <Link href="/catalog">Servizi</Link>
          <Link href="/orders">Ordini</Link>
          <Link href="/order-dashboard">SLA</Link>
          <Link href="/billing">Fatture</Link>
          <Link href="/companies">Organizzazioni</Link>
          <Link href="/properties">Immobili</Link>
          <Link href="/documents">Documenti</Link>
          <Link href="/documents/status">Elaborazione</Link>
          <Link href="/workflows">Pratiche</Link>
          <Link href="/reports">Report</Link>
          <Link href="/compliance">Conformità</Link>
          <Link href="/analytics">Analytics</Link>
          <Link href="/marketplace">Marketplace</Link>
          <Link href="/partner-console">Console partner</Link>
          <Link href="/partner-finance">Economia partner</Link>
          <Link href="/admin-economics">Amministrazione</Link>
          <Link href="/findings">Criticità</Link>
          <Link href="/search">Ricerca</Link>
          <Link href="/customer">Cliente</Link>
          <Link href="/partner">Partner</Link>
          <Link href="/notifications">Notifiche</Link>
          <Link href="/integrations">Integrazioni</Link>
          <Link href="/readiness">Pilot</Link>
          <Link href="/system">Sistema</Link>
          <Link href="/logout">Esci</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
