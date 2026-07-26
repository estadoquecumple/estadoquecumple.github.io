const FORMULA_PREFIX = /^[=+\-@]/;

export function safeCsvCell(value: unknown): string {
  let text = String(value ?? '');
  if (FORMULA_PREFIX.test(text)) text = `'${text}`;
  return `"${text.replaceAll('"', '""')}"`;
}

export function scenarioCsv(rows: Array<Record<string, unknown>>, columns: string[]): string {
  return [
    columns.map(safeCsvCell).join(','),
    ...rows.map((row) => columns.map((column) => safeCsvCell(row[column])).join(',')),
  ].join('\n');
}

export function safeExternalUrl(value: string): string | null {
  try {
    const url = new URL(value, 'https://example.invalid');
    return ['http:', 'https:'].includes(url.protocol) ? value : null;
  } catch {
    return null;
  }
}
