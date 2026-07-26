import type { Consequence, ConsequenceInput } from './types';
export const legalConsequences = (input: ConsequenceInput): Consequence[] => {
  const constitutional = /suprimir|federal|legislatura|soberanía/i.test(input.operation);
  return [{
    dimension:'ruta normativa',
    kind:'requirement',
    before:'Ordenamiento unitario vigente',
    decision:input.operation,
    after:constitutional ? 'Rediseño constitucional hipotético' : 'Figura sujeta a verificación jurídica concreta',
    explanation:constitutional ? 'La operación altera elementos constitucionales y no corresponde a una figura vigente.' : 'La ruta depende de naturaleza, cobertura, competencias y gobierno.',
    source:'Constitución Política, arts. 1 y 286–325',
  }];
};

