"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Owner = {
  id: number;
  first_name: string;
  last_name: string;
  ownership_percentage: string;
};

type Property = {
  id: number;
  title: string;
  address: string;
  municipality: string;
  province: string;
  status: string;
  domus_score: number;
  owners: Owner[];
  documents_count: number;
};

export default function PropertyDetailPage() {
  const params = useParams<{id: string}>();
  const [item, setItem] = useState<Property | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiFetch(`/properties/items/${params.id}/`)
      .then(response => response.json())
      .then(setItem);
  }, [params.id]);

  async function refreshScore() {
    const response = await apiFetch(`/properties/items/${params.id}/refresh_score/`, {method: "POST"});
    const data = await response.json();
    setItem(current => current ? {...current, domus_score: data.domus_score} : current);
  }

  async function generateReport() {
    const response = await apiFetch("/reports/generate/", {
      method: "POST",
      body: JSON.stringify({property: Number(params.id)}),
    });
    setMessage(response.ok ? "Report generato." : "Errore nella generazione.");
  }

  if (!item) return <main className="container"><p>Caricamento...</p></main>;

  return (
    <main className="container">
      <div className="card">
        <h1>{item.title}</h1>
        <p>{item.address}, {item.municipality} ({item.province})</p>
        <p>Stato: <span className="badge">{item.status}</span></p>
        <p>Domus Score: <strong>{item.domus_score}/100</strong></p>
        <p>Documenti: {item.documents_count}</p>
        <button className="button" onClick={refreshScore}>Ricalcola score</button>{" "}
        <button className="button" onClick={generateReport}>Genera report PDF</button>{" "}
        <Link className="button" href={`/properties/${item.id}/verification`}>Verifica conformità</Link>
        {message && <p>{message}</p>}
      </div>

      <div className="card" style={{marginTop: 16}}>
        <h2>Proprietari</h2>
        {item.owners.length === 0 && <p>Nessun proprietario registrato.</p>}
        {item.owners.map(owner => (
          <p key={owner.id}>
            {owner.first_name} {owner.last_name} — {owner.ownership_percentage}%
          </p>
        ))}
      </div>
    </main>
  );
}
