"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { apiFetch } from "@/lib/api";

type OrderItem = {
  id: number;
  service_name: string;
  quantity: number;
  line_total: string;
};

type Order = {
  id: number;
  number: string;
  status: string;
  subtotal: string;
  vat_total: string;
  total: string;
  sla_due_at: string | null;
  items: OrderItem[];
};

export default function OrderDetailPage() {
  const params = useParams<{id: string}>();
  const [order, setOrder] = useState<Order | null>(null);
  const [message, setMessage] = useState("");

  async function load() {
    const response = await apiFetch(`/orders/${params.id}/`);
    setOrder(await response.json());
  }

  useEffect(() => {
    load();
  }, [params.id]);

  async function pay() {
    const response = await apiFetch("/billing/payments/mock_checkout/", {
      method: "POST",
      body: JSON.stringify({order: Number(params.id), succeed: true}),
    });
    setMessage(response.ok ? "Pagamento simulato completato." : "Pagamento non riuscito.");
    await load();
  }

  async function invoice() {
    const response = await apiFetch("/billing/invoices/issue/", {
      method: "POST",
      body: JSON.stringify({order: Number(params.id)}),
    });
    setMessage(response.ok ? "Fattura generata." : "Fattura non disponibile.");
  }

  if (!order) return <main className="container"><p>Caricamento...</p></main>;

  return (
    <main className="container">
      <div className="card">
        <h1>{order.number}</h1>
        <p>Stato: <span className="badge">{order.status}</span></p>
        <p>Scadenza SLA: {order.sla_due_at ? new Date(order.sla_due_at).toLocaleString("it-IT") : "-"}</p>
        {order.items.map(item => (
          <p key={item.id}>{item.service_name} — EUR {item.line_total}</p>
        ))}
        <hr />
        <p>Imponibile: EUR {order.subtotal}</p>
        <p>IVA: EUR {order.vat_total}</p>
        <p><strong>Totale: EUR {order.total}</strong></p>
        {order.status === "AWAITING_PAYMENT" && (
          <button className="button" onClick={pay}>Simula pagamento</button>
        )}{" "}
        {["PAID", "IN_PROGRESS", "COMPLETED"].includes(order.status) && (
          <button className="button" onClick={invoice}>Genera fattura</button>
        )}
        {message && <p>{message}</p>}
      </div>
    </main>
  );
}
