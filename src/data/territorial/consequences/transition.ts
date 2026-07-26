import type { Consequence, ConsequenceInput } from './types';
export const transitionConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'transición', kind:'requirement', before:'Instituciones, personal, contratos y archivos vigentes', decision:input.operation, after:'Plan de transición requerido', explanation:'Debe definir hitos, responsables, continuidad de servicios, activos, pasivos, contratos, personal y control.' },
  { dimension:'costos de transición', kind:'missing-data', before:'Sin línea base monetaria', decision:input.operation, after:'No cuantificados', explanation:'No se afirma ahorro ni costo exacto sin inventario y metodología verificable.' },
];

