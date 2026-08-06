"use client";
import { useEffect, useState } from "react";

type Health = {
  status: string;
  database: boolean;
  redis: boolean;
  version: string;
};

export default function SystemPage() {
  const [health, setHealth] = useState<Health | null>(null);
  const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

  useEffect(() => {
    fetch(`${apiBase}/health/`)
      .then(response => response.json())
      .then(setHealth)
      .catch(() => setHealth(null));
  }, [apiBase]);

  return (
    <main className="container">
      <h1>Stato sistema</h1>
      <div className="grid">
        <div className="card"><h2>Applicazione</h2><p>{health?.status ?? "non disponibile"}</p></div>
        <div className="card"><h2>Database</h2><p>{health?.database ? "online" : "offline"}</p></div>
        <div className="card"><h2>Redis</h2><p>{health?.redis ? "online" : "offline"}</p></div>
        <div className="card"><h2>Versione</h2><p>{health?.version ?? "-"}</p></div>
      </div>
      <div className="card" style={{marginTop: 16}}>
        <a className="button" href="http://localhost:8000/api/docs/" target="_blank">
          Apri Swagger API
        </a>
      </div>
    </main>
  );
}
