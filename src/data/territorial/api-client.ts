export type BackendState = "disabled" | "connecting" | "online" | "offline";
const configuredBase = (import.meta.env.PUBLIC_LAB_API_BASE_URL ?? "").trim().replace(/\/$/, "");
let failures = 0;
let openUntil = 0;
let state: BackendState = configuredBase ? "connecting" : "disabled";

export const territorialBackend = {
  enabled: Boolean(configuredBase),
  get state() { return state; },
  async request<T>(path: string, init: RequestInit = {}, timeoutMs = 3500): Promise<T | null> {
    if (!configuredBase) return null;
    if (Date.now() < openUntil) { state = "offline"; return null; }
    for (let attempt = 0; attempt < 2; attempt += 1) {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await fetch(`${configuredBase}${path}`, { ...init, signal: controller.signal });
        if (!response.ok) throw new Error(`API ${response.status}`);
        failures = 0; state = "online";
        return await response.json() as T;
      } catch {
        failures += 1;
        if (failures >= 3) openUntil = Date.now() + 30_000;
        state = "offline";
      } finally { clearTimeout(timeout); }
    }
    return null;
  },
};
