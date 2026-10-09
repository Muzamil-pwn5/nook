const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = response.headers.get("content-type")?.includes("application/json") ? await response.json() : null;
  if (!response.ok) throw new Error(data?.detail || `Request failed (${response.status})`);
  return data;
}

export const authClient = {
  async register(name, email, password) { return request("/auth/register", { method: "POST", body: JSON.stringify({ name, email, password }) }); },
  async login(email, password) { return request("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }); },
  async me(token) { return request("/auth/me", { headers: { Authorization: `Bearer ${token}` } }); },
  async logout(token) { return request("/auth/logout", { method: "POST", headers: { Authorization: `Bearer ${token}` } }); },
};
