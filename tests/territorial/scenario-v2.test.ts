import { describe, expect, it } from 'vitest';
import {
  LAB_SCHEMA_VERSION,
  ScenarioTimeline,
  addUnit,
  aggregateCompleteUnits,
  assignCompetence,
  changeFinance,
  changeGovernment,
  changePlanning,
  classifyLegalImpact,
  createLevel,
  createScenario,
  exportScenario,
  importScenario,
  mergeUnits,
  migrateLocalState,
  splitByGeometry,
  splitByMembership,
  suppressUnit,
  territorialScenarioSchema,
  transformUnit,
} from '../../src/data/territorial/scenario-v2';

const seeded = () => {
  let scenario = createScenario('Prueba');
  scenario = addUnit(scenario, { id: 'municipality:05001', name: 'Medellín', levelId: 'municipality', officialCodes: ['05001'] });
  scenario = addUnit(scenario, { id: 'municipality:05002', name: 'Abejorral', levelId: 'municipality', officialCodes: ['05002'] });
  scenario = addUnit(scenario, { id: 'department:05', name: 'Antioquia', levelId: 'department', memberIds: ['municipality:05001', 'municipality:05002'], officialCodes: ['05'] });
  return scenario;
};

describe('modelo territorial V3', () => {
  it('crea un esquema tipado y versionado', () => {
    const scenario = createScenario();
    expect(scenario.schemaVersion).toBe(LAB_SCHEMA_VERSION);
    expect(territorialScenarioSchema.parse(scenario)).toEqual(scenario);
  });
  it('rechaza esquemas desconocidos con detalle', () => expect(() => importScenario({ schemaVersion: 99 })).toThrow(/Escenario incompatible/));
  it('migra solo preferencias compatibles y elimina claves V1', () => {
    const values = new Map([['cams-territorial-scenarios-v1', JSON.stringify({ mode: 'sap', scenarios: [{ unsafe: true }] })]]);
    const storage = { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, value: string) => values.set(key, value), removeItem: (key: string) => { values.delete(key); } };
    expect(migrateLocalState(storage)).toEqual({ migratedPreferences: true, discardedScenarios: true });
    expect(values.has('cams-territorial-scenarios-v1')).toBe(false);
  });
  it('une unidades y conserva integrantes según disposición', () => {
    const result = mergeUnits(seeded(), ['municipality:05001', 'municipality:05002'], 'Valle de Aburrá', 'region', 'political');
    expect(result.units.at(-1)?.memberIds).toHaveLength(2);
    expect(result.history.at(-1)?.kind).toBe('merge-units');
  });
  it('absorbe integrantes cuando se solicita', () => {
    const result = mergeUnits(seeded(), ['municipality:05001', 'municipality:05002'], 'Unidad', 'region', 'absorbed');
    expect(result.units.filter((unit) => unit.state === 'absorbed')).toHaveLength(2);
  });
  it('divide por pertenencias sin duplicarlas', () => {
    const result = splitByMembership(seeded(), 'department:05', [{ name: 'Norte', memberIds: ['municipality:05001'] }, { name: 'Sur', memberIds: ['municipality:05002'] }]);
    expect(result.units.filter((unit) => unit.id.startsWith('cams-split'))).toHaveLength(2);
    expect(result.history.at(-1)?.kind).toBe('split-by-membership');
  });
  it('marca división geométrica experimental sin cifras falsas', () => {
    const result = splitByGeometry(seeded(), 'municipality:05001', { type: 'Polygon', coordinates: [] }, ['municipality:05001']);
    expect(result.history.at(-1)?.payload.population).toEqual({ value: null, kind: 'unavailable' });
    expect(result.assumptions.at(-1)?.uncertainty).toBe('alta');
  });
  it('transforma y suprime solo dentro del escenario', () => {
    const transformed = transformUnit(seeded(), 'department:05', 'administrative-only', 'región administrativa');
    expect(transformed.units.find((unit) => unit.id === 'department:05')?.administrativeStatus).toBe('región administrativa');
    expect(suppressUnit(transformed, 'department:05').units.find((unit) => unit.id === 'department:05')?.state).toBe('suppressed-in-scenario');
  });
  it('crea niveles sin acoplarlos a geometrías', () => {
    const result = createLevel(seeded(), 'Provincia', 2, 'administrativa');
    expect(result.levels.some((level) => level.name === 'Provincia')).toBe(true);
  });
  it('reasigna competencias con modalidad', () => {
    const result = assignCompetence(seeded(), 'salud', 'region', 'shared');
    expect(result.competences).toContainEqual({ function: 'salud', levelId: 'region', modality: 'shared', role: 'execution' });
  });
  it('cambia gobierno, financiación y planeación separadamente', () => {
    let result = changeGovernment(seeded(), { unitId: 'department:05', authority: 'colegiada', selection: 'corporación', termYears: 4, reelection: 'no', representativeBody: 'asamblea' });
    result = changeFinance(result, { levelId: 'department', instruments: ['igualación'], note: 'sin estimar recaudo' });
    result = changePlanning(result, { levelId: 'department', horizonYears: 12, instruments: ['plan estratégico'], review: 'cuatrienal' });
    expect(result.governments).toHaveLength(1);
    expect(result.finances[0].note).toMatch(/sin estimar/);
    expect(result.planning[0].horizonYears).toBe(12);
  });
  it('deshace y rehace estados completos', () => {
    const initial = seeded();
    const timeline = new ScenarioTimeline(initial);
    const next = timeline.apply(assignCompetence(initial, 'agua', 'municipality', 'exclusive'));
    expect(timeline.undo().competences).toHaveLength(0);
    expect(timeline.redo()).toEqual(next);
  });
  it('agrega unidades completas y conserva ausencias', () => {
    expect(aggregateCompleteUnits([{ population: 10, area: 2 }, { population: 20, area: 3 }])).toMatchObject({ population: { value: 30, kind: 'calculated' }, area: { value: 5 } });
    expect(aggregateCompleteUnits([{ population: null }, { population: 20 }]).population.kind).toBe('unavailable');
  });
  it('clasifica impacto jurídico preliminar por disparadores', () => {
    const suppressed = suppressUnit(seeded(), 'department:05');
    expect(classifyLegalImpact(suppressed).legalImpacts.some((impact) => impact.category.includes('reforma constitucional'))).toBe(true);
  });
  it('exporta e importa sin ejecutar contenido', () => {
    const scenario = seeded();
    const text = exportScenario(scenario);
    expect(importScenario(JSON.parse(text))).toEqual(scenario);
    expect(text).toContain('"schemaVersion": 3');
  });
  it('toda operación entra al historial', () => {
    const scenario = assignCompetence(seeded(), 'catastro', 'region', 'delegated');
    expect(scenario.history.every((item) => item.id && item.at && item.summary)).toBe(true);
  });
});
