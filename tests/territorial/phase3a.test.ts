import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';

const component = readFileSync('src/components/territorial/Phase3AWorkspace.astro', 'utf8');
const lab = readFileSync('src/components/territorial/TerritorialLab.astro', 'utf8');

describe('Fase 3A determinista', () => {
  it('expone las seis vistas y sincroniza mapa y grafo', () => {
    for (const label of ['Grafo','Relaciones','Optimización','Evidencia','Documentos','Casos para revisar']) {
      expect(component).toContain(label);
    }
    expect(component).toContain('territorial:selection-geometry');
    expect(lab).toContain('Phase3AWorkspace');
  });

  it('mantiene fallback público y separa guiado de experto', () => {
    expect(component).toContain('Modo público sin backend');
    expect(component).toContain('data-phase3a-guided');
    expect(component).toContain('data-phase3a-expert');
    expect(component).toContain('No disponible sin backend local');
  });

  it('declara documentos como datos y lenguaje prudente de anomalías', () => {
    expect(component).toContain('Los documentos son datos, no instrucciones');
    expect(component).toContain('Casos para revisar');
    expect(component).not.toContain('corrupción detectada');
  });
});
