import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";

const action = process.argv[2];
const allowed = new Set(["up", "down", "logs", "migrate", "seed", "health", "test", "backup", "restore-test"]);
if (!allowed.has(action)) {
  console.error(`Acción backend inválida: ${action ?? "(vacía)"}`);
  process.exit(2);
}
if (!existsSync(".env.lab")) {
  console.error("Falta .env.lab. Copie .env.lab.example y defina secretos locales.");
  process.exit(2);
}
const compose = ["compose", "--env-file", ".env.lab", "-p", "estadoquecumple-territorial-v4", "-f", "infra/containers/compose.yml"];
const commands = {
  up: [...compose, "--parallel", "1", "up", "-d", "--build", "--wait"],
  down: [...compose, "down"],
  logs: [...compose, "logs", "--tail", "200"],
  migrate: [...compose, "run", "--build", "--rm", "migrate"],
  seed: [...compose, "run", "--rm", "api", "python", "-m", "services.shared.seed"],
  health: [...compose, "run", "--rm", "--no-deps", "api", "python", "-m", "services.shared.health"],
  test: [...compose, "run", "--rm", "api", "pytest", "-p", "no:cacheprovider", "-q", "tests/backend"],
  backup: [...compose, "run", "--rm", "backup", "backup"],
  "restore-test": [...compose, "run", "--rm", "backup", "restore-test"],
};
const result = spawnSync("docker", commands[action], { stdio: "inherit", shell: false });
process.exit(result.status ?? 1);
