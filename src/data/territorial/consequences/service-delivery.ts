import type { Consequence, ConsequenceInput } from './types';
export const serviceDeliveryConsequences = (input: ConsequenceInput): Consequence[] => [
  { dimension:'prestación de servicios', kind:'conditional', before:'Prestadores y competencias vigentes', decision:input.operation, after:'Arreglo institucional propuesto', explanation:'El efecto depende de capacidad, financiación, contratos, regulación, transición y condiciones territoriales.' },
  { dimension:'mantenimiento', kind:'requirement', before:'Responsables vigentes', decision:input.operation, after:'Responsable y fuente deben definirse', explanation:'Crear una unidad no transfiere automáticamente activos ni obligaciones de mantenimiento.' },
];

