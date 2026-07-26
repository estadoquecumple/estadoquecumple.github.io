import { normalizeSearch } from './selection-v3';

export type OfficialMetric = {
  id: string;
  label: string;
  value: number | null;
  unit: string;
  kind: 'observed' | 'calculated' | 'unavailable';
  coverage: string;
  source: string;
  warning?: string;
};

type GovernmentRecord = { code: string; entityCount: number };
type SgrRecord = { territoryLabel: string; projectCount: number };

export function metricsForSelection(
  selection: Array<{ code: string; name: string; level: 'department' | 'municipality' }>,
  government: GovernmentRecord[],
  sgr: SgrRecord[],
  secopRecords: Array<{ kind: string; recordCount: number | null }>,
): OfficialMetric[] {
  const localCodes = new Set(selection.filter((item) => item.level === 'municipality').map((item) => item.code));
  const entityRows = government.filter((item) => localCodes.has(item.code));
  const departments = selection.filter((item) => item.level === 'department');
  const sgrRows = departments.flatMap((department) => {
    const name = normalizeSearch(department.name.replace('Bogotá, D.C.', 'Bogota D.C.').replace('Valle del Cauca', 'Valle'));
    return sgr.filter((item) => normalizeSearch(item.territoryLabel) === name);
  });
  return [
    {
      id: 'government-entities',
      label: 'Entidades públicas con sede reportada',
      value: localCodes.size && entityRows.length === localCodes.size ? entityRows.reduce((sum, item) => sum + item.entityCount, 0) : null,
      unit: 'entidades',
      kind: localCodes.size && entityRows.length === localCodes.size ? 'calculated' : 'unavailable',
      coverage: `${entityRows.length}/${localCodes.size || 0} unidades locales`,
      source: 'Función Pública · Directorio SIGEP georreferenciado',
      warning: 'La sede reportada no mide planta, capacidad ni cobertura del servicio.',
    },
    {
      id: 'sgr-project-sample',
      label: 'Proyectos SGR en muestra oficial',
      value: departments.length && sgrRows.length === departments.length ? sgrRows.reduce((sum, item) => sum + item.projectCount, 0) : null,
      unit: 'proyectos en muestra',
      kind: departments.length && sgrRows.length === departments.length ? 'calculated' : 'unavailable',
      coverage: `${sgrRows.length}/${departments.length || 0} departamentos`,
      source: 'DNP · Sistema General de Regalías',
      warning: 'Muestra API de hasta 5.000 filas: no representa el total nacional.',
    },
    {
      id: 'secop-system',
      label: 'Cobertura técnica SECOP II',
      value: secopRecords.every((item) => typeof item.recordCount === 'number') ? secopRecords.reduce((sum, item) => sum + (item.recordCount ?? 0), 0) : null,
      unit: 'registros en 4 conjuntos nacionales',
      kind: secopRecords.every((item) => typeof item.recordCount === 'number') ? 'calculated' : 'unavailable',
      coverage: `${secopRecords.filter((item) => typeof item.recordCount === 'number').length}/${secopRecords.length} conjuntos`,
      source: 'Colombia Compra Eficiente · SECOP II',
      warning: 'Cobertura del sistema, no contratación atribuible a la selección.',
    },
  ];
}
