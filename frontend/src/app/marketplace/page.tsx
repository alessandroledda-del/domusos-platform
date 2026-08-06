"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Partner = {
  id: number;
  display_name: string;
  professional_type: string;
  provinces: string[];
  rating: string;
  sla_compliance_rate: string;
  completed_assignments: number;
  rank_score: string;
};

export default function MarketplacePage() {
  const [items, setItems] = useState<Partner[]>([]);
  const [province, setProvince] = useState("");

  useEffect(() => {
    const suffix = province ? `?province=${province}` : "";
    apiFetch(`/marketplace/partners/ranked/${suffix}`)
      .then(response => response.json())
      .then(setItems);
  }, [province]);

  return (
    <main className="container">
      <h1>DomusPartner Marketplace</h1>
      <div className="card">
        <label>Provincia</label>
        <input
          className="input"
          maxLength={2}
          value={province}
          onChange={event => setProvince(event.target.value.toUpperCase())}
          placeholder="RM"
        />
      </div>

      <div className="grid" style={{marginTop: 16}}>
        {items.map(item => (
          <div className="card" key={item.id}>
            <p><span className="badge">{item.professional_type}</span></p>
            <h2>{item.display_name}</h2>
            <p>Province: {item.provinces.join(", ")}</p>
            <p>Rating: {item.rating}/5</p>
            <p>SLA rispettati: {item.sla_compliance_rate}%</p>
            <p>Pratiche completate: {item.completed_assignments}</p>
            <p>Ranking: {item.rank_score}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
