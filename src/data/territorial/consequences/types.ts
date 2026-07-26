export type ConsequenceKind = 'direct' | 'conditional' | 'risk' | 'requirement' | 'missing-data' | 'uncertainty';
export type ConsequenceDimension =
  | 'naturaleza jurídica'|'ruta normativa'|'autonomía'|'autoridades'|'elección o nombramiento'|'representación'
  | 'corporaciones públicas'|'competencias'|'financiación'|'planeación'|'control político'|'control fiscal'
  | 'control judicial'|'coordinación'|'concurrencia'|'subsidiariedad'|'capacidad administrativa'|'escala'
  | 'proximidad'|'accesibilidad'|'continuidad territorial'|'identidad territorial'|'enfoque étnico'
  | 'consulta previa potencial'|'prestación de servicios'|'mantenimiento'|'transición'|'costos de transición'
  | 'riesgos de captura'|'datos faltantes'|'incertidumbre';
export type Consequence = {
  dimension: ConsequenceDimension;
  kind: ConsequenceKind;
  before: string;
  decision: string;
  after: string;
  explanation: string;
  source?: string;
};
export type ConsequenceInput = {
  operation: string;
  before?: Record<string,string>;
  after?: Record<string,string>;
  selectedCount?: number;
  contiguous?: boolean | null;
};

