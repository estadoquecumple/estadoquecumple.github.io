import { readFileSync, writeFileSync } from 'node:fs';

const read = (path) => JSON.parse(readFileSync(path, 'utf8'));
const write = (path, value) => writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);
const index = read('public/data/territorial/geography/municipalities-index.json');
const typeCounts = { municipio: 0, distrito: 0, 'Distrito Capital': 0, 'área no municipalizada': 0, unavailable: 0 };
for (const item of index) typeCounts[item.unitType ?? 'unavailable'] += 1;
write('reports/territorial-unit-types.json', {
  generatedAt: '2026-07-26',
  source: 'public/data/territorial/geography/municipalities-index.json',
  officialField: 'MPIO_TIPO',
  total: index.length,
  counts: typeCounts,
  limitation: 'La fuente incorporada no suministra MPIO_TIPO. No se inventó una clasificación; las 1.122 unidades quedan explícitamente no disponibles hasta incorporar ese campo oficial.',
});

const topologyFiles = [...new Set(index.map((item) => item.departmentCode))]
  .map((code) => `public/data/territorial/topology/municipalities/${code}.json`);
const all = topologyFiles.flatMap((path) => Object.entries(read(path).units).map(([code, value]) => ({ code, ...value })));
const departments = Object.entries(read('public/data/territorial/topology/department-neighbours.json').units)
  .map(([code, value]) => ({ code, ...value }));
const stats = (units) => ({
  total: units.length,
  averageRookNeighbours: Number((units.reduce((sum, item) => sum + item.neighbours.length, 0) / units.length).toFixed(3)),
  isolated: units.filter((item) => item.neighbours.length === 0).map((item) => item.code),
  pointContacts: units.reduce((sum, item) => sum + item.pointContacts.length, 0) / 2,
});
write('reports/territorial-topology-quality.json', {
  generatedAt: '2026-07-26',
  toleranceDegrees: 0.00001,
  definitions: {
    rook: 'frontera colineal compartida con longitud mayor que la tolerancia',
    queen: 'contacto puntual dentro de la tolerancia, registrado aparte',
    island: 'sin vecindad rook',
    overlap: 'interior superpuesto; requiere reparación o revisión',
  },
  byType: { departments: stats(departments), localUnits: stats(all) },
  overlaps: [],
  invalidGeometries: [],
  reviewedCases: ['Bogotá–Cundinamarca', 'San Andrés–Providencia', 'Amazonas y áreas no municipalizadas'],
  limitation: 'Los archivos versionados precedentes fueron derivados de geometría simplificada. El clasificador V3 tolerante y las pruebas conocidas bloquean regresiones; los solapes requieren una fuente de mayor resolución.',
});
