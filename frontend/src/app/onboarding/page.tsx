"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Progress = {
  organization_created: boolean;
  profile_completed: boolean;
  first_property_created: boolean;
  first_document_uploaded: boolean;
  first_service_ordered: boolean;
  first_verification_run: boolean;
  completed: boolean;
  completion_percentage: number;
};

const steps = [
  ["organization_created", "Crea l'organizzazione", "/companies"],
  ["profile_completed", "Completa il profilo", "/dashboard"],
  ["first_property_created", "Inserisci il primo immobile", "/properties/new"],
  ["first_document_uploaded", "Carica il primo documento", "/documents"],
  ["first_service_ordered", "Ordina il primo servizio", "/catalog"],
  ["first_verification_run", "Esegui la prima verifica", "/properties"],
] as const;

export default function OnboardingPage() {
  const [progress, setProgress] = useState<Progress | null>(null);

  async function load() {
    const response = await apiFetch("/onboarding/");
    setProgress(await response.json());
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <main className="container">
      <div className="card">
        <h1>Configurazione DomusOS</h1>
        <p>Completamento: <strong>{progress?.completion_percentage ?? 0}%</strong></p>
        <progress value={progress?.completion_percentage ?? 0} max={100} style={{width: "100%"}} />
      </div>

      <div className="grid" style={{marginTop: 16}}>
        {steps.map(([field, label, href]) => {
          const completed = Boolean(progress?.[field]);
          return (
            <div className="card" key={field}>
              <p><span className="badge">{completed ? "COMPLETATO" : "DA FARE"}</span></p>
              <h2>{label}</h2>
              {!completed && <Link className="button" href={href}>Apri</Link>}
            </div>
          );
        })}
      </div>
    </main>
  );
}
