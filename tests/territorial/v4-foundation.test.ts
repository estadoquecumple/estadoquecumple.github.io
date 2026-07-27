import { describe, expect, it } from 'vitest';
import { polygon } from '@turf/helpers';
import {
  INTERACTIVE_COORDINATE_LIMIT,
  differenceGeometries,
  dissolveGeometries,
  geometryRelations,
  inspectGeometry,
  intersectGeometries,
} from '../../src/data/territorial/geometry-v4';
import { addUnit, createScenario } from '../../src/data/territorial/scenario-v2';
import { compileScenario, createCapsule, reproducibilityCapsuleSchema } from '../../src/data/territorial/scenario-v4';

const square = (x: number): GeoJSON.Polygon => polygon([[[x, 0], [x + 2, 0], [x + 2, 2], [x, 2], [x, 0]]]).geometry;

describe('geometría Turf V4', () => {
  it('disuelve polígonos realmente y valida el resultado', () => {
    const result = dissolveGeometries([square(0), square(1)]);
    expect(result.ok).toBe(true);
    expect(result.valid).toBe(true);
    expect(result.geometry?.type).toMatch(/Polygon/);
  });
  it('calcula diferencia, intersección, solape y contacto', () => {
    expect(differenceGeometries(square(0), square(1)).geometry).not.toBeNull();
    expect(intersectGeometries(square(0), square(1)).geometry).not.toBeNull();
    expect(geometryRelations(square(0), square(1))).toMatchObject({ intersects: true, overlaps: true });
    expect(geometryRelations(square(0), square(2)).touches).toBe(true);
  });
  it('limpia e inspecciona polígonos', () => expect(inspectGeometry(square(0))).toMatchObject({ valid: true, partsAfterUnkink: 1 }));
  it('deriva operaciones grandes al backend sin bloquear', () => {
    const ring = Array.from({ length: INTERACTIVE_COORDINATE_LIMIT + 1 }, (_, index) => [index, index % 2] as [number, number]);
    ring.push(ring[0]);
    expect(dissolveGeometries([{ type: 'Polygon', coordinates: [ring] }, square(0)]).backendRequired).toBe(true);
  });
});

describe('compilador y cápsula V4', () => {
  it('bloquea unidades sin padre y responsabilidades sin financiación', () => {
    let scenario = createScenario('Incompleto');
    scenario = addUnit(scenario, { id: 'region:test', name: 'Región', levelId: 'region', parentId: null });
    scenario.competences.push({ function: 'salud', levelId: 'region', modality: 'exclusive', role: 'execution' });
    const result = compileScenario(scenario);
    expect(result.valid).toBe(false);
    expect(result.validations.map((item) => item.code)).toEqual(expect.arrayContaining(['missing-parent', 'responsibility-without-finance']));
  });
  it('crea expediente reproducible con proveedores desactivados', () => {
    const scenario = createScenario('Base');
    const hash = 'a'.repeat(64);
    const capsule = createCapsule(scenario, {
      commit: 'abcdef123',
      contractVersion: '4.0.0',
      legalRegistryVersion: '3.0.0',
      datasets: [{ id: 'dane', version: '2025', sha256: hash }],
      rules: [{ id: 'compiler', version: '4.0.0', sha256: hash }],
      models: [],
    }, { compilation: compileScenario(scenario) });
    expect(reproducibilityCapsuleSchema.parse(capsule).providers).toEqual({ llm: 'none', embeddings: 'none' });
  });
});
