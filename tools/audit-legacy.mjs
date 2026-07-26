import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const failures = [];
const read = (path) => readFileSync(join(root, path), 'utf8');
const auditPath = 'reports/legacy-audit.json';
if (!existsSync(join(root, auditPath))) failures.push('Falta reports/legacy-audit.json');
else {
  const audit = JSON.parse(read(auditPath));
  if (!Array.isArray(audit.items) || audit.items.length < 10) failures.push('La auditoría de legado no tiene inventario suficiente.');
  for (const [index, item] of audit.items.entries()) {
    for (const field of ['file', 'reference', 'category', 'decision', 'justification']) if (!item[field]) failures.push(`legacy-audit item ${index}: falta ${field}`);
    if (!['conservar', 'migrar', 'reemplazar', 'eliminar'].includes(item.decision)) failures.push(`legacy-audit item ${index}: decisión inválida`);
  }
}
const publicFiles = [
  'src/pages/observatorio/index.astro',
  'src/pages/observatorio/laboratorio-territorial/index.astro',
  'src/pages/estado-que-cumple/aplicaciones/index.astro',
  'src/data/site.ts',
];
for (const file of publicFiles) {
  const content = read(file);
  if (/V1|en desarrollo|prototipo/i.test(content)) failures.push(`${file}: conserva una entrada pública anterior`);
  if (content.includes('camscarlosmartinez.github.io')) failures.push(`${file}: conserva dominio anterior`);
}
const map = read('src/components/territorial/TerritoryMap.astro');
if (/import\s+\*\s+as\s+maplibregl/.test(map)) failures.push('TerritoryMap: importación namespace anterior');
if (/municipalities\/11\.geojson/.test(map)) failures.push('TerritoryMap: código fijo de Bogotá');
const workspaces = ['RootsWorkspace.astro', 'SaviaWorkspace.astro', 'SeedsWorkspace.astro']
  .map((name) => read(`src/components/territorial/${name}`)).join('\n');
const lab = read('src/components/territorial/TerritorialLab.astro');
for (const contract of ['data-workspace="raices"', 'data-workspace="savia"', 'data-workspace="semillas"', 'IndexedDB', 'data-export-json']) {
  if (!(workspaces + lab).includes(contract)) failures.push(`V2: falta contrato ${contract}`);
}
if (failures.length) {
  console.error(`LEGACY AUDIT FAIL (${failures.length})\n- ${failures.join('\n- ')}`);
  process.exit(1);
}
console.log(`LEGACY AUDIT OK: ${publicFiles.length} entradas públicas, dominio, importación MapLibre, DIVIPOLA dinámico y contrato V2 verificados.`);
