"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Order = {
  id: number;
  number: string;
  status: string;
  total: string;
  sla_due_at: string | null;
  created_at: string;
};

export default function OrdersPage() {
  const [items, setItems] = useState<Order[]>([]);

  useEffect(() => {
    apiFetch("/orders/")
      .then(response => response.json())
      .then(data => setItems(data.results ?? data));
  }, []);

  return (
    <main className="container">
      <h1>I miei ordini</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr><th>Ordine</th><th>Stato</th><th>Totale</th><th>SLA</th></tr>
          </thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id}>
                <td><Link href={`/orders/${item.id}`}><strong>{item.number}</strong></Link></td>
                <td><span className="badge">{item.status}</span></td>
                <td>EUR {item.total}</td>
                <td>{item.sla_due_at ? new Date(item.sla_due_at).toLocaleString("it-IT") : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
