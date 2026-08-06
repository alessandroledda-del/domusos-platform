"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type PublicCertificate = {
  valid: boolean;
  public_code: string;
  status: string;
  property: {
    title: string;
    municipality: string;
    province: string;
  };
  verified_level: string;
  score: number;
  issued_at: string;
  expires_at: string;
  disclaimer: string;
};

export default function PublicVerifyPage() {
  const params = useParams<{code: string}>();
  const [data, setData] = useState<PublicCertificate | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
    fetch(`${base}/compliance/public/${params.code}/`)
      .then(async response => {
        if (!response.ok) throw new Error("Certificato non trovato");
        return response.json();
      })
      .then(setData)
      .catch(() => setError("Certificato non valido o non disponibile."));
  }, [params.code]);

  return (
    <main className="container">
      <div className="card" style={{maxWidth: 720, margin: "40px auto"}}>
        <h1>Verifica Domus Verified</h1>
        {error && <p>{error}</p>}
        {data && (
          <>
            <p><span className="badge">{data.valid ? "VALIDO" : data.status}</span></p>
            <h2>{data.property.title}</h2>
            <p>{data.property.municipality} ({data.property.province})</p>
            <p>Livello: <strong>{data.verified_level}</strong></p>
            <p>Punteggio: <strong>{data.score}/100</strong></p>
            <p>Codice: {data.public_code}</p>
            <p>Scadenza: {new Date(data.expires_at).toLocaleDateString("it-IT")}</p>
            <hr />
            <small>{data.disclaimer}</small>
          </>
        )}
      </div>
    </main>
  );
}
