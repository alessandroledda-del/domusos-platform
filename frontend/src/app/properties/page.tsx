"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Property = {
  id: number;
  title: string;
  address: string;
  municipality: string;
  status: string;
  domus_score: number;
};

export default function PropertiesPage() {
  const [items, setItems] = useState<Property[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch("/properties/items/")
      .then(async response => {
        if (!response.ok) throw new Error("Errore caricamento");
        const data = await response.json();
        setItems(data.results ?? data);
      })
      .catch(() => setError("Impossibile caricare gli immobili."));
  }, []);

  return (
    <main className="container">
      <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
        <h1>Immobili</h1>
        <Link className="button" href="/properties/new">Nuovo immobile</Link>
      </div>
      {error && <p>{error}</p>}
      <div className="card">
        <table className="table">
          <thead><tr><th>Immobile</th><th>Comune</th><th>Stato</th><th>Score</th></tr></thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id}>
                <td><Link href={`/properties/${item.id}`}><strong>{item.title}</strong></Link><br /><small>{item.address}</small></td>
                <td>{item.municipality}</td>
                <td><span className="badge">{item.status}</span></td>
                <td>{item.domus_score}/100</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
