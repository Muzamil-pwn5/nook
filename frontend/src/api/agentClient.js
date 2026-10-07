const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;
  if (!response.ok) throw new Error(data?.detail || `Request failed (${response.status})`);
  return data;
}

export const agentClient = {
  baseUrl: API_BASE_URL,
  async health() { return request("/health"); },
  async products() { return request("/products"); },
  async createSession() { return request("/agent/session", { method: "POST" }); },
  async chat(sessionId, message) {
    return request("/agent/chat", { method: "POST", body: JSON.stringify({ session_id: sessionId, message }) });
  },
  async approveOrder(sessionId, approvalId) {
    return request(`/agent/session/${sessionId}/approve-order/${approvalId}`, { method: "POST" });
  }
};
