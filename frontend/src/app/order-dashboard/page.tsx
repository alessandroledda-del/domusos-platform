"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type OrderDashboard = {
  orders_total: number;
  revenue_total: string;
  awaiting_payment: number;
  in_progress: number;
  completed: number;
  sla_at_risk: number;
};

export default function OrderDashboardPage() {
  const [data, setData] = useState<OrderDashboard | null>(null);

  useEffect(() => {
    apiFetch("/orders/dashboard/")
      .then(response => response.json())
      .then(setData);
  }, []);

  return (
    <main className="container">
      <h1>Dashboard ordini</h1>
      <div className="grid">
        <div className="card"><h2>Ordini</h2><p>{data?.orders_total ?? "-"}</p></div>
        <div className="card"><h2>Valore</h2><p>EUR {data?.revenue_total ?? "-"}</p></div>
        <div className="card"><h2>Da pagare</h2><p>{data?.awaiting_payment ?? "-"}</p></div>
        <div className="card"><h2>In lavorazione</h2><p>{data?.in_progress ?? "-"}</p></div>
        <div className="card"><h2>Completati</h2><p>{data?.completed ?? "-"}</p></div>
        <div className="card"><h2>SLA monitorati</h2><p>{data?.sla_at_risk ?? "-"}</p></div>
      </div>
    </main>
  );
}
