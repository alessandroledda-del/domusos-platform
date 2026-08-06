"use client";
import { useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Results = {
  properties: Array<{id: number; title: string; address: string; municipality: string; domus_score: number}>;
  documents: Array<{id: number; name: string; document_type: string; property_id: number}>;
  cases: Array<{id: number; title: string; status: string; property_id: number}>;
};

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Results | null>(null);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const response = await apiFetch(`/search/?q=${encodeURIComponent(query)}`);
    setResults(await response.json());
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit}>
        <h1>Ricerca globale</h1>
        <input
          className="input"
          value={query}
          onChange={event => setQuery(event.target.value)}
          placeholder="Indirizzo, comune, foglio, particella, documento..."
          minLength={2}
          required
        />
        <button className="button" type="submit">Cerca</button>
      </form>

      {results && (
        <div className="grid" style={{marginTop: 16}}>
          <div className="card">
            <h2>Immobili</h2>
            {results.properties.map(item => (
              <p key={item.id}>
                <Link href={`/properties/${item.id}`}>{item.title}</Link>
              </p>
            ))}
          </div>
          <div className="card">
            <h2>Documenti</h2>
            {results.documents.map(item => (
              <p key={item.id}>{item.name} — {item.document_type}</p>
            ))}
          </div>
          <div className="card">
            <h2>Pratiche</h2>
            {results.cases.map(item => (
              <p key={item.id}>{item.title} — {item.status}</p>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
