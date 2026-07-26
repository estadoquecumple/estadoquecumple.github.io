export const TERRITORIAL_UNIT_TYPES = [
  'municipio',
  'distrito',
  'Distrito Capital',
  'área no municipalizada',
] as const;

export type TerritorialUnitType = typeof TERRITORIAL_UNIT_TYPES[number];

export type TypedTerritorialIndexItem = {
  code: string;
  departmentCode: string;
  name: string;
  MPIO_TIPO: string | null;
  unitType: TerritorialUnitType | null;
};

const aliases: Record<string, TerritorialUnitType> = {
  municipio: 'municipio',
  distrito: 'distrito',
  'distrito especial': 'distrito',
  'distrito capital': 'Distrito Capital',
  'area no municipalizada': 'área no municipalizada',
  'área no municipalizada': 'área no municipalizada',
};

export function normalizeMpioTipo(value: unknown): TerritorialUnitType | null {
  if (typeof value !== 'string' || !value.trim()) return null;
  const key = value.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLocaleLowerCase('es').trim();
  return aliases[key] ?? null;
}

export function labelTerritorialUnit(item: Pick<TypedTerritorialIndexItem, 'unitType'>): string {
  return item.unitType ?? 'tipo territorial no suministrado por la fuente';
}
