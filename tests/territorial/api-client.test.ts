import { describe, expect, it, vi } from "vitest";

describe("adaptador de API degradable", () => {
  it("mantiene GitHub Pages estático con configuración pública vacía", async () => {
    vi.stubEnv("PUBLIC_LAB_API_BASE_URL", "");
    vi.resetModules();
    const { territorialBackend } = await import("../../src/data/territorial/api-client");
    expect(territorialBackend.enabled).toBe(false);
    expect(await territorialBackend.request("/health")).toBeNull();
    expect(territorialBackend.state).toBe("disabled");
  });

  it("usa la API configurada y reporta conexión", async () => {
    vi.stubEnv("PUBLIC_LAB_API_BASE_URL", "http://localhost:8001");
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "ok" }),
    }));
    vi.resetModules();
    const { territorialBackend } = await import("../../src/data/territorial/api-client");
    expect(territorialBackend.enabled).toBe(true);
    expect(await territorialBackend.request<{ status: string }>("/health")).toEqual({ status: "ok" });
    expect(territorialBackend.state).toBe("online");
  });

  it("vuelve al modo estático cuando la API configurada está caída", async () => {
    vi.stubEnv("PUBLIC_LAB_API_BASE_URL", "http://localhost:8001");
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("backend caído")));
    vi.resetModules();
    const { territorialBackend } = await import("../../src/data/territorial/api-client");
    expect(await territorialBackend.request("/v1/territories", {}, 10)).toBeNull();
    expect(territorialBackend.state).toBe("offline");
  });
});
