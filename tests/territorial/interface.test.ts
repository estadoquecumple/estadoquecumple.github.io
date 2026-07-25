import { describe,expect,it } from 'vitest';
import { readFileSync } from 'node:fs';
const page=readFileSync('src/components/territorial/TerritorialLab.astro','utf8');
const map=readFileSync('src/components/territorial/TerritoryMap.astro','utf8');
const downloads=readFileSync('src/components/territorial/DownloadPanel.astro','utf8');
describe('interfaz del laboratorio',()=>{
  it('permite cambiar modo y escenario con URL compartible',()=>expect(page).toMatch(/history\.replaceState/));
  it('permite seleccionar territorio y filtrar tabla',()=>expect(page).toMatch(/data-table-filter/));
  it('carga MapLibre y mantiene alternativa textual',()=>{expect(map).toMatch(/maplibre-gl/);expect(map).toMatch(/tabla/)}); 
  it('expone fuentes y metodología',()=>{expect(page).toMatch(/SourcesPanel/);expect(page).toMatch(/MethodologyDrawer/)});
  it('implementa las descargas exigidas',()=>expect(downloads).toMatch(/CSV de vista[\s\S]*JSON de perfil[\s\S]*GeoJSON visible[\s\S]*Ficha metodológica[\s\S]*Manifiesto/));
});
