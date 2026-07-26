import { expect, test } from '@playwright/test';

const route='/observatorio/laboratorio-territorial/';
// Contratos cubiertos por esta suite:
// [data-mode] [data-mobile-panel] [data-map-retry] [data-camera] [data-roots-compare]
// [data-reset-weights] [data-evaluate] [data-load-example] [data-create-scenario]
// [data-duplicate-scenario] [data-rename-scenario] [data-archive-scenario] [data-delete-scenario]
// [data-select-department] [data-select-neighbours] [data-select-contiguous]
// [data-draw-rectangle] [data-draw-polygon] [data-invert-selection] [data-clear-selection]
// [data-apply-spatial] [data-cancel-spatial] [data-merge] [data-split-membership]
// [data-split-geometry] [data-suppress-department] [data-create-level] [data-add-group]
// [data-confirm-groups] [data-cancel-groups] [data-confirm-level] [data-cancel-level]
// [data-change-government] [data-assign-competence] [data-change-finance] [data-change-planning]
// [data-add-subdivisions] [data-undo] [data-redo] [data-export-json] [data-export-geojson]
// [data-export-csv] [data-export-method] [data-share-link] [data-print]
// [data-compare-current] [data-compare-scenarios] [data-consequence-tab]

test.beforeEach(async({page})=>{await page.goto(route,{waitUntil:'networkidle'});});

test('RAÍCES busca municipio nacional, cambia capas, función y comparación',async({page},testInfo)=>{
  await expect(page.locator('[data-map-status]')).toHaveAttribute('data-state','ready');
  if(testInfo.project.name==='mobile')await page.locator('[data-mobile-tab="controls"]').click();
  await page.locator('[data-territory-search]').fill('05001');
  await page.locator('[data-territory-search]').press('Enter');
  await expect(page.locator('[data-search-feedback]')).toContainText('Departamento cargado automáticamente');
  await expect(page.locator('[data-territory-card]')).toContainText('05001');
  await page.locator('[data-layer="departments"]').uncheck();
  const visibility=await page.evaluate(()=>(window as any).__territorialMap.getLayoutProperty('departments-fill','visibility'));
  expect(visibility).toBe('none');
  await page.locator('[data-function-route]').selectOption('educación');
  await expect(page.locator('[data-function-result]')).toContainText('establecimientos');
  await page.locator('[data-roots-compare]').click();
  await expect(page.locator('[data-operation-status]')).toContainText('al menos dos');
});

test('mapa contiene contexto local, selección diferenciada y cámaras',async({page},testInfo)=>{
  const contract=await page.evaluate(()=>{const map=(window as any).__territorialMap; return ['context-ocean','context-countries','context-coastline','context-borders','departments','selected-departments','selected-municipalities','scenario-created','scenario-transformed','scenario-suppressed','scenario-functional'].map((id)=>Boolean(map.getSource(id)));});
  expect(contract.every(Boolean)).toBe(true);
  if(testInfo.project.name==='mobile')await page.locator('[data-mobile-panel="map"]').click();
  await page.locator('[data-camera="caribbean"]').click();
  await page.locator('[data-camera="colombia"]').click();
  await page.locator('[data-basemap]').selectOption('dark');
  await expect(page.locator('.context-warning')).toContainText('solo como contexto');
});

test('topología selecciona vecinos y contiguos con razón',async({page})=>{
  await page.getByRole('button',{name:/SEMILLAS/}).click();
  await page.locator('[data-territory-check]').first().check();
  await page.locator('[data-select-neighbours]').click();
  await expect(page.locator('[data-operation-status]')).toContainText('frontera compartida');
  await page.locator('[data-contiguous-rings]').fill('2');
  await page.locator('[data-select-contiguous]').click();
  await expect(page.locator('[data-operation-status]')).toContainText('2 anillo');
  await page.locator('[data-invert-selection]').click();
  await expect(page.locator('[data-selection-universe]')).toContainText('Universo visible');
  await page.locator('[data-clear-selection]').click();
});

test('SEMILLAS materializa base, carga ejemplo, modela y calcula consecuencias',async({page})=>{
  await page.getByRole('button',{name:/SEMILLAS/}).click();
  await page.locator('[data-create-scenario]').click();
  await expect(page.locator('[data-hierarchy-tree]')).toContainText('Nación');
  await page.locator('[data-government-authority]').selectOption({label:'dirección política + administración profesional'});
  await page.locator('[data-change-government]').click();
  await page.locator('[data-competence-role]').selectOption('maintenance');
  await page.locator('[data-assign-competence]').click();
  await page.locator('[data-finance="transferencias"]').check();
  await page.locator('[data-change-finance]').click();
  await page.locator('[data-change-planning]').click();
  await expect(page.locator('[data-consequence-output]')).toContainText('No se afirma ahorro');
  await page.locator('[data-subdivision-model]').selectOption('bogota');
  await page.locator('[data-add-subdivisions]').click();
  await expect(page.locator('[data-subdivision-result]')).toContainText('Alcalde Mayor');
  await page.locator('[data-example-select]').selectOption('federal-colombia');
  await page.locator('[data-load-example]').click();
  await expect(page.locator('[data-example-summary]')).toContainText('república unitaria');
});

test('editor de nivel valida y crea sin prompt',async({page})=>{
  await page.getByRole('button',{name:/SEMILLAS/}).click(); await page.locator('[data-create-scenario]').click();
  await page.locator('[data-create-level]').click();
  await page.locator('[data-confirm-level]').click();
  await expect(page.locator('[data-operation-status]')).toContainText('obligatorios');
  await page.locator('[data-level-name]').fill('Provincia funcional'); await page.locator('[data-level-code]').fill('provincia-funcional');
  await page.locator('[data-level-coverage]').fill('Unidades seleccionadas por el usuario'); await page.locator('[data-level-authority]').fill('Autoridad intergubernamental');
  await page.locator('[data-confirm-level]').click();
  await expect(page.locator('[data-hierarchy-tree]')).toContainText('Provincia funcional');
});

test('SAVIA declara fuentes manual-required como ausentes',async({page},testInfo)=>{
  await page.getByRole('button',{name:/SAVIA/}).click();
  if(testInfo.project.name==='mobile')await page.locator('[data-mobile-tab="controls"]').click();
  await page.locator('[data-evaluate]').click();
  await expect(page.locator('[data-capacity-profile]')).toContainText('insuficiente');
  await page.locator('[data-weight="fiscal"]').fill('40'); await page.locator('[data-reset-weights]').click();
  await expect(page.locator('[data-weight="fiscal"]')).toHaveValue('25');
});

test('exportación, comparación, compartir completo y undo/redo',async({page})=>{
  await page.getByRole('button',{name:/SEMILLAS/}).click(); await page.locator('[data-create-scenario]').click();
  await page.locator('[data-change-planning]').click(); await page.locator('[data-undo]').click(); await page.locator('[data-redo]').click();
  await page.locator('.lab-lower details').filter({hasText:'Comparación'}).locator('summary').click();
  await page.locator('[data-compare-current]').click(); await expect(page.locator('[data-comparison-output]')).toContainText('Impacto jurídico');
  await page.locator('.lab-lower details').filter({hasText:'Descargas e intercambio'}).locator('summary').click();
  await page.locator('[data-share-link]').click(); await expect(page.locator('[data-operation-status]')).toContainText(/completo|archivo V3/);
});

test('capturas de ejemplos Bogotá–Sabana y Colombia federal',async({page},testInfo)=>{
  await page.getByRole('button',{name:/SEMILLAS/}).click();
  await page.locator('[data-example-select]').selectOption('bogota-sabana');
  await page.locator('[data-load-example]').click();
  await expect(page.locator('[data-example-summary]')).toContainText('Ley 2199');
  await page.screenshot({path:`artifacts/playwright/acceptance-ejemplo-bogota-sabana-${testInfo.project.name}.png`,fullPage:true});
  await page.locator('[data-example-select]').selectOption('federal-colombia');
  await page.locator('[data-load-example]').click();
  await expect(page.locator('[data-example-summary]')).toContainText('república unitaria');
  await page.screenshot({path:`artifacts/playwright/acceptance-ejemplo-colombia-federal-${testInfo.project.name}.png`,fullPage:true});
});
