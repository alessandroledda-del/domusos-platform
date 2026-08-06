"use client";
import { useState } from "react";
import { useParams } from "next/navigation";
import { apiFetch } from "@/lib/api";

export default function DocumentVersionsPage() {
  const params = useParams<{id: string}>();
  const [file, setFile] = useState<File | null>(null);
  const [notes, setNotes] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!file) return;

    const body = new FormData();
    body.append("file", file);
    body.append("notes", notes);

    const response = await apiFetch(`/documents/${params.id}/add_version/`, {
      method: "POST",
      body,
    });
    setMessage(response.ok ? "Nuova versione caricata." : "Errore durante il caricamento.");
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit}>
        <h1>Nuova versione documento</h1>
        <label>File</label>
        <input
          className="input"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={event => setFile(event.target.files?.[0] ?? null)}
          required
        />
        <label>Note versione</label>
        <textarea
          className="input"
          value={notes}
          onChange={event => setNotes(event.target.value)}
        />
        <button className="button" type="submit">Carica versione</button>
        {message && <p>{message}</p>}
      </form>
    </main>
  );
}
