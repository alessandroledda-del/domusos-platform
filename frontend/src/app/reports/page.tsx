"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Report = {
  id: number;
  title: string;
  file: string;
  created_at: string;
};

export default function ReportsPage() {
  const [items, setItems] = useState<Report[]>([]);

  useEffect(() => {
    apiFetch("/reports/")
      .then(response => response.json())
      .then(data => setItems(data.results ?? data));
  }, []);

  return (
    <main className="container">
      <h1>Report</h1>
      <div className="card">
        {items.length === 0 && <p>Nessun report generato.</p>}
        {items.map(report => (
          <p key={report.id}>
            <a href={report.file} target="_blank">{report.title}</a>
          </p>
        ))}
      </div>
    </main>
  );
}
