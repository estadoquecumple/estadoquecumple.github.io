import { z } from 'zod';
import { calculateConsequences } from './consequences/compare';

export const LAB_SCHEMA_VERSION = 3 as const;
export const LAB_DB_NAME = 'cams-territorial-lab';
export const LAB_STORE_NAME = 'scenarios-v3';
export const LEGACY_KEYS = ['cams-territorial-scenarios-v1', 'territorial-lab-v1', 'cams-territorial-scenarios-v2'];

export const unitStateSchema = z.enum([
  'active', 'transformed', 'absorbed', 'statistical-only', 'political-only',
  'administrative-only', 'suppressed-in-scenario',
]);
export const resultKindSchema = z.enum(['observed', 'calculated', 'assumption', 'unavailable']);
export const operationKindSchema = z.enum([
  'select', 'create-unit', 'merge-units', 'split-by-membership', 'split-by-geometry',
  'transform-unit', 'suppress-unit', 'restore-unit', 'move-membership', 'create-level',
  'remove-level', 'assign-competence', 'change-government', 'change-finance', 'change-planning',
]);

const levelSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  order: z.number().int(),
  nature: z.string(),
});
const unitSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  levelId: z.string().min(1),
  state: unitStateSchema,
  parentId: z.string().nullable(),
  memberIds: z.array(z.string()),
  officialCodes: z.array(z.string()),
  geometry: z.unknown().nullable(),
  politicalStatus: z.string(),
  administrativeStatus: z.string(),
  statisticalStatus: z.string(),
});
const membershipSchema = z.object({
  parentId: z.string(),
  childId: z.string(),
  relation: z.enum(['political', 'administrative', 'statistical', 'functional']),
});
const governmentSchema = z.object({
  unitId: z.string(),
  authority: z.string(),
  selection: z.string(),
  termYears: z.number().nonnegative(),
  reelection: z.string(),
  representativeBody: z.string(),
});
const competenceSchema = z.object({
  function: z.string(),
  levelId: z.string(),
  modality: z.enum(['exclusive', 'concurrent', 'shared', 'delegated', 'subsidiary', 'temporary']),
  role: z.enum(['regulation','financing','planning','execution','operation','maintenance','inspection','surveillance','fiscal-control','political-control','evaluation']).default('execution'),
});
const financeSchema = z.object({
  levelId: z.string(),
  instruments: z.array(z.string()),
  note: z.string(),
});
const planningSchema = z.object({
  levelId: z.string(),
  horizonYears: z.number().int().positive(),
  instruments: z.array(z.string()),
  review: z.string(),
});
const interventionSchema = z.object({
  trigger: z.string(),
  action: z.string(),
  recovery: z.string(),
});
const operationSchema = z.object({
  id: z.string(),
  kind: operationKindSchema,
  at: z.string(),
  summary: z.string(),
  payload: z.record(z.string(), z.unknown()),
});
const legalImpactSchema = z.object({
  category: z.string(),
  trigger: z.string(),
  rationale: z.string(),
  source: z.string(),
  checkedAt: z.string(),
});

export const territorialScenarioSchema = z.object({
  schemaVersion: z.literal(3),
  id: z.string().min(1),
  name: z.string().min(1),
  version: z.string(),
  status: z.enum(['draft', 'exploratory', 'published', 'archived']),
  baseScenarioId: z.string(),
  createdAt: z.string(),
  updatedAt: z.string(),
  author: z.string(),
  levels: z.array(levelSchema),
  units: z.array(unitSchema),
  memberships: z.array(membershipSchema),
  governments: z.array(governmentSchema),
  competences: z.array(competenceSchema),
  finances: z.array(financeSchema),
  planning: z.array(planningSchema),
  interventions: z.array(interventionSchema),
  assumptions: z.array(z.object({ id: z.string(), text: z.string(), uncertainty: z.string() })),
  risks: z.array(z.object({ id: z.string(), text: z.string(), severity: z.string() })),
  legalImpacts: z.array(legalImpactSchema),
  consequences: z.array(z.object({
    dimension: z.string(), kind: z.enum(['direct','conditional','risk','requirement','missing-data','uncertainty']),
    before: z.string(), decision: z.string(), after: z.string(), explanation: z.string(), source: z.string().optional(),
  })),
  transitions: z.array(z.object({ order: z.number(), text: z.string(), status: z.string() })),
  sources: z.array(z.object({ title: z.string(), url: z.string(), date: z.string() })),
  history: z.array(operationSchema),
});

export type TerritorialScenario = z.infer<typeof territorialScenarioSchema>;
export type TerritorialUnit = z.infer<typeof unitSchema>;
export type ScenarioOperation = z.infer<typeof operationSchema>;
export type ResultKind = z.infer<typeof resultKindSchema>;

const now = () => new Date().toISOString();
const uid = (prefix: string) =>
  `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;

export function createScenario(name = 'Escenario territorial sin título'): TerritorialScenario {
  const stamp = now();
  return {
    schemaVersion: LAB_SCHEMA_VERSION,
    id: uid('scenario'),
    name,
    version: '3.0.0',
    status: 'draft',
    baseScenarioId: 'current-colombia-2025',
    createdAt: stamp,
    updatedAt: stamp,
    author: 'Usuario local',
    levels: [
      { id: 'nation', name: 'Nación', order: 0, nature: 'territorial vigente' },
      { id: 'department', name: 'Departamento', order: 1, nature: 'entidad territorial vigente' },
      { id: 'municipality', name: 'Municipio', order: 2, nature: 'entidad territorial vigente' },
    ],
    units: [
      { id:'nation:CO', name:'Colombia', levelId:'nation', state:'active', parentId:null, memberIds:DEPARTMENTS.map(([code])=>`department:${code}`), officialCodes:['CO'], geometry:null, politicalStatus:'república unitaria vigente', administrativeStatus:'Nación', statisticalStatus:'oficial' },
      ...DEPARTMENTS.map(([code, name]) => ({ id:`department:${code}`, name, levelId:'department', state:'active' as const, parentId:'nation:CO', memberIds:[], officialCodes:[code], geometry:null, politicalStatus:code === '11' ? 'Distrito Capital y entidad territorial' : 'entidad territorial vigente', administrativeStatus:code === '11' ? 'Distrito Capital' : 'departamento', statisticalStatus:'oficial' })),
    ],
    memberships: [],
    governments: [],
    competences: [],
    finances: [],
    planning: [],
    interventions: [],
    assumptions: [],
    risks: [],
    legalImpacts: [],
    consequences: [],
    transitions: [],
    sources: [
      { title: 'DANE DIVIPOLA MGN 2025', url: 'https://geoportal.dane.gov.co/', date: '2025' },
      { title: 'Constitución Política de Colombia', url: 'https://www.secretariasenado.gov.co/constitucion-politica', date: 'consulta 2026-07-25' },
    ],
    history: [],
  };
}

const DEPARTMENTS = [
  ['05','Antioquia'],['08','Atlántico'],['11','Bogotá, D.C.'],['13','Bolívar'],['15','Boyacá'],['17','Caldas'],['18','Caquetá'],['19','Cauca'],['20','Cesar'],['23','Córdoba'],['25','Cundinamarca'],['27','Chocó'],['41','Huila'],['44','La Guajira'],['47','Magdalena'],['50','Meta'],['52','Nariño'],['54','Norte de Santander'],['63','Quindío'],['66','Risaralda'],['68','Santander'],['70','Sucre'],['73','Tolima'],['76','Valle del Cauca'],['81','Arauca'],['85','Casanare'],['86','Putumayo'],['88','Archipiélago de San Andrés, Providencia y Santa Catalina'],['91','Amazonas'],['94','Guainía'],['95','Guaviare'],['97','Vaupés'],['99','Vichada'],
] as const;

function operation(kind: ScenarioOperation['kind'], summary: string, payload: Record<string, unknown>): ScenarioOperation {
  return { id: uid('op'), kind, at: now(), summary, payload };
}

function commit(scenario: TerritorialScenario, op: ScenarioOperation, patch: Partial<TerritorialScenario>): TerritorialScenario {
  const next = {
    ...scenario,
    ...patch,
    updatedAt: now(),
    history: [...scenario.history, op],
  };
  next.consequences = calculateConsequences({ operation: op.summary });
  return territorialScenarioSchema.parse(next);
}

export function addUnit(scenario: TerritorialScenario, input: Partial<TerritorialUnit> & Pick<TerritorialUnit, 'name' | 'levelId'>) {
  const unit: TerritorialUnit = {
    id: input.id ?? uid('cams-unit'),
    name: input.name,
    levelId: input.levelId,
    state: input.state ?? 'active',
    parentId: input.parentId ?? null,
    memberIds: input.memberIds ?? [],
    officialCodes: input.officialCodes ?? [],
    geometry: input.geometry ?? null,
    politicalStatus: input.politicalStatus ?? 'exploratory',
    administrativeStatus: input.administrativeStatus ?? 'exploratory',
    statisticalStatus: input.statisticalStatus ?? 'derived',
  };
  return commit(scenario, operation('create-unit', `Creó ${unit.name}`, { unit }), { units: [...scenario.units, unit] });
}

export function mergeUnits(
  scenario: TerritorialScenario,
  ids: string[],
  name: string,
  levelId: string,
  disposition: 'political' | 'administrative' | 'absorbed' | 'statistical',
) {
  if (ids.length < 2) throw new Error('Seleccione al menos dos unidades para unir.');
  const members = scenario.units.filter((unit) => ids.includes(unit.id));
  if (members.length !== ids.length) throw new Error('Una o más unidades seleccionadas no existen.');
  const merged: TerritorialUnit = {
    id: uid('cams-merged'), name, levelId, state: 'active', parentId: null,
    memberIds: ids, officialCodes: members.flatMap((unit) => unit.officialCodes),
    geometry: null, politicalStatus: disposition === 'political' ? 'members-retained' : 'exploratory',
    administrativeStatus: disposition, statisticalStatus: 'derived',
  };
  const nextUnits = scenario.units.map((unit) => ids.includes(unit.id) && disposition === 'absorbed'
    ? { ...unit, state: 'absorbed' as const }
    : unit);
  return commit(
    scenario,
    operation('merge-units', `Unió ${members.map((unit) => unit.name).join(', ')} en ${name}`, { ids, merged, disposition }),
    {
      units: [...nextUnits, merged],
      memberships: [
        ...scenario.memberships,
        ...ids.map((childId) => ({ parentId: merged.id, childId, relation: disposition === 'statistical' ? 'statistical' as const : 'administrative' as const })),
      ],
    },
  );
}

export function splitByMembership(scenario: TerritorialScenario, parentId: string, groups: Array<{ name: string; memberIds: string[] }>) {
  if (groups.length < 2 || groups.some((group) => !group.memberIds.length)) throw new Error('La división requiere al menos dos grupos no vacíos.');
  const seen = groups.flatMap((group) => group.memberIds);
  if (new Set(seen).size !== seen.length) throw new Error('Una unidad no puede pertenecer a dos grupos de la misma división.');
  let units = [...scenario.units];
  const created: TerritorialUnit[] = groups.map((group) => ({
    id: uid('cams-split'), name: group.name, levelId: scenario.units.find((unit) => unit.id === parentId)?.levelId ?? 'department',
    state: 'active', parentId: null, memberIds: group.memberIds,
    officialCodes: units.filter((unit) => group.memberIds.includes(unit.id)).flatMap((unit) => unit.officialCodes),
    geometry: null, politicalStatus: 'exploratory', administrativeStatus: 'exploratory', statisticalStatus: 'derived',
  }));
  units = units.map((unit) => unit.id === parentId ? { ...unit, state: 'transformed' as const } : unit).concat(created);
  return commit(scenario, operation('split-by-membership', `Dividió ${parentId} en ${groups.length} unidades`, { parentId, groups, created }), {
    units,
    memberships: [...scenario.memberships, ...created.flatMap((unit) => unit.memberIds.map((childId) => ({ parentId: unit.id, childId, relation: 'administrative' as const })))],
  });
}

export function splitByGeometry(scenario: TerritorialScenario, unitId: string, geometry: unknown, intersectedIds: string[]) {
  const assumption = {
    id: uid('assumption'),
    text: 'División geométrica experimental: población, finanzas, SGR y SECOP quedan sin estimación por falta de datos submunicipales.',
    uncertainty: 'alta',
  };
  return commit(scenario, operation('split-by-geometry', `Registró corte geométrico experimental sobre ${unitId}`, {
    unitId, geometry, intersectedIds, experimental: true,
    population: { value: null, kind: 'unavailable' },
    finance: { value: null, kind: 'unavailable' },
  }), { assumptions: [...scenario.assumptions, assumption] });
}

export function transformUnit(scenario: TerritorialScenario, id: string, state: TerritorialUnit['state'], nature: string) {
  const units = scenario.units.map((unit) => unit.id === id
    ? { ...unit, state, administrativeStatus: nature }
    : unit);
  if (!units.some((unit) => unit.id === id)) throw new Error('Unidad no encontrada.');
  return commit(scenario, operation('transform-unit', `Transformó ${id} como ${nature}`, { id, state, nature }), { units });
}

export function suppressUnit(scenario: TerritorialScenario, id: string) {
  return transformWithKind(scenario, id, 'suppressed-in-scenario', 'suppress-unit', `Suprimió ${id} dentro del escenario`);
}
export function restoreUnit(scenario: TerritorialScenario, id: string) {
  return transformWithKind(scenario, id, 'active', 'restore-unit', `Restauró ${id}`);
}
function transformWithKind(scenario: TerritorialScenario, id: string, state: TerritorialUnit['state'], kind: 'suppress-unit' | 'restore-unit', summary: string) {
  if (!scenario.units.some((unit) => unit.id === id)) throw new Error('Unidad no encontrada.');
  return commit(scenario, operation(kind, summary, { id, state }), {
    units: scenario.units.map((unit) => unit.id === id ? { ...unit, state } : unit),
  });
}

export function createLevel(scenario: TerritorialScenario, name: string, order: number, nature: string) {
  const level = { id: uid('level'), name, order, nature };
  return commit(scenario, operation('create-level', `Creó el nivel ${name}`, { level }), { levels: [...scenario.levels, level].sort((a, b) => a.order - b.order) });
}

export function assignCompetence(scenario: TerritorialScenario, publicFunction: string, levelId: string, modality: z.infer<typeof competenceSchema>['modality'], role: z.infer<typeof competenceSchema>['role'] = 'execution') {
  const competences = scenario.competences.filter((item) => !(item.function === publicFunction && item.role === role));
  competences.push({ function: publicFunction, levelId, modality, role });
  return commit(scenario, operation('assign-competence', `Asignó ${role} de ${publicFunction} a ${levelId}`, { publicFunction, levelId, modality, role }), { competences });
}

export function changeGovernment(scenario: TerritorialScenario, government: z.infer<typeof governmentSchema>) {
  const governments = scenario.governments.filter((item) => item.unitId !== government.unitId).concat(government);
  return commit(scenario, operation('change-government', `Cambió el gobierno de ${government.unitId}`, { government }), { governments });
}

export function changeFinance(scenario: TerritorialScenario, rule: z.infer<typeof financeSchema>) {
  const finances = scenario.finances.filter((item) => item.levelId !== rule.levelId).concat(rule);
  return commit(scenario, operation('change-finance', `Cambió financiación de ${rule.levelId}`, { rule }), { finances });
}

export function changePlanning(scenario: TerritorialScenario, rule: z.infer<typeof planningSchema>) {
  const planning = scenario.planning.filter((item) => item.levelId !== rule.levelId).concat(rule);
  return commit(scenario, operation('change-planning', `Cambió planeación de ${rule.levelId}`, { rule }), { planning });
}

export function classifyLegalImpact(scenario: TerritorialScenario) {
  const impacts: TerritorialScenario['legalImpacts'] = [];
  const add = (category: string, trigger: string, rationale: string, source: string) =>
    impacts.push({ category, trigger, rationale, source, checkedAt: '2026-07-25' });
  if (scenario.history.some((item) => item.kind === 'merge-units')) add('posible mediante convenio o asociación', 'asociación entre entidades', 'La cooperación puede apoyarse en esquemas asociativos vigentes, sujeto al diseño concreto.', 'Constitución, arts. 286–321; Ley 1454 de 2011');
  if (scenario.levels.some((level) => !['nation', 'department', 'municipality'].includes(level.id))) add('requiere revisión jurídica especializada', 'nuevo nivel territorial', 'La naturaleza y autonomía propuesta determinan si basta una figura administrativa o se altera la organización territorial.', 'Constitución, Título XI');
  if (scenario.units.some((unit) => unit.state === 'suppressed-in-scenario' && unit.levelId === 'department')) add('probablemente requiere reforma constitucional', 'supresión del nivel departamental', 'El departamento integra la organización territorial constitucional vigente.', 'Constitución, arts. 286 y 297–310');
  if (scenario.governments.some((item) => item.selection !== 'elección directa')) add('probablemente requiere reforma constitucional', 'cambio en elección de autoridad territorial', 'La elección popular de gobernadores y alcaldes tiene reconocimiento constitucional.', 'Constitución, arts. 303 y 314');
  if (!impacts.length) add('compatible con figura vigente', 'sin alteración estructural detectada', 'No se detectó una operación que por sí sola altere la arquitectura constitucional.', 'Constitución y Ley 1454 de 2011');
  return { ...scenario, legalImpacts: impacts };
}

export function aggregateCompleteUnits(values: Array<{ population?: number | null; area?: number | null }>) {
  const population = values.every((item) => typeof item.population === 'number')
    ? { value: values.reduce((sum, item) => sum + (item.population ?? 0), 0), kind: 'calculated' as const }
    : { value: null, kind: 'unavailable' as const };
  const area = values.every((item) => typeof item.area === 'number')
    ? { value: values.reduce((sum, item) => sum + (item.area ?? 0), 0), kind: 'calculated' as const }
    : { value: null, kind: 'unavailable' as const };
  return { population, area, units: { value: values.length, kind: 'calculated' as const } };
}

export function duplicateScenario(scenario: TerritorialScenario, name = `${scenario.name} — copia`) {
  const stamp = now();
  return territorialScenarioSchema.parse({ ...structuredClone(scenario), id: uid('scenario'), name, status: 'draft', createdAt: stamp, updatedAt: stamp, history: [] });
}

export function importScenario(input: unknown): TerritorialScenario {
  const parsed = territorialScenarioSchema.safeParse(input);
  if (!parsed.success) throw new Error(`Escenario incompatible: ${parsed.error.issues.map((issue) => `${issue.path.join('.')}: ${issue.message}`).join('; ')}`);
  return parsed.data;
}

export function exportScenario(scenario: TerritorialScenario) {
  return JSON.stringify(territorialScenarioSchema.parse(scenario), null, 2);
}

export function migrateLocalState(storage: Pick<Storage, 'getItem' | 'removeItem' | 'setItem'>) {
  let migratedPreferences = false;
  let discardedScenarios = false;
  for (const key of LEGACY_KEYS) {
    const value = storage.getItem(key);
    if (!value) continue;
    try {
      const parsed = JSON.parse(value);
      if (parsed && typeof parsed === 'object' && typeof parsed.mode === 'string') {
        storage.setItem('cams-territorial-preferences-v3', JSON.stringify({ mode: parsed.mode }));
        migratedPreferences = true;
      }
    } catch {
      // Los datos incompatibles se descartan sin ejecutarlos.
    }
    storage.removeItem(key);
    discardedScenarios = true;
  }
  return { migratedPreferences, discardedScenarios };
}

export class ScenarioTimeline {
  private past: TerritorialScenario[] = [];
  private future: TerritorialScenario[] = [];
  constructor(public current: TerritorialScenario) {}
  apply(next: TerritorialScenario) {
    this.past.push(this.current);
    this.current = next;
    this.future = [];
    return this.current;
  }
  undo() {
    const previous = this.past.pop();
    if (!previous) return this.current;
    this.future.push(this.current);
    this.current = previous;
    return this.current;
  }
  redo() {
    const next = this.future.pop();
    if (!next) return this.current;
    this.past.push(this.current);
    this.current = next;
    return this.current;
  }
}
