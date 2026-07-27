export type AnalyticsRequest = {
  id: string;
  sql: string;
  parquetUrl: string;
  fallbackUrl: string;
  timeoutMs?: number;
  maxBytes?: number;
};

export type AnalyticsResponse = {
  id: string;
  ok: boolean;
  engine: 'duckdb-wasm' | 'json-fallback';
  rows: unknown[];
  error?: string;
};

export class TerritorialAnalytics {
  private worker?: Worker;
  private pending = new Map<string, { resolve: (value: AnalyticsResponse) => void; timer: ReturnType<typeof setTimeout> }>();

  async query(input: Omit<AnalyticsRequest, 'id'>): Promise<AnalyticsResponse> {
    if (!this.worker) {
      this.worker = new Worker(new URL('../../workers/analytics-v4.worker.ts', import.meta.url), { type: 'module' });
      this.worker.onmessage = (event: MessageEvent<AnalyticsResponse>) => {
        const pending = this.pending.get(event.data.id);
        if (!pending) return;
        clearTimeout(pending.timer);
        this.pending.delete(event.data.id);
        pending.resolve(event.data);
      };
    }
    const request = { ...input, id: crypto.randomUUID() };
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        this.pending.delete(request.id);
        resolve({ id: request.id, ok: false, engine: 'json-fallback', rows: [], error: 'La consulta excedió el tiempo permitido.' });
      }, input.timeoutMs ?? 15_000);
      this.pending.set(request.id, { resolve, timer });
      this.worker?.postMessage(request);
    });
  }

  cancelAll() {
    this.worker?.terminate();
    this.worker = undefined;
    for (const [id, pending] of this.pending) {
      clearTimeout(pending.timer);
      pending.resolve({ id, ok: false, engine: 'json-fallback', rows: [], error: 'Consulta cancelada.' });
    }
    this.pending.clear();
  }
}
