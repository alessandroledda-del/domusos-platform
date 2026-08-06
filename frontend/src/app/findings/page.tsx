"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Finding = {
  id: number;
  title: string;
  description: string;
  severity: string;
  status: string;
  property: number;
};

export default function FindingsPage() {
  const [items, setItems] = useState<Finding[]>([]);

  async function load() {
    const response = await apiFetch("/compliance/findings/");
    const data = await response.json();
    setItems(data.results ?? data);
  }

  useEffect(() => {
    load();
  }, []);

  async function resolve(id: number) {
    await apiFetch(`/compliance/findings/${id}/`, {
      method: "PATCH",
      body: JSON.stringify({
        status: "RESOLVED",
        resolution_notes: "Risolta tramite pannello DomusOS.",
      }),
    });
    await load();
  }

  return (
    <main className="container">
      <h1>Criticità e findings</h1>
      <div className="grid">
        {items.map(item => (
          <div className="card" key={item.id}>
            <p><span className="badge">{item.severity}</span></p>
            <h2>{item.title}</h2>
            <p>{item.description}</p>
            <p>Stato: {item.status}</p>
            {item.status !== "RESOLVED" && (
              <button className="button" onClick={() => resolve(item.id)}>
                Segna come risolta
              </button>
            )}
          </div>
        ))}
      </div>
    </main>
  );
}
