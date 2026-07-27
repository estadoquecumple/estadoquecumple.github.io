import * as duckdb from '@duckdb/duckdb-wasm';
import duckdbWasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import duckdbWorker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import type { AnalyticsRequest, AnalyticsResponse } from '../data/territorial/analytics-v4';

let database: duckdb.AsyncDuckDB | undefined;

async function db() {
  if (database) return database;
  const worker = new Worker(duckdbWorker);
  database = new duckdb.AsyncDuckDB(new duckdb.ConsoleLogger(duckdb.LogLevel.WARNING), worker);
  await database.instantiate(duckdbWasm);
  await database.open({ path: ':memory:', query: { castTimestampToDate: true } });
  return database;
}

async function fallback(request: AnalyticsRequest, error: unknown): Promise<AnalyticsResponse> {
  try {
    const response = await fetch(request.fallbackUrl);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const rows = await response.json();
    return {
      id: request.id,
      ok: true,
      engine: 'json-fallback',
      rows: Array.isArray(rows) ? rows : rows.records ?? [],
      error: error instanceof Error ? error.message : String(error),
    };
  } catch (fallbackError) {
    return {
      id: request.id,
      ok: false,
      engine: 'json-fallback',
      rows: [],
      error: `DuckDB: ${String(error)}; fallback: ${String(fallbackError)}`,
    };
  }
}

self.onmessage = async (event: MessageEvent<AnalyticsRequest>) => {
  const request = event.data;
  try {
    const head = await fetch(request.parquetUrl, { method: 'HEAD' });
    const bytes = Number(head.headers.get('content-length') ?? 0);
    if (bytes && bytes > (request.maxBytes ?? 25_000_000)) throw new Error(`Parquet de ${bytes} bytes excede el límite.`);
    const engine = await db();
    await engine.registerFileURL('territorial.parquet', request.parquetUrl, duckdb.DuckDBDataProtocol.HTTP, false);
    const connection = await engine.connect();
    try {
      const table = await connection.query(request.sql);
      const rows = table.toArray().map((row) => row.toJSON());
      self.postMessage({ id: request.id, ok: true, engine: 'duckdb-wasm', rows } satisfies AnalyticsResponse);
    } finally {
      await connection.close();
    }
  } catch (error) {
    self.postMessage(await fallback(request, error));
  }
};
