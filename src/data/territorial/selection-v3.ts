export type TerritorialLevel = 'department' | 'municipality' | 'district' | 'locality' | 'commune' | 'corregimiento' | 'custom';
export type SelectionMethod = 'click' | 'search' | 'table' | 'department' | 'neighbours' | 'contiguous' | 'rectangle' | 'polygon' | 'filter' | 'example';

export interface TerritorialSelectionState {
  mode: 'raices' | 'savia' | 'semillas';
  level: TerritorialLevel;
  selectedIds: string[];
  primaryId: string | null;
  loadedDepartmentCodes: string[];
  selectionMethod: SelectionMethod;
  universe: string;
}

export const initialSelectionState = (): TerritorialSelectionState => ({
  mode: 'raices',
  level: 'department',
  selectedIds: [],
  primaryId: null,
  loadedDepartmentCodes: [],
  selectionMethod: 'click',
  universe: '33 departamentos y Distrito Capital',
});

export const normalizeSearch = (value: string) =>
  value.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLocaleLowerCase('es').trim();

export function connectedSelection(
  topology: Record<string, { neighbours: string[] }>,
  seeds: string[],
  rings: number,
) {
  const included = new Set(seeds);
  const reasons = new Map(seeds.map((code) => [code, 'unidad inicial']));
  let frontier = [...seeds];
  for (let ring = 1; ring <= rings; ring += 1) {
    const next: string[] = [];
    for (const code of frontier) for (const neighbour of topology[code]?.neighbours ?? []) {
      if (included.has(neighbour)) continue;
      included.add(neighbour);
      reasons.set(neighbour, `anillo ${ring}: comparte frontera con ${code}`);
      next.push(neighbour);
    }
    frontier = next;
  }
  return { ids: [...included], reasons: Object.fromEntries(reasons) };
}

