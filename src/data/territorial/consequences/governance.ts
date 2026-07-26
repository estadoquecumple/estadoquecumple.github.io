import type { Consequence, ConsequenceInput } from './types';
export const governanceConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'autoridades', kind:'direct', before:input.before?.authority ?? 'Autoridad vigente según el tipo de entidad', decision:input.operation, after:input.after?.authority ?? 'Autoridad configurada en el escenario', explanation:'El escenario cambia la regla de autoridad; no prueba por sí mismo una mejora de gestión.' },
  { dimension:'elección o nombramiento', kind:'requirement', before:input.before?.selection ?? 'Régimen vigente', decision:input.operation, after:input.after?.selection ?? 'Procedimiento configurado', explanation:'Sustituir la elección popular de alcaldes o gobernadores probablemente exige reforma constitucional.', source:'Constitución Política, arts. 303 y 314' },
  { dimension:'riesgos de captura', kind:'risk', before:'Riesgo no cuantificado', decision:input.operation, after:'Debe evaluarse para el diseño concreto', explanation:'La forma de selección modifica incentivos y rendición de cuentas, pero no permite estimar una magnitud sin evidencia.' },
];

