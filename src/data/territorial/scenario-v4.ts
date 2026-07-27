import { z } from 'zod';
import type { TerritorialScenario } from './scenario-v2';

export const compilationStateSchema = z.enum([
  'draft',
  'geometrically-valid',
  'institutionally-complete',
  'fiscally-evaluated',
  'legally-classified',
  'ready-for-deliberation',
]);

const validationSchema = z.object({
  code: z.string(),
  severity: z.enum(['error', 'warning']),
  path: z.string(),
  message: z.string(),
  action: z.string(),
});

export const reproducibilityCapsuleSchema = z.object({
  schemaVersion: z.literal(4),
  runId: z.string().min(1),
  createdAt: z.string(),
  commit: z.string().min(7),
  contractVersion: z.string(),
  legalRegistryVersion: z.string(),
  datasets: z.array(z.object({ id: z.string(), version: z.string(), sha256: z.string().regex(/^[a-f0-9]{64}$/) })),
  rules: z.array(z.object({ id: z.string(), version: z.string(), sha256: z.string().regex(/^[a-f0-9]{64}$/) })),
  models: z.array(z.object({ id: z.string(), version: z.string(), sha256: z.string().regex(/^[a-f0-9]{64}$/) })),
  assumptions: z.array(z.string()),
  constraints: z.array(z.string()),
  randomSeed: z.number().int().nonnegative(),
  inputs: z.record(z.string(), z.unknown()),
  outputs: z.record(z.string(), z.unknown()),
  validations: z.array(validationSchema),
  warnings: z.array(z.string()),
  providers: z.object({ llm: z.literal('none'), embeddings: z.literal('none') }),
});

export type CompilationValidation = z.infer<typeof validationSchema>;
export type ReproducibilityCapsule = z.infer<typeof reproducibilityCapsuleSchema>;

const duplicateValues = (values: string[]) => [...new Set(values.filter((value, index) => values.indexOf(value) !== index))];

export function compileScenario(scenario: TerritorialScenario) {
  const validations: CompilationValidation[] = [];
  const error = (code: string, path: string, message: string, action: string) =>
    validations.push({ code, severity: 'error', path, message, action });
  const warning = (code: string, path: string, message: string, action: string) =>
    validations.push({ code, severity: 'warning', path, message, action });

  const ids = new Set(scenario.units.map((unit) => unit.id));
  for (const duplicate of duplicateValues(scenario.units.map((unit) => unit.id))) {
    error('duplicate-unit', 'units', `La unidad ${duplicate} está duplicada.`, 'Conserve un único ID estable.');
  }
  for (const unit of scenario.units) {
    if (unit.id !== 'nation:CO' && !unit.parentId && unit.state === 'active') {
      error('missing-parent', `units.${unit.id}.parentId`, `${unit.name} no tiene unidad superior.`, 'Asigne un padre institucional.');
    }
    if (unit.parentId && !ids.has(unit.parentId)) {
      error('unknown-parent', `units.${unit.id}.parentId`, `El padre ${unit.parentId} no existe.`, 'Corrija la referencia o cree la unidad.');
    }
    if (unit.geometry && typeof unit.geometry === 'object' && !('type' in unit.geometry)) {
      error('invalid-geometry', `units.${unit.id}.geometry`, 'La geometría no declara tipo GeoJSON.', 'Use Polygon o MultiPolygon válido.');
    }
  }
  for (const unit of scenario.units) {
    const visited = new Set<string>();
    let cursor: typeof unit | undefined = unit;
    while (cursor?.parentId) {
      if (visited.has(cursor.parentId)) {
        error('hierarchy-cycle', `units.${unit.id}.parentId`, `La jerarquía de ${unit.name} contiene un ciclo.`, 'Rompa la referencia circular.');
        break;
      }
      visited.add(cursor.parentId);
      cursor = scenario.units.find((candidate) => candidate.id === cursor?.parentId);
    }
  }

  const activeLevels = new Set(scenario.units.filter((unit) => unit.state === 'active').map((unit) => unit.levelId));
  for (const competence of scenario.competences) {
    if (!activeLevels.has(competence.levelId)) {
      error('competence-without-owner', 'competences', `${competence.function} se asignó a un nivel sin unidad activa.`, 'Asigne un nivel responsable activo.');
    }
    if (!scenario.finances.some((finance) => finance.levelId === competence.levelId && finance.instruments.length)) {
      error('responsibility-without-finance', 'finances', `${competence.function} no tiene financiación en ${competence.levelId}.`, 'Defina instrumentos financieros.');
    }
  }
  for (const government of scenario.governments) {
    if (!government.selection.trim()) error('authority-without-selection', 'governments', `${government.unitId} no define selección.`, 'Defina la forma de selección.');
    if (!government.representativeBody.trim()) error('authority-without-control', 'governments', `${government.unitId} no define órgano representativo.`, 'Defina representación y control.');
  }
  if (scenario.history.length && !scenario.legalImpacts.length) {
    error('missing-legal-path', 'legalImpacts', 'El escenario modificado no tiene clasificación jurídica.', 'Ejecute la clasificación jurídica preliminar.');
  }
  if (scenario.history.length && !scenario.transitions.length) {
    error('missing-transition', 'transitions', 'El escenario modificado no tiene ruta de transición.', 'Defina hitos, responsables y controles.');
  }
  if (!scenario.units.some((unit) => unit.geometry)) {
    warning('geometry-not-loaded', 'units', 'La compilación no pudo verificar cobertura o solapes sin geometrías.', 'Cargue las geometrías oficiales antes de deliberar.');
  }

  const errors = validations.filter((item) => item.severity === 'error');
  let state: z.infer<typeof compilationStateSchema> = 'draft';
  if (!errors.some((item) => ['duplicate-unit', 'missing-parent', 'unknown-parent', 'hierarchy-cycle', 'invalid-geometry'].includes(item.code))) state = 'geometrically-valid';
  if (!errors.some((item) => ['competence-without-owner', 'authority-without-selection', 'authority-without-control'].includes(item.code)) && state === 'geometrically-valid') state = 'institutionally-complete';
  if (!errors.some((item) => item.code === 'responsibility-without-finance') && state === 'institutionally-complete') state = 'fiscally-evaluated';
  if (!errors.some((item) => item.code === 'missing-legal-path') && state === 'fiscally-evaluated') state = 'legally-classified';
  if (!errors.length && scenario.transitions.length) state = 'ready-for-deliberation';
  return { valid: !errors.length, state, validations };
}

export function createCapsule(
  scenario: TerritorialScenario,
  provenance: Pick<ReproducibilityCapsule, 'commit' | 'contractVersion' | 'legalRegistryVersion' | 'datasets' | 'rules' | 'models'>,
  outputs: Record<string, unknown>,
  randomSeed = 0,
): ReproducibilityCapsule {
  const compilation = compileScenario(scenario);
  return reproducibilityCapsuleSchema.parse({
    schemaVersion: 4,
    runId: `run-${scenario.id}-${Date.now().toString(36)}`,
    createdAt: new Date().toISOString(),
    ...provenance,
    assumptions: scenario.assumptions.map((item) => item.text),
    constraints: scenario.risks.map((item) => item.text),
    randomSeed,
    inputs: { scenario },
    outputs,
    validations: compilation.validations,
    warnings: compilation.validations.filter((item) => item.severity === 'warning').map((item) => item.message),
    providers: { llm: 'none', embeddings: 'none' },
  });
}
