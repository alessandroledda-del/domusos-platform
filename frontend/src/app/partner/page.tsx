"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type PartnerData = {
  assigned_cases: Array<{
    id: number;
    title: string;
    status: string;
    service_type: string;
    due_date: string | null;
  }>;
  open_cases: number;
  overdue_tasks: number;
};

export default function PartnerPortalPage() {
  const [data, setData] = useState<PartnerData | null>(null);

  useEffect(() => {
    apiFetch("/workflows/partner-portal/")
      .then(response => response.json())
      .then(setData);
  }, []);

  return (
    <main className="container">
      <h1>Portale partner</h1>
      <div className="grid">
        <div className="card"><h2>Pratiche aperte</h2><p>{data?.open_cases ?? "-"}</p></div>
        <div className="card"><h2>Attività scadute</h2><p>{data?.overdue_tasks ?? "-"}</p></div>
      </div>

      <div className="card" style={{marginTop: 16}}>
        <h2>Pratiche assegnate</h2>
        {data?.assigned_cases.map(item => (
          <p key={item.id}>
            <strong>{item.title}</strong> — {item.service_type} — {item.status}
          </p>
        ))}
      </div>
    </main>
  );
}
