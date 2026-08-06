"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Metrics = {
  orders: {
    total: number;
    gross_order_value: string;
    average_order_value: string;
    awaiting_payment: number;
    in_progress: number;
    completed: number;
  };
  payments: {
    succeeded: number;
    collected: string;
    failed: number;
  };
  invoices: {
    issued: number;
    invoiced: string;
  };
  operations: {
    properties: number;
    verified_properties: number;
    documents: number;
    documents_failed: number;
    open_cases: number;
  };
  compliance: {
    verification_runs: number;
    certificates: number;
    open_findings: number;
    critical_findings: number;
  };
};

export default function AnalyticsPage() {
  const [data, setData] = useState<Metrics | null>(null);

  useEffect(() => {
    apiFetch("/analytics/dashboard/")
      .then(response => response.json())
      .then(setData);
  }, []);

  async function snapshot() {
    await apiFetch("/analytics/dashboard/snapshot/", {method: "POST"});
  }

  return (
    <main className="container">
      <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
        <h1>Analytics DomusOS</h1>
        <div>
          <button className="button" onClick={snapshot}>Salva snapshot</button>{" "}
          <a className="button" href="http://localhost:8000/api/analytics/dashboard/export_csv/">
            Esporta CSV
          </a>
        </div>
      </div>

      <div className="grid">
        <div className="card"><h2>Ordini</h2><p>{data?.orders.total ?? "-"}</p></div>
        <div className="card"><h2>Valore ordini</h2><p>EUR {data?.orders.gross_order_value ?? "-"}</p></div>
        <div className="card"><h2>Incassato</h2><p>EUR {data?.payments.collected ?? "-"}</p></div>
        <div className="card"><h2>Fatturato</h2><p>EUR {data?.invoices.invoiced ?? "-"}</p></div>
        <div className="card"><h2>Immobili</h2><p>{data?.operations.properties ?? "-"}</p></div>
        <div className="card"><h2>Domus Verified</h2><p>{data?.operations.verified_properties ?? "-"}</p></div>
        <div className="card"><h2>Pratiche aperte</h2><p>{data?.operations.open_cases ?? "-"}</p></div>
        <div className="card"><h2>Finding critici</h2><p>{data?.compliance.critical_findings ?? "-"}</p></div>
      </div>
    </main>
  );
}
