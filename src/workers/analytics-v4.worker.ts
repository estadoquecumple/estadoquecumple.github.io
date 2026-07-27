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
    const response = await fetch(request.parquetUrl);
    if (!response.ok) throw new Error(`Parquet HTTP ${response.status}`);
    const bytes = Number(response.headers.get('content-length') ?? 0);
    if (bytes && bytes > (request.maxBytes ?? 25_000_000)) throw new Error(`Parquet de ${bytes} bytes excede el límite.`);
    const parquet = new Uint8Array(await response.arrayBuffer());
    if (parquet.byteLength > (request.maxBytes ?? 25_000_000)) throw new Error(`Parquet de ${parquet.byteLength} bytes excede el límite.`);
    const engine = await db();
    await engine.dropFile('territorial.parquet').catch(() => undefined);
    await engine.registerFileBuffer('territorial.parquet', parquet);
    const connection = await engine.connect();
    try {
      const extensionRepository = new URL('/assets/duckdb', self.location.origin).href.replace(/\/$/, '');
      await connection.query(`SET custom_extension_repository='${extensionRepository}'`);
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
