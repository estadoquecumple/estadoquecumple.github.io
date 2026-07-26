import type { Consequence, ConsequenceInput } from './types';
export const representationConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'representación', kind:'conditional', before:input.before?.representation ?? 'Corporaciones vigentes', decision:input.operation, after:input.after?.representation ?? 'Órgano propuesto', explanation:'La representación cambia solo si el diseño define integración, elección, circunscripción y reglas de decisión.' },
];

