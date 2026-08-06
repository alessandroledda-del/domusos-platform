"use client";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Notification = {
  id: number;
  title: string;
  message: string;
  level: string;
  is_read: boolean;
};

export default function NotificationsPage() {
  const [items, setItems] = useState<Notification[]>([]);

  useEffect(() => {
    apiFetch("/notifications/")
      .then(response => response.json())
      .then(data => setItems(data.results ?? data));
  }, []);

  async function markRead(id: number) {
    await apiFetch(`/notifications/${id}/mark_read/`, {method: "POST"});
    setItems(current => current.map(item => item.id === id ? {...item, is_read: true} : item));
  }

  return (
    <main className="container">
      <h1>Notifiche</h1>
      <div className="grid">
        {items.map(item => (
          <div className="card" key={item.id}>
            <h2>{item.title}</h2>
            <p>{item.message}</p>
            <p><span className="badge">{item.level}</span></p>
            {!item.is_read && <button className="button" onClick={() => markRead(item.id)}>Segna come letta</button>}
          </div>
        ))}
      </div>
    </main>
  );
}
