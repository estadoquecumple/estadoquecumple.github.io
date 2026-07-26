import type { Consequence, ConsequenceInput } from './types';
export const competenceConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'competencias', kind:'direct', before:input.before?.competence ?? 'Distribución vigente', decision:input.operation, after:input.after?.competence ?? 'Asignación por rol del escenario', explanation:'Deben distinguirse regulación, financiación, planeación, ejecución, operación, mantenimiento, inspección, vigilancia y controles.' },
  { dimension:'concurrencia', kind:'conditional', before:'Coordinación vigente', decision:input.operation, after:'Concurrencia según modalidad elegida', explanation:'La efectividad depende de convenios, recursos, capacidad y reglas de coordinación.' },
];

