"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type CustomerData = {
  properties: Array<{
    id: number;
    title: string;
    address: string;
    municipality: string;
    domus_score: number;
    documents_count: number;
  }>;
  documents_total: number;
  open_cases: number;
};

export default function CustomerPortalPage() {
  const [data, setData] = useState<CustomerData | null>(null);

  useEffect(() => {
    apiFetch("/properties/customer-portal/")
      .then(response => response.json())
      .then(setData);
  }, []);

  return (
    <main className="container">
      <h1>Portale cliente</h1>
      <div className="grid">
        <div className="card"><h2>Immobili</h2><p>{data?.properties.length ?? "-"}</p></div>
        <div className="card"><h2>Documenti</h2><p>{data?.documents_total ?? "-"}</p></div>
        <div className="card"><h2>Pratiche aperte</h2><p>{data?.open_cases ?? "-"}</p></div>
      </div>

      <div className="card" style={{marginTop: 16}}>
        <h2>I miei immobili</h2>
        {data?.properties.map(item => (
          <p key={item.id}>
            <Link href={`/properties/${item.id}`}><strong>{item.title}</strong></Link>
            {" — "}{item.address}, {item.municipality} — Score {item.domus_score}/100
          </p>
        ))}
      </div>
    </main>
  );
}
