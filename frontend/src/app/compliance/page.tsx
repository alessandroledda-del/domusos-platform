"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Dashboard = {
  properties_total: number;
  verified_properties: number;
  properties_with_issues: number;
  verification_runs: number;
  open_findings: number;
  critical_findings: number;
  high_findings: number;
};

export default function ComplianceDashboardPage() {
  const [data, setData] = useState<Dashboard | null>(null);

  useEffect(() => {
    apiFetch("/compliance/dashboard/")
      .then(response => response.json())
      .then(setData);
  }, []);

  return (
    <main className="container">
      <h1>Conformità immobiliare</h1>
      <div className="grid">
        <div className="card"><h2>Immobili</h2><p>{data?.properties_total ?? "-"}</p></div>
        <div className="card"><h2>Domus Verified</h2><p>{data?.verified_properties ?? "-"}</p></div>
        <div className="card"><h2>Con criticità</h2><p>{data?.properties_with_issues ?? "-"}</p></div>
        <div className="card"><h2>Verifiche</h2><p>{data?.verification_runs ?? "-"}</p></div>
        <div className="card"><h2>Finding aperti</h2><p>{data?.open_findings ?? "-"}</p></div>
        <div className="card"><h2>Critici</h2><p>{data?.critical_findings ?? "-"}</p></div>
        <div className="card"><h2>Alti</h2><p>{data?.high_findings ?? "-"}</p></div>
      </div>
    </main>
  );
}
