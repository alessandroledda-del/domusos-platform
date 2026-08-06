"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { API_URL } from "@/lib/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setError("");
    const response = await fetch(`${API_URL}/auth/token/`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({email, password}),
    });
    if (!response.ok) {
      setError("Credenziali non valide.");
      return;
    }
    const data = await response.json();
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    router.push("/dashboard");
  }

  return (
    <main className="container">
      <form className="card" onSubmit={submit} style={{maxWidth: 460, margin: "60px auto"}}>
        <h1>Accesso DomusOS</h1>
        <label>Email</label>
        <input className="input" value={email} onChange={e => setEmail(e.target.value)} type="email" required />
        <label>Password</label>
        <input className="input" value={password} onChange={e => setPassword(e.target.value)} type="password" required />
        {error && <p>{error}</p>}
        <button className="button" type="submit">Accedi</button>
      </form>
    </main>
  );
}
