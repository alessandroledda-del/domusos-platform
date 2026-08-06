"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Assignment = {
  id: number;
  case_title: string;
  status: string;
  agreed_amount: string;
  partner_net_amount: string;
  due_at: string | null;
};

export default function PartnerConsolePage() {
  const [items, setItems] = useState<Assignment[]>([]);

  async function load() {
    const response = await apiFetch("/marketplace/assignments/");
    const data = await response.json();
    setItems(data.results ?? data);
  }

  useEffect(() => {
    load();
  }, []);

  async function action(id: number, actionName: "accept" | "complete") {
    await apiFetch(`/marketplace/assignments/${id}/${actionName}/`, {method: "POST"});
    await load();
  }

  return (
    <main className="container">
      <h1>Console partner</h1>
      <div className="grid">
        {items.map(item => (
          <div className="card" key={item.id}>
            <h2>{item.case_title}</h2>
            <p><span className="badge">{item.status}</span></p>
            <p>Compenso lordo: EUR {item.agreed_amount}</p>
            <p>Netto partner: EUR {item.partner_net_amount}</p>
            <p>Scadenza: {item.due_at ? new Date(item.due_at).toLocaleString("it-IT") : "-"}</p>
            {item.status === "PROPOSED" && (
              <button className="button" onClick={() => action(item.id, "accept")}>Accetta</button>
            )}{" "}
            {["ACCEPTED", "IN_PROGRESS"].includes(item.status) && (
              <button className="button" onClick={() => action(item.id, "complete")}>Completa</button>
            )}
          </div>
        ))}
      </div>
    </main>
  );
}
