import { capacityConsequences } from './capacity';
import { competenceConsequences } from './competences';
import { financeConsequences } from './finance';
import { governanceConsequences } from './governance';
import { legalConsequences } from './legal';
import { representationConsequences } from './representation';
import { serviceDeliveryConsequences } from './service-delivery';
import { transitionConsequences } from './transition';
import type { Consequence, ConsequenceInput } from './types';

export const calculateConsequences = (input: ConsequenceInput): Consequence[] => [
  ...legalConsequences(input), ...governanceConsequences(input), ...competenceConsequences(input),
  ...financeConsequences(input), ...representationConsequences(input), ...capacityConsequences(input),
  ...serviceDeliveryConsequences(input), ...transitionConsequences(input),
  { dimension:'continuidad territorial', kind: input.contiguous === false ? 'risk' : 'conditional', before:'Geometría oficial de integrantes', decision:input.operation, after:input.contiguous == null ? 'No evaluada' : input.contiguous ? 'Conectada por frontera compartida' : 'Discontinua', explanation:'La continuidad terrestre se calcula por topología; los corredores funcionales deben declararse por separado.' },
  { dimension:'enfoque étnico', kind:'requirement', before:'Condiciones territoriales por verificar', decision:input.operation, after:'Análisis específico requerido', explanation:'La selección territorial no determina por sí sola afectación ni procedencia de consulta previa.' },
  { dimension:'consulta previa potencial', kind:'uncertainty', before:'No determinada', decision:input.operation, after:'Sujeta a análisis de afectación directa', explanation:'No se presume ni descarta automáticamente.' },
];
export type { Consequence, ConsequenceInput } from './types';

