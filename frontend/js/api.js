import { getToken } from "./auth.js";

export async function apiFetch(path, options = {}) {
  const token = getToken();

  const res = await fetch(`/api${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });
  const isJson = (res.headers.get("content-type") || "").includes("application/json");
  const data = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null);

  if (!res.ok) {
    throw data ?? { detail: `Request failed: ${res.status}` };
  }

  return data;
}
