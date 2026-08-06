"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type MarketplaceDashboard = {
  partners_active: number;
  assignments_open: number;
  assignments_completed: number;
  commissions_earned: string;
  partner_payable: string;
  payouts_pending: number;
};

export default function AdminEconomicsPage() {
  const [data, setData] = useState<MarketplaceDashboard | null>(null);

  useEffect(() => {
    apiFetch("/marketplace/dashboard/")
      .then(response => response.json())
      .then(setData);
  }, []);

  return (
    <main className="container">
      <h1>Amministrazione economica</h1>
      <div className="grid">
        <div className="card"><h2>Partner attivi</h2><p>{data?.partners_active ?? "-"}</p></div>
        <div className="card"><h2>Assegnazioni aperte</h2><p>{data?.assignments_open ?? "-"}</p></div>
        <div className="card"><h2>Completate</h2><p>{data?.assignments_completed ?? "-"}</p></div>
        <div className="card"><h2>Commissioni DomusOS</h2><p>EUR {data?.commissions_earned ?? "-"}</p></div>
        <div className="card"><h2>Da riconoscere ai partner</h2><p>EUR {data?.partner_payable ?? "-"}</p></div>
        <div className="card"><h2>Payout pendenti</h2><p>{data?.payouts_pending ?? "-"}</p></div>
      </div>
    </main>
  );
}
