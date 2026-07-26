import { capacityConsequences } from './capacity';
import { competenceConsequences } from './competences';
import { financeConsequences } from './finance';
import { governanceConsequences } from './governance';
import { legalConsequences } from './legal';
import { representationConsequences } from './representation';
import { serviceDeliveryConsequences } from './service-delivery';
import { transitionConsequences } from './transition';
import type { Consequence, ConsequenceDimension, ConsequenceInput } from './types';

export const calculateConsequences = (input: ConsequenceInput): Consequence[] => [
  ...legalConsequences(input), ...governanceConsequences(input), ...competenceConsequences(input),
  ...financeConsequences(input), ...representationConsequences(input), ...capacityConsequences(input),
  ...serviceDeliveryConsequences(input), ...transitionConsequences(input),
  { dimension:'continuidad territorial', kind: input.contiguous === false ? 'risk' : 'conditional', before:'Geometría oficial de integrantes', decision:input.operation, after:input.contiguous == null ? 'No evaluada' : input.contiguous ? 'Conectada por frontera compartida' : 'Discontinua', explanation:'La continuidad terrestre se calcula por topología; los corredores funcionales deben declararse por separado.' },
  { dimension:'enfoque étnico', kind:'requirement', before:'Condiciones territoriales por verificar', decision:input.operation, after:'Análisis específico requerido', explanation:'La selección territorial no determina por sí sola afectación ni procedencia de consulta previa.' },
  { dimension:'consulta previa potencial', kind:'uncertainty', before:'No determinada', decision:input.operation, after:'Sujeta a análisis de afectación directa', explanation:'No se presume ni descarta automáticamente.' },
];

type ScenarioLike = {
  levels: Array<{ id: string; name: string }>;
  units: Array<{ id: string; levelId: string; state: string }>;
  governments: unknown[];
  competences: unknown[];
  finances: unknown[];
  planning: unknown[];
  assumptions: Array<{ text: string }>;
  risks: Array<{ text: string }>;
};

export function calculateScenarioDiff(
  before: ScenarioLike,
  operation: { kind: string; summary: string; payload: Record<string, unknown> },
  after: ScenarioLike,
  context: { figure?: string; contiguous?: boolean | null; population?: number | null; capacity?: number | null; legalPath?: string } = {},
): Consequence[] {
  const figure = context.figure ?? String(operation.payload.figure ?? operation.kind);
  const base = calculateConsequences({
    operation: `${operation.kind}: ${figure}`,
    contiguous: context.contiguous,
  });
  const delta = (label: ConsequenceDimension, previous: number, next: number): Consequence => ({
    dimension: label,
    kind: 'direct',
    before: String(previous),
    decision: operation.kind,
    after: String(next),
    explanation: previous === next ? 'La operación no cambia esta dimensión.' : `Cambio estructurado: ${next - previous > 0 ? '+' : ''}${next - previous}.`,
  });
  return [
    ...base,
    delta('unidades', before.units.length, after.units.length),
    delta('niveles', before.levels.length, after.levels.length),
    delta('autoridades y forma de selección', before.governments.length, after.governments.length),
    delta('competencias y roles', before.competences.length, after.competences.length),
    delta('financiación', before.finances.length, after.finances.length),
    delta('planeación y control', before.planning.length, after.planning.length),
    {
      dimension: 'población y capacidad',
      kind: context.population == null || context.capacity == null ? 'missing-data' : 'conditional',
      before: 'Datos observados del escenario base',
      decision: operation.kind,
      after: context.population == null || context.capacity == null ? 'No disponible' : `Población ${context.population}; capacidad ${context.capacity}`,
      explanation: 'No se infieren población, capacidad ni desempeño de una descripción textual.',
    },
    {
      dimension: 'ruta jurídica y transición',
      kind: context.legalPath ? 'requirement' : 'missing-data',
      before: 'Régimen vigente',
      decision: figure,
      after: context.legalPath ?? 'Ruta jurídica por definir',
      explanation: `Supuestos: ${after.assumptions.length}; riesgos: ${after.risks.length}.`,
    },
  ];
}
export type { Consequence, ConsequenceInput } from './types';

