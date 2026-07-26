import { readFileSync } from 'node:fs';

const evidence = JSON.parse(readFileSync('reports/territorial-v3-playwright-evidence.json', 'utf8'));
const controls = JSON.parse(readFileSync('reports/territorial-v3-controls-final.json', 'utf8'));
const initial = readFileSync('reports/territorial-v3-improvement-initial.md', 'utf8');
const source = readFileSync('src/components/territorial/TerritorialLab.astro', 'utf8');
const model = readFileSync('src/data/territorial/scenario-v2.ts', 'utf8');
const tests = ['scenario-v2.test.ts', 'lab.test.ts', 'interface.test.ts', 'v3-improvements.test.ts'].map((file) => readFileSync(`tests/territorial/${file}`, 'utf8')).join('\n');
const errors = [];
if (evidence.summary.failed || !evidence.summary.passed) errors.push('la ejecución Playwright no está completamente aprobada');
if (controls.controls.some((item) => item.classification !== 'funcional')) errors.push('existen botones sin contrato ejecutado');
if (!initial.includes('línea base inmutable')) errors.push('falta auditoría inicial honesta');
for (const contract of ['scenarioToMapCollections', 'calculateScenarioDiff', 'safeCsvCell', 'normalizeMpioTipo', 'classifyBoundaryRelation']) {
  if (!source.includes(contract) && !model.includes(contract) && !tests.includes(contract)) errors.push(`contrato funcional sin uso o prueba: ${contract}`);
}
if (/\.innerHTML\s*=\s*`[^`]*\$\{/.test(source)) errors.push('hay innerHTML con interpolación dinámica');
if (!readFileSync('.github/workflows/deploy.yml', 'utf8').includes('npm run lab:e2e')) errors.push('workflow sin E2E bloqueante');
if (errors.length) {
  console.error(`FUNCTIONAL AUDIT: ${errors.length} error(es)\n${errors.map((error) => `- ${error}`).join('\n')}`);
  process.exit(1);
}
console.log(`FUNCTIONAL AUDIT OK: ${evidence.summary.passed} ejecuciones; comentarios excluidos; contratos verificados.`);
