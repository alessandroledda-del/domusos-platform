export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

let refreshPromise: Promise<string | null> | null = null;

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

export function logout(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/login";
}

async function refreshAccessToken(): Promise<string | null> {
  if (typeof window === "undefined") return null;

  const refresh = localStorage.getItem("refresh_token");
  if (!refresh) return null;

  const response = await fetch(`${API_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({refresh}),
  });

  if (!response.ok) {
    logout();
    return null;
  }

  const data = await response.json();
  localStorage.setItem("access_token", data.access);
  if (data.refresh) {
    localStorage.setItem("refresh_token", data.refresh);
  }
  return data.access;
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
  retry = true,
): Promise<Response> {
  const token = getToken();
  const headers = new Headers(options.headers);

  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  let response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && retry) {
    refreshPromise ??= refreshAccessToken().finally(() => {
      refreshPromise = null;
    });
    const newToken = await refreshPromise;
    if (newToken) {
      headers.set("Authorization", `Bearer ${newToken}`);
      response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers,
      });
    }
  }

  if (response.status === 401 && typeof window !== "undefined") {
    logout();
  }

  return response;
}

export async function downloadAuthenticated(
  path: string,
  filename: string,
): Promise<void> {
  const response = await apiFetch(path);
  if (!response.ok) {
    throw new Error("Download non disponibile.");
  }
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
