"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { apiFetch } from "@/lib/api";

type Finding = {
  id: number;
  title: string;
  description: string;
  severity: string;
  status: string;
};

type Verification = {
  id: number;
  status: string;
  score: number;
  passed_rules: number;
  warning_rules: number;
  failed_rules: number;
  summary: {
    verified_level?: string;
    rules?: Array<{
      code: string;
      title: string;
      passed: boolean;
      severity: string;
      description: string;
    }>;
  };
  findings: Finding[];
};

export default function PropertyVerificationPage() {
  const params = useParams<{id: string}>();
  const [verification, setVerification] = useState<Verification | null>(null);
  const [message, setMessage] = useState("");

  async function runVerification() {
    const response = await apiFetch("/compliance/verifications/run/", {
      method: "POST",
      body: JSON.stringify({property: Number(params.id)}),
    });
    if (!response.ok) {
      setMessage("Impossibile eseguire la verifica.");
      return;
    }
    setVerification(await response.json());
    setMessage("Verifica completata.");
  }

  async function issueCertificate() {
    if (!verification) return;
    const response = await apiFetch(
      `/compliance/verifications/${verification.id}/issue_certificate/`,
      {method: "POST"},
    );
    const data = await response.json();
    setMessage(
      response.ok
        ? `Certificato emesso: ${data.public_code}`
        : data.detail ?? "Certificato non emettibile."
    );
  }

  return (
    <main className="container">
      <div className="card">
        <h1>Verifica DomusOS</h1>
        <button className="button" onClick={runVerification}>
          Esegui verifica
        </button>
        {verification && (
          <>
            <h2>Esito: {verification.summary.verified_level}</h2>
            <p>Punteggio: <strong>{verification.score}/100</strong></p>
            <p>Regole superate: {verification.passed_rules}</p>
            <p>Avvisi: {verification.warning_rules}</p>
            <p>Regole fallite: {verification.failed_rules}</p>
            <button className="button" onClick={issueCertificate}>
              Emetti certificato
            </button>
          </>
        )}
        {message && <p>{message}</p>}
      </div>

      {verification?.summary.rules && (
        <div className="grid" style={{marginTop: 16}}>
          {verification.summary.rules.map(rule => (
            <div className="card" key={rule.code}>
              <p><span className="badge">{rule.passed ? "SUPERATA" : rule.severity}</span></p>
              <h2>{rule.title}</h2>
              <p>{rule.description}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
