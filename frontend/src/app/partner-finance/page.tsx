"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Commission = {
  id: number;
  partner_name: string;
  gross_amount: string;
  platform_amount: string;
  partner_amount: string;
  status: string;
};

type Payout = {
  id: number;
  number: string;
  partner_name: string;
  amount: string;
  status: string;
  period_start: string;
  period_end: string;
};

export default function PartnerFinancePage() {
  const [commissions, setCommissions] = useState<Commission[]>([]);
  const [payouts, setPayouts] = useState<Payout[]>([]);

  useEffect(() => {
    apiFetch("/marketplace/commissions/")
      .then(response => response.json())
      .then(data => setCommissions(data.results ?? data));
    apiFetch("/marketplace/payouts/")
      .then(response => response.json())
      .then(data => setPayouts(data.results ?? data));
  }, []);

  return (
    <main className="container">
      <h1>Economia partner</h1>
      <div className="card">
        <h2>Commissioni</h2>
        <table className="table">
          <thead><tr><th>Partner</th><th>Lordo</th><th>DomusOS</th><th>Partner</th><th>Stato</th></tr></thead>
          <tbody>
            {commissions.map(item => (
              <tr key={item.id}>
                <td>{item.partner_name}</td>
                <td>EUR {item.gross_amount}</td>
                <td>EUR {item.platform_amount}</td>
                <td>EUR {item.partner_amount}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card" style={{marginTop: 16}}>
        <h2>Payout</h2>
        <table className="table">
          <thead><tr><th>Numero</th><th>Partner</th><th>Importo</th><th>Periodo</th><th>Stato</th></tr></thead>
          <tbody>
            {payouts.map(item => (
              <tr key={item.id}>
                <td>{item.number}</td>
                <td>{item.partner_name}</td>
                <td>EUR {item.amount}</td>
                <td>{item.period_start} / {item.period_end}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
