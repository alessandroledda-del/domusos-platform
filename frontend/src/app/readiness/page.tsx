"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Readiness = {
  ready: boolean;
  checks: Record<string, boolean>;
  version: string;
};

export default function ReadinessPage() {
  const [data, setData] = useState<Readiness | null>(null);

  useEffect(() => {
    apiFetch("/readiness/")
      .then(async response => {
        const body = await response.json();
        setData(body);
      });
  }, []);

  return (
    <main className="container">
      <h1>Prontezza pilot</h1>
      <div className="card">
        <p><span className="badge">{data?.ready ? "PRONTO" : "NON PRONTO"}</span></p>
        <p>Versione: {data?.version ?? "-"}</p>
      </div>
      <div className="grid" style={{marginTop: 16}}>
        {data && Object.entries(data.checks).map(([key, value]) => (
          <div className="card" key={key}>
            <h2>{key.replaceAll("_", " ")}</h2>
            <p>{value ? "OK" : "Da completare"}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
