"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Company = {
  id: number;
  name: string;
  vat_number: string;
  company_type: string;
  memberships_count: number;
};

export default function CompaniesPage() {
  const [items, setItems] = useState<Company[]>([]);

  useEffect(() => {
    apiFetch("/companies/organizations/")
      .then(response => response.json())
      .then(data => setItems(data.results ?? data));
  }, []);

  return (
    <main className="container">
      <h1>Organizzazioni</h1>
      <div className="grid">
        {items.map(item => (
          <div className="card" key={item.id}>
            <h2>{item.name}</h2>
            <p>P.IVA: {item.vat_number}</p>
            <p>Tipo: {item.company_type}</p>
            <p>Membri: {item.memberships_count}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
