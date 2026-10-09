const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

export const dashboardClient = {
  async summary() {
    const response = await fetch(`${API_BASE_URL}/dashboard/summary`);
    const data = await response.json();
    if (!response.ok) throw new Error(data?.detail || `Dashboard request failed (${response.status})`);
    return data;
  },
};
