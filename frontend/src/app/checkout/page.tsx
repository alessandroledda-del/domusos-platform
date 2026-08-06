"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function CheckoutPage() {
  const params = useSearchParams();
  const router = useRouter();
  const serviceId = params.get("service") ?? "";
  const [company, setCompany] = useState("");
  const [property, setProperty] = useState("");
  const [notes, setNotes] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const payload: Record<string, unknown> = {
      service_ids: [Number(serviceId)],
      customer_notes: notes,
    };
    if (company) payload.company = Number(company);
    if (property) payload.property = Number(property);

    const response = await apiFetch("/orders/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      setMessage("Impossibile creare l'ordine.");
      return;
    }
    const order = await response.json();
    router.push(`/orders/${order.id}`);
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit}>
        <h1>Checkout servizio</h1>
        <p>Servizio selezionato: ID {serviceId}</p>
        <label>ID organizzazione</label>
        <input className="input" value={company} onChange={event => setCompany(event.target.value)} />
        <label>ID immobile</label>
        <input className="input" value={property} onChange={event => setProperty(event.target.value)} />
        <label>Dati e note per l'evasione</label>
        <textarea className="input" value={notes} onChange={event => setNotes(event.target.value)} />
        <button className="button" type="submit">Crea ordine</button>
        {message && <p>{message}</p>}
      </form>
    </main>
  );
}
