"use client";
import { useState } from "react";
import { apiFetch } from "@/lib/api";

export default function DocumentsPage() {
  const [propertyId, setPropertyId] = useState("");
  const [name, setName] = useState("");
  const [documentType, setDocumentType] = useState("DEED");
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!file) return;
    const body = new FormData();
    body.append("property", propertyId);
    body.append("name", name);
    body.append("document_type", documentType);
    body.append("file", file);

    const response = await apiFetch("/documents/", {method: "POST", body});
    setMessage(response.ok ? "Documento caricato." : "Errore durante il caricamento.");
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit}>
        <h1>Carica documento</h1>
        <label>ID immobile</label>
        <input className="input" value={propertyId} onChange={e => setPropertyId(e.target.value)} required />
        <label>Nome documento</label>
        <input className="input" value={name} onChange={e => setName(e.target.value)} required />
        <label>Tipologia</label>
        <select className="select" value={documentType} onChange={e => setDocumentType(e.target.value)}>
          <option value="DEED">Atto di provenienza</option>
          <option value="CADASTRAL">Visura catastale</option>
          <option value="PLAN">Planimetria</option>
          <option value="ENERGY">APE</option>
          <option value="BUILDING">Titolo edilizio</option>
          <option value="MORTGAGE">Visura ipotecaria</option>
          <option value="OTHER">Altro</option>
        </select>
        <input className="input" type="file" accept=".pdf,.jpg,.jpeg,.png" onChange={e => setFile(e.target.files?.[0] ?? null)} required />
        <button className="button" type="submit">Carica</button>
        {message && <p>{message}</p>}
      </form>
    </main>
  );
}
