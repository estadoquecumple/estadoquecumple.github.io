import { describe,expect,it } from 'vitest';
import { readFileSync } from 'node:fs';
const page=readFileSync('src/components/territorial/TerritorialLab.astro','utf8');
const map=readFileSync('src/components/territorial/TerritoryMap.astro','utf8');
const downloads=readFileSync('src/components/territorial/DownloadPanel.astro','utf8');
describe('interfaz del laboratorio',()=>{
  it('permite cambiar modo y escenario con URL compartible',()=>expect(page).toMatch(/history\.replaceState/));
  it('permite seleccionar territorio y filtrar tabla',()=>expect(page).toMatch(/data-table-filter/));
  it('inicializa MapLibre con un contenedor vacío y estados separados',()=>{
    expect(map).toMatch(/<div id="territory-map" class="territory-map"[^>]*><\/div>/);
    expect(map).toMatch(/class="map-status" data-map-status/);
    expect(map).toMatch(/Reintentar mapa/);
  });
  it('valida WebGL, GeoJSON, bounds, errores y redimensionamiento',()=>{
    expect(map).toMatch(/hasWebGL/);
    expect(map).toMatch(/response\.ok/);
    expect(map).toMatch(/FeatureCollection/);
    expect(map).toMatch(/features\.length/);
    expect(map).toMatch(/fitBounds/);
    expect(map).toMatch(/map!?\s*\.on\('error'/);
    expect(map).toMatch(/ResizeObserver/);
  });
  it('crea source y capas departamentales y carga municipios por código',()=>{
    expect(map).toMatch(/addSource\('departments'/);
    expect(map).toMatch(/departments-fill/);
    expect(map).toMatch(/departments-line/);
    expect(map).toMatch(/departments-hover/);
    expect(map).toMatch(/municipalities\/\$\{departmentCode\}\.geojson/);
    expect(map).not.toMatch(/municipalities\/11\.geojson/);
  });
  it('mantiene popups como texto y la alternativa tabular',()=>{
    expect(map).toMatch(/\.setText\(/);
    expect(map).not.toMatch(/\.setHTML\(/);
    expect(map).toMatch(/tabla/);
  });
  it('expone fuentes y metodología',()=>{expect(page).toMatch(/SourcesPanel/);expect(page).toMatch(/MethodologyDrawer/)});
  it('implementa las descargas exigidas',()=>expect(downloads).toMatch(/CSV de vista[\s\S]*JSON de perfil[\s\S]*GeoJSON visible[\s\S]*Ficha metodológica[\s\S]*Manifiesto/));
});
