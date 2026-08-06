"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Invoice = {
  id: number;
  number: string;
  order_number: string;
  status: string;
  total: string;
  pdf_file: string;
  issued_at: string | null;
};

export default function BillingPage() {
  const [items, setItems] = useState<Invoice[]>([]);

  useEffect(() => {
    apiFetch("/billing/invoices/")
      .then(response => response.json())
      .then(data => setItems(data.results ?? data));
  }, []);

  return (
    <main className="container">
      <h1>Fatture</h1>
      <div className="card">
        <table className="table">
          <thead><tr><th>Numero</th><th>Ordine</th><th>Totale</th><th>Stato</th><th>PDF</th></tr></thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id}>
                <td>{item.number}</td>
                <td>{item.order_number}</td>
                <td>EUR {item.total}</td>
                <td><span className="badge">{item.status}</span></td>
                <td>{item.pdf_file ? <a href={item.pdf_file} target="_blank">Apri</a> : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
