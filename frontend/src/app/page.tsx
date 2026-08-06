import Link from "next/link";

export default function Home() {
  return (
    <main className="container">
      <div className="card">
        <h1>DomusOS</h1>
        <p>Il sistema operativo digitale dell'immobile.</p>
        <Link className="button" href="/login">Accedi alla demo</Link>
      </div>
    </main>
  );
}
