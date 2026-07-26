import type { Consequence, ConsequenceInput } from './types';
export const financeConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'financiación', kind:'direct', before:input.before?.finance ?? 'Fuentes vigentes', decision:input.operation, after:input.after?.finance ?? 'Instrumentos seleccionados', explanation:'La selección identifica instrumentos; no estima recaudo, ahorro ni suficiencia.' },
  { dimension:'datos faltantes', kind:'missing-data', before:'Sin proyección fiscal granular', decision:input.operation, after:'Sigue sin estimación monetaria', explanation:'Se requieren bases fiscales, reglas de distribución, vigencia y supuestos explícitos.' },
];

