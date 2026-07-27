import { existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

const local = process.platform === 'win32' ? '.venv/Scripts/python.exe' : '.venv/bin/python';
const executable = existsSync(local) ? local : (process.platform === 'win32' ? 'py' : 'python3');
const fallbackArgs = executable === 'py' ? ['-3.12'] : [];
const result = spawnSync(executable, [...fallbackArgs, ...process.argv.slice(2)], { stdio: 'inherit' });
if (result.error) {
  console.error(`No se pudo ejecutar el intérprete Python aprobado: ${result.error.message}`);
  process.exit(1);
}
process.exit(result.status ?? 1);
