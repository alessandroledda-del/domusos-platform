"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

export default function NewPropertyPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    company: "",
    title: "",
    address: "",
    municipality: "",
    province: "",
    postal_code: "",
    cadastral_sheet: "",
    cadastral_particle: "",
    cadastral_subaltern: "",
    cadastral_category: "",
  });
  const [error, setError] = useState("");

  function update(name: string, value: string) {
    setForm(current => ({...current, [name]: value}));
  }

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const response = await apiFetch("/properties/items/", {
      method: "POST",
      body: JSON.stringify({...form, company: Number(form.company)}),
    });
    if (!response.ok) {
      setError("Verifica i dati e l'ID azienda.");
      return;
    }
    router.push("/properties");
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit}>
        <h1>Nuovo immobile</h1>
        <label>ID azienda</label>
        <input className="input" value={form.company} onChange={e => update("company", e.target.value)} required />
        <label>Titolo</label>
        <input className="input" value={form.title} onChange={e => update("title", e.target.value)} required />
        <label>Indirizzo</label>
        <input className="input" value={form.address} onChange={e => update("address", e.target.value)} required />
        <label>Comune</label>
        <input className="input" value={form.municipality} onChange={e => update("municipality", e.target.value)} required />
        <label>Provincia</label>
        <input className="input" maxLength={2} value={form.province} onChange={e => update("province", e.target.value.toUpperCase())} required />
        <label>Foglio</label>
        <input className="input" value={form.cadastral_sheet} onChange={e => update("cadastral_sheet", e.target.value)} />
        <label>Particella</label>
        <input className="input" value={form.cadastral_particle} onChange={e => update("cadastral_particle", e.target.value)} />
        <label>Subalterno</label>
        <input className="input" value={form.cadastral_subaltern} onChange={e => update("cadastral_subaltern", e.target.value)} />
        {error && <p>{error}</p>}
        <button className="button" type="submit">Salva immobile</button>
      </form>
    </main>
  );
}
