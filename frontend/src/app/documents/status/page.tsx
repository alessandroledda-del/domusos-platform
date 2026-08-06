"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type DocumentItem = {
  id: number;
  name: string;
  document_type: string;
  status: string;
  processing_confidence: string | null;
  processing_error: string;
  processed_at: string | null;
};

export default function DocumentStatusPage() {
  const [items, setItems] = useState<DocumentItem[]>([]);

  async function load() {
    const response = await apiFetch("/documents/");
    const data = await response.json();
    setItems(data.results ?? data);
  }

  useEffect(() => {
    load();
    const timer = window.setInterval(load, 5000);
    return () => window.clearInterval(timer);
  }, []);

  async function reprocess(id: number) {
    await apiFetch(`/documents/${id}/process/`, {method: "POST"});
    await load();
  }

  return (
    <main className="container">
      <h1>Elaborazione documenti</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Documento</th>
              <th>Tipo</th>
              <th>Stato</th>
              <th>Confidenza</th>
              <th>Azione</th>
            </tr>
          </thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id}>
                <td>{item.name}{item.processing_error && <><br/><small>{item.processing_error}</small></>}</td>
                <td>{item.document_type}</td>
                <td><span className="badge">{item.status}</span></td>
                <td>{item.processing_confidence ?? "-"}</td>
                <td>
                  <button className="button" onClick={() => reprocess(item.id)}>
                    Rielabora
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
