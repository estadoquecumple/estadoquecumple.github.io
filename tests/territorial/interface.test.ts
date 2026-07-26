import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const lab = readFileSync('src/components/territorial/TerritorialLab.astro', 'utf8');
const map = readFileSync('src/components/territorial/TerritoryMap.astro', 'utf8');
const roots = readFileSync('src/components/territorial/RootsWorkspace.astro', 'utf8');
const sap = readFileSync('src/components/territorial/SapWorkspace.astro', 'utf8');
const seeds = readFileSync('src/components/territorial/SeedsWorkspace.astro', 'utf8');
const model = readFileSync('src/data/territorial/scenario-v2.ts', 'utf8');

describe('contrato de interfaz V3', () => {
  it('separa RAÍCES, SAVIA y SEMILLAS', () => {
    expect(roots).toMatch(/RAÍCES · VER/);
    expect(sap).toMatch(/SAVIA · EVALUAR/);
    expect(seeds).toMatch(/SEMILLAS · DISEÑAR/);
  });
  it('RAÍCES no expone operaciones de edición', () => {
    expect(roots).not.toMatch(/data-merge|data-split|data-change-government/);
    expect(roots).toMatch(/data-department-select[\s\S]*data-municipality-select/);
  });
  it('SAVIA evalúa pesos sin modificar escenarios', () => {
    expect(sap).toMatch(/data-weight[\s\S]*data-reset-weights[\s\S]*data-evaluate/);
    expect(sap).not.toMatch(/data-create-scenario|data-merge/);
  });
  it('SEMILLAS implementa estructura e instituciones', () => {
    for (const contract of ['data-merge', 'data-split-membership', 'data-split-geometry', 'data-suppress-department', 'data-change-government', 'data-assign-competence', 'data-change-finance', 'data-change-planning']) expect(seeds).toContain(contract);
  });
  it('persiste, importa, exporta, compara y permite undo/redo', () => {
    for (const contract of ['ScenarioStore', 'data-import-json', 'data-export-json', 'data-export-geojson', 'data-export-csv', 'data-compare-current', 'data-undo', 'data-redo']) expect(lab).toContain(contract);
  });
  it('mantiene alternativa tabular operativa', () => expect(lab).toMatch(/data-territory-table[\s\S]*data-territory-check/));
  it('mantiene la corrección MapLibre V1', () => {
    expect(map).toMatch(/from 'maplibre-gl'/);
    expect(map).not.toMatch(/import \* as maplibregl|municipalities\/11\.geojson/);
    expect(map).toMatch(/departments-fill[\s\S]*departments-line[\s\S]*departments-hover/);
    expect(map).toMatch(/ResizeObserver[\s\S]*fitBounds[\s\S]*setText/);
  });
  it('clasifica todos los resultados', () => expect(model).toMatch(/observed[\s\S]*calculated[\s\S]*assumption[\s\S]*unavailable/));
  it('migra claves antiguas con schemaVersion 3', () => expect(model).toMatch(/LAB_SCHEMA_VERSION = 3[\s\S]*LEGACY_KEYS[\s\S]*removeItem/));
});
