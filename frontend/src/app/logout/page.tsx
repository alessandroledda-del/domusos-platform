"use client";
import { useEffect } from "react";
import { logout } from "@/lib/api";

export default function LogoutPage() {
  useEffect(() => {
    logout();
  }, []);

  return (
    <main className="container">
      <p>Disconnessione...</p>
    </main>
  );
}
