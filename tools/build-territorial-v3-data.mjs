import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

const read = (path) => JSON.parse(readFileSync(path, 'utf8'));
const write = (path, value) => {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(value, null, 2)}\n`);
};
const collection = (features) => ({ type: 'FeatureCollection', features });
const region = [-92, -20, -58, 19];
const coordinates = (geometry) => geometry?.coordinates?.flat(Infinity).filter((value) => typeof value === 'number') ?? [];
const pairs = (geometry) => {
  const values = coordinates(geometry);
  const result = [];
  for (let index = 0; index < values.length; index += 2) result.push([values[index], values[index + 1]]);
  return result;
};
const intersectsRegion = (feature) => pairs(feature.geometry).some(([x, y]) => x >= region[0] && x <= region[2] && y >= region[1] && y <= region[3]);
const contextRoot = 'public/data/territorial/context';
const sourceRoot = 'public/data/territorial/context-source';
const wantedCountries = new Set(['Colombia', 'Panama', 'Costa Rica', 'Nicaragua', 'Venezuela', 'Brazil', 'Peru', 'Ecuador']);
const countries = read(join(sourceRoot, 'countries.geojson')).features
  .filter((feature) => wantedCountries.has(feature.properties.ADMIN))
  .map((feature) => ({
    type: 'Feature',
    id: feature.properties.ADM0_A3,
    properties: { name: feature.properties.ADMIN, code: feature.properties.ADM0_A3, source: 'Natural Earth 1:110m' },
    geometry: feature.geometry,
  }));
write(join(contextRoot, 'countries-near-colombia.geojson'), collection(countries));
write(join(contextRoot, 'country-borders.geojson'), collection(countries.map((feature) => ({
  ...feature,
  id: `border-${feature.id}`,
  properties: { ...feature.properties, status: 'context-only-not-official-colombian-boundary' },
}))));
write(join(contextRoot, 'coastline.geojson'), collection(read(join(sourceRoot, 'coastline.geojson')).features.filter(intersectsRegion)));
write(join(contextRoot, 'ocean.geojson'), collection(read(join(sourceRoot, 'ocean.geojson')).features.filter(intersectsRegion)));

const places = read(join(sourceRoot, 'places.geojson')).features.filter((feature) =>
  wantedCountries.has(feature.properties.adm0name)
  && (feature.properties.adm0cap === 1 || feature.properties.capin === 'world'),
).map((feature) => ({
  type: 'Feature',
  id: feature.properties.sov_a3,
  properties: { name: feature.properties.name, country: feature.properties.adm0name, source: 'Natural Earth 1:110m' },
  geometry: feature.geometry,
}));
write(join(contextRoot, 'capital-cities.geojson'), collection(places));
write(join(contextRoot, 'geographic-labels.geojson'), collection([
  { type: 'Feature', id: 'caribbean-sea', properties: { name: 'Mar Caribe', kind: 'ocean-label' }, geometry: { type: 'Point', coordinates: [-76.5, 15] } },
  { type: 'Feature', id: 'pacific-ocean', properties: { name: 'Océano Pacífico', kind: 'ocean-label' }, geometry: { type: 'Point', coordinates: [-85, 1] } },
  ...countries.map((feature) => {
    const points = pairs(feature.geometry);
    const x = points.reduce((sum, point) => sum + point[0], 0) / points.length;
    const y = points.reduce((sum, point) => sum + point[1], 0) / points.length;
    return { type: 'Feature', id: `label-${feature.id}`, properties: { name: feature.properties.name, kind: 'country-label' }, geometry: { type: 'Point', coordinates: [x, y] } };
  }),
]));
write(join(contextRoot, 'context-manifest.json'), {
  version: '1.0.0',
  generatedAt: '2026-07-25',
  region,
  license: 'Public domain',
  source: 'Natural Earth 1:110m version available 2026-07-25',
  sourceUrl: 'https://www.naturalearthdata.com/',
  warning: 'Las fronteras de países vecinos se muestran solo como contexto cartográfico. Los límites territoriales colombianos provienen de las fuentes oficiales declaradas.',
  maritimeBoundariesIncluded: false,
  files: ['countries-near-colombia.geojson', 'country-borders.geojson', 'coastline.geojson', 'ocean.geojson', 'geographic-labels.geojson', 'capital-cities.geojson'],
});

const rings = (geometry) => geometry.type === 'Polygon' ? geometry.coordinates : geometry.coordinates.flat();
const edgeKey = (a, b) => {
  const point = ([x, y]) => `${Number(x).toFixed(5)},${Number(y).toFixed(5)}`;
  return [point(a), point(b)].sort().join('|');
};
function topology(features) {
  const edges = new Map();
  const pointsByCode = new Map();
  for (const feature of features) {
    const code = String(feature.properties.code);
    const pointSet = new Set();
    for (const ring of rings(feature.geometry)) {
      for (let index = 1; index < ring.length; index += 1) {
        const key = edgeKey(ring[index - 1], ring[index]);
        const owners = edges.get(key) ?? [];
        owners.push(code);
        edges.set(key, owners);
        pointSet.add(`${Number(ring[index][0]).toFixed(5)},${Number(ring[index][1]).toFixed(5)}`);
      }
    }
    pointsByCode.set(code, pointSet);
  }
  const shared = new Map(features.map((feature) => [String(feature.properties.code), new Set()]));
  for (const owners of edges.values()) if (owners.length > 1) for (const a of owners) for (const b of owners) if (a !== b) shared.get(a).add(b);
  const result = {};
  for (const [code, neighbours] of shared) {
    const contacts = [];
    for (const [other, points] of pointsByCode) {
      if (other === code || neighbours.has(other)) continue;
      if ([...points].some((point) => pointsByCode.get(code).has(point))) contacts.push(other);
    }
    result[code] = {
      neighbours: [...neighbours].sort(),
      pointContacts: contacts.sort(),
      island: neighbours.size === 0,
      rule: 'shared-rounded-boundary-segment',
    };
  }
  return result;
}
const departments = read('public/data/territorial/geography/departments.geojson');
write('public/data/territorial/topology/department-neighbours.json', {
  version: '1.0.0',
  generatedAt: '2026-07-25',
  definition: 'Vecino: comparte al menos un segmento de frontera en la geometría DANE redondeada a 5 decimales. El contacto puntual se registra aparte y no se incluye automáticamente.',
  units: topology(departments.features),
});
for (const departmentCode of [...new Set(read('public/data/territorial/geography/municipalities-index.json').map((item) => item.departmentCode))]) {
  const municipalities = read(`public/data/territorial/geography/municipalities/${departmentCode}.geojson`);
  write(`public/data/territorial/topology/municipalities/${departmentCode}.json`, {
    version: '1.0.0',
    departmentCode,
    generatedAt: '2026-07-25',
    definition: 'Vecino: comparte al menos un segmento de frontera; contacto puntual separado.',
    units: topology(municipalities.features),
  });
}
console.log(`V3 DATA OK: ${countries.length} países contextuales, ${places.length} capitales, topología de 33 departamentos y 33 archivos municipales.`);
