import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const server = spawn(process.execPath, ['node_modules/astro/astro.js', 'preview', '--host', '127.0.0.1', '--port', '4321'], { stdio: ['ignore', 'pipe', 'pipe'] });
let serverOutput = '';
server.stdout.on('data', (chunk) => serverOutput += chunk);
server.stderr.on('data', (chunk) => serverOutput += chunk);
const deadline = Date.now() + 120_000;
while (Date.now() < deadline) {
  try { const response = await fetch('http://127.0.0.1:4321/observatorio/laboratorio-territorial/'); if (response.ok) break; } catch {}
  await new Promise((resolve) => setTimeout(resolve, 250));
}
if (Date.now() >= deadline) {
  server.kill();
  console.error(`E2E SERVER ERROR\n${serverOutput}`);
  process.exit(1);
}

const runner = spawn(process.execPath, ['node_modules/@playwright/test/cli.js', 'test', '--reporter=json'], { stdio: ['ignore', 'pipe', 'inherit'] });
let output = '';
runner.stdout.on('data', (chunk) => output += chunk);
const code = await new Promise((resolve) => runner.on('exit', (value) => resolve(value ?? 1)));
server.kill('SIGTERM');
await new Promise((resolve) => {
  const timeout = setTimeout(resolve, 2000);
  server.once('exit', () => { clearTimeout(timeout); resolve(); });
});
if (code !== 0) {
  try {
    const report = JSON.parse(output);
    for (const error of report.errors ?? []) console.error(error.message ?? error);
    const failures = [];
    const collect = (suite) => {
      for (const spec of suite.specs ?? []) for (const test of spec.tests ?? []) for (const result of test.results ?? []) {
        if (result.status !== 'passed' && result.status !== 'skipped') failures.push(`${test.projectName} · ${spec.title}\n${result.error?.message ?? result.status}`);
      }
      for (const child of suite.suites ?? []) collect(child);
    };
    for (const suite of report.suites ?? []) collect(suite);
    console.error(failures.join('\n\n'));
  } catch { console.error(output); }
  process.exit(code);
}

const report = JSON.parse(output);
const executions = [];
const visit = (suite, file = suite.file) => {
  for (const spec of suite.specs ?? []) for (const test of spec.tests ?? []) {
    const result = test.results?.at(-1);
    executions.push({ file, title: spec.title, project: test.projectName, status: result?.status, durationMs: result?.duration ?? 0 });
  }
  for (const child of suite.suites ?? []) visit(child, child.file ?? file);
};
for (const suite of report.suites ?? []) visit(suite);
const evidence = {
  generatedAt: '2026-07-26',
  source: 'Playwright JSON reporter; only completed browser interactions are evidence.',
  summary: {
    total: executions.length,
    passed: executions.filter((item) => item.status === 'passed').length,
    failed: executions.filter((item) => item.status !== 'passed').length,
  },
  executions,
};
writeFileSync('reports/territorial-v3-playwright-evidence.json', `${JSON.stringify(evidence, null, 2)}\n`);
console.log(`LAB E2E OK: ${evidence.summary.passed} ejecuciones Playwright aprobadas; evidencia actualizada.`);
