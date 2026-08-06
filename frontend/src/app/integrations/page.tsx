"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Endpoint = {
  id: number;
  name: string;
  url: string;
  subscribed_events: string[];
  is_active: boolean;
};

export default function IntegrationsPage() {
  const [items, setItems] = useState<Endpoint[]>([]);
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [secret, setSecret] = useState("");

  async function load() {
    const response = await apiFetch("/integrations/webhook-endpoints/");
    const data = await response.json();
    setItems(data.results ?? data);
  }

  useEffect(() => {
    load();
  }, []);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    await apiFetch("/integrations/webhook-endpoints/", {
      method: "POST",
      body: JSON.stringify({
        name,
        url,
        secret,
        subscribed_events: [
          "order.status_changed",
          "document.processed",
          "invoice.issued"
        ],
      }),
    });
    setName("");
    setUrl("");
    setSecret("");
    await load();
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit}>
        <h1>Integrazioni webhook</h1>
        <label>Nome</label>
        <input className="input" value={name} onChange={e => setName(e.target.value)} required />
        <label>URL HTTPS</label>
        <input className="input" type="url" value={url} onChange={e => setUrl(e.target.value)} required />
        <label>Segreto HMAC</label>
        <input className="input" value={secret} onChange={e => setSecret(e.target.value)} />
        <button className="button" type="submit">Crea endpoint</button>
      </form>

      <div className="grid" style={{marginTop: 16}}>
        {items.map(item => (
          <div className="card" key={item.id}>
            <h2>{item.name}</h2>
            <p>{item.url}</p>
            <p><span className="badge">{item.is_active ? "ATTIVO" : "DISATTIVO"}</span></p>
            <p>{item.subscribed_events.join(", ")}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
