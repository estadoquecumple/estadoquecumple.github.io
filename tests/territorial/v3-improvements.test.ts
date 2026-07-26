import { describe, expect, it } from 'vitest';
import { calculateScenarioDiff } from '../../src/data/territorial/consequences/compare';
import { scenarioToMapCollections } from '../../src/data/territorial/scenario-map';
import { addUnit, createScenario, mergeUnits } from '../../src/data/territorial/scenario-v2';
import { safeCsvCell, safeExternalUrl, scenarioCsv } from '../../src/data/territorial/security';
import { classifyBoundaryRelation, repairRing } from '../../src/data/territorial/topology-v3';
import { labelTerritorialUnit, normalizeMpioTipo } from '../../src/data/territorial/unit-types';
import { territorialExamples } from '../../src/data/territorial/examples-v3';
import { metricsForSelection } from '../../src/data/territorial/official-metrics';

const square = (x: number) => ({ type: 'Polygon', coordinates: [[[x, 0], [x + 1, 0], [x + 1, 1], [x, 1], [x, 0]]] });

describe('mejoras funcionales V3', () => {
  it('normaliza solo tipos territoriales oficiales suministrados', () => {
    expect(normalizeMpioTipo('Distrito Capital')).toBe('Distrito Capital');
    expect(normalizeMpioTipo('ÁREA NO MUNICIPALIZADA')).toBe('área no municipalizada');
    expect(normalizeMpioTipo('categoría inventada')).toBeNull();
    expect(labelTerritorialUnit({ unitType: null })).toContain('no suministrado');
  });

  it('clasifica rook, queen y discontinuidad con tolerancia y repara anillos', () => {
    const a = [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]] as [number, number][];
    const rook = [[1, 0], [2, 0], [2, 1], [1, 1], [1, 0]] as [number, number][];
    const queen = [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]] as [number, number][];
    expect(classifyBoundaryRelation(a, rook)).toBe('rook');
    expect(classifyBoundaryRelation(a, queen)).toBe('queen');
    expect(classifyBoundaryRelation(a, queen.map(([x, y]) => [x + 5, y]))).toBe('disjoint');
    expect(repairRing([[0, 0], [1, 0], [0, 1]])).toHaveLength(4);
    expect(() => repairRing([[0, 0], [0, 0]])).toThrow(/inválida/);
  });

  it('une geometrías y proyecta cada estado a colecciones cartográficas', () => {
    let scenario = createScenario('Mapa');
    scenario = addUnit(scenario, { id: 'municipality:a', name: 'A', levelId: 'municipality', geometry: square(0) });
    scenario = addUnit(scenario, { id: 'municipality:b', name: 'B', levelId: 'municipality', geometry: square(1) });
    const merged = mergeUnits(scenario, ['municipality:a', 'municipality:b'], 'AB', 'region', 'absorbed');
    expect(merged.units.at(-1)?.geometry).toMatchObject({ type: 'MultiPolygon' });
    const collections = scenarioToMapCollections(merged);
    expect(collections['scenario-created'].features.some((item) => item.properties.name === 'AB')).toBe(true);
    expect(collections['scenario-transformed'].features).toHaveLength(2);
    expect(collections['scenario-units'].features.length).toBeGreaterThan(2);
  });

  it('calcula diferencias desde estados estructurados y no desde regex del resumen', () => {
    const before = createScenario('Antes');
    const after = addUnit(before, { name: 'Región', levelId: 'region' });
    const diff = calculateScenarioDiff(before, after.history.at(-1)!, after, { figure: 'RET', legalPath: 'Ley 1962 y requisitos constitucionales' });
    expect(diff.find((item) => item.dimension === 'unidades')?.after).toBe(String(after.units.length));
    expect(diff.find((item) => item.dimension === 'población y capacidad')?.kind).toBe('missing-data');
    expect(diff.find((item) => item.dimension === 'ruta jurídica y transición')?.after).toContain('Ley 1962');
  });

  it('neutraliza fórmulas CSV y URLs activas', () => {
    for (const value of ['=1+1', '+CMD', '-2+3', '@SUM(A1)']) expect(safeCsvCell(value)).toMatch(/^"'/);
    expect(scenarioCsv([{ nombre: '=HYPERLINK("javascript:x")' }], ['nombre'])).toContain("'=HYPERLINK");
    expect(safeExternalUrl('javascript:alert(1)')).toBeNull();
    expect(safeExternalUrl('https://dane.gov.co/')).toBe('https://dane.gov.co/');
  });

  it('solo habilita los tres ejemplos completamente implementados', () => {
    expect(territorialExamples.filter((item) => item.available).map((item) => item.id)).toEqual([
      'bogota-sabana', 'rap-caribe-ret', 'without-departments',
    ]);
    expect(territorialExamples.filter((item) => !item.available).every((item) => item.selection.length > 0)).toBe(true);
  });

  it('conecta gobierno y SGR por territorio sin atribuir SECOP nacional a la selección', () => {
    const metrics=metricsForSelection(
      [{code:'05001',name:'Medellín',level:'municipality'},{code:'05',name:'Antioquia',level:'department'}],
      [{code:'05001',entityCount:31}],
      [{territoryLabel:'ANTIOQUIA',projectCount:337}],
      [{kind:'contracts',recordCount:100}],
    );
    expect(metrics.find((item)=>item.id==='government-entities')).toMatchObject({value:31,kind:'calculated'});
    expect(metrics.find((item)=>item.id==='sgr-project-sample')).toMatchObject({value:337,kind:'calculated'});
    expect(metrics.find((item)=>item.id==='secop-system')?.warning).toContain('no contratación atribuible');
  });
});
