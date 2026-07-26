import type { Consequence, ConsequenceInput } from './types';
export const capacityConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'capacidad administrativa', kind:'uncertainty', before:'Cobertura parcial o ausente', decision:input.operation, after:'No inferida automáticamente', explanation:'Una mayor escala no garantiza capacidad. Se requieren personal, procesos, información y desempeño observados.' },
  { dimension:'accesibilidad', kind:'missing-data', before:'Sin matriz nacional de tiempos de viaje conectada', decision:input.operation, after:'No evaluada', explanation:'La contigüidad geométrica no equivale a accesibilidad funcional.' },
];

