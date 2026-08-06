"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Dashboard = {
  properties_total: number;
  properties_verified: number;
  documents_total: number;
  cases_open: number;
  average_domus_score: number;
};

export default function DashboardPage() {
  const [data, setData] = useState<Dashboard | null>(null);

  useEffect(() => {
    apiFetch("/properties/dashboard/")
      .then(response => response.json())
      .then(setData);
  }, []);

  return (
    <main className="container">
      <h1>Dashboard DomusOS</h1>
      <div className="grid">
        <div className="card"><h2>Immobili</h2><p>{data?.properties_total ?? "-"}</p></div>
        <div className="card"><h2>Verificati</h2><p>{data?.properties_verified ?? "-"}</p></div>
        <div className="card"><h2>Documenti</h2><p>{data?.documents_total ?? "-"}</p></div>
        <div className="card"><h2>Pratiche aperte</h2><p>{data?.cases_open ?? "-"}</p></div>
        <div className="card"><h2>Domus Score medio</h2><p>{data?.average_domus_score ?? "-"}</p></div>
      </div>
    </main>
  );
}
