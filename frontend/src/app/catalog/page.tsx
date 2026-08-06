"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";

type Service = {
  id: number;
  code: string;
  name: string;
  short_description: string;
  category_name: string;
  base_price: string;
  gross_price: string;
  sla_hours: number;
  is_featured: boolean;
};

export default function CatalogPage() {
  const [items, setItems] = useState<Service[]>([]);
  const [category, setCategory] = useState("");

  useEffect(() => {
    const suffix = category ? `?category=${encodeURIComponent(category)}` : "";
    apiFetch(`/catalog/services/${suffix}`)
      .then(response => response.json())
      .then(data => setItems(data.results ?? data));
  }, [category]);

  return (
    <main className="container">
      <h1>Catalogo servizi</h1>
      <div className="card">
        <label>Area</label>
        <select className="select" value={category} onChange={event => setCategory(event.target.value)}>
          <option value="">Tutte</option>
          <option value="catasto">Catasto</option>
          <option value="conservatoria">Conservatoria</option>
          <option value="camera-commercio">Camera di Commercio</option>
          <option value="pra">PRA</option>
          <option value="dossier">Dossier</option>
        </select>
      </div>

      <div className="grid" style={{marginTop: 16}}>
        {items.map(item => (
          <div className="card" key={item.id}>
            <p><span className="badge">{item.category_name}</span></p>
            <h2>{item.name}</h2>
            <p>{item.short_description}</p>
            <p><strong>EUR {item.gross_price}</strong> IVA inclusa</p>
            <p>Consegna indicativa: {item.sla_hours} ore</p>
            <Link className="button" href={`/checkout?service=${item.id}`}>
              Acquista
            </Link>
          </div>
        ))}
      </div>
    </main>
  );
}
