import { expect, test } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const route = '/observatorio/laboratorio-territorial/';
const screenshot = (name: string) => resolve(`artifacts/playwright/${name}.png`);

test.beforeEach(async ({ page }) => {
  await page.goto(route, { waitUntil: 'networkidle' });
});

test('RAÍCES carga mapa, selecciona departamento y mantiene tabla', async ({ page }, testInfo) => {
  await expect(page.locator('[data-workspace="roots"]')).toBeVisible();
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-panel="map"]').click();
  const map = page.locator('#territory-map');
  await map.scrollIntoViewIfNeeded();
  await expect(page.locator('[data-map-status]')).toHaveAttribute('data-state', 'ready');
  const box = await map.boundingBox();
  expect(box?.height ?? 0).toBeGreaterThan(400);
  await expect(map.locator('.maplibregl-canvas')).toBeVisible();
  const contract = await page.evaluate(() => {
    const instance = (window as typeof window & { __territorialMap?: any }).__territorialMap;
    return {
      source: Boolean(instance?.getSource('departments')),
      fill: Boolean(instance?.getLayer('departments-fill')),
      line: Boolean(instance?.getLayer('departments-line')),
    };
  });
  expect(contract).toEqual({ source: true, fill: true, line: true });
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-panel="controls"]').click();
  await page.locator('[data-department-select]').selectOption('05');
  await expect(page.locator('[data-municipality-select]')).toBeEnabled();
  await expect(page.locator('[data-territory-table] tr')).not.toHaveCount(0);
  mkdirSync(resolve('artifacts/playwright'), { recursive: true });
  await page.screenshot({ path: screenshot(`v2-roots-${testInfo.project.name}`), fullPage: true });
});

test('SAVIA cambia y restablece pesos con advertencia metodológica', async ({ page }, testInfo) => {
  await page.getByRole('button', { name: /SAVIA/ }).click();
  await expect(page.locator('[data-workspace="sap"]')).toBeVisible();
  const fiscal = page.locator('[data-weight="fiscal"]');
  await fiscal.fill('60');
  await expect(fiscal).toHaveValue('60');
  await page.locator('[data-reset-weights]').click();
  await expect(fiscal).toHaveValue('25');
  await page.locator('[data-evaluate]').click();
  await expect(page.locator('[data-capacity-profile]')).toContainText('evidencia insuficiente');
  await expect(page.locator('.method-warning')).toContainText('No se determina');
  await page.screenshot({ path: screenshot(`v2-savia-${testInfo.project.name}`), fullPage: true });
});

test('SEMILLAS crea, une, modifica instituciones, deshace, guarda y exporta', async ({ page }, testInfo) => {
  await page.getByRole('button', { name: /SEMILLAS/ }).click();
  await page.locator('[data-create-scenario]').click();
  await expect(page.locator('[data-save-status]')).toContainText('Guardado');
  const checks = page.locator('[data-territory-check]');
  await checks.nth(0).check();
  await checks.nth(1).check();
  await page.locator('[data-merge]').click();
  await expect(page.locator('[data-scenario-history]')).toContainText('Unió');
  if (testInfo.project.name === 'chromium') {
    await page.locator('[data-draw-rectangle]').click();
    const map = page.locator('#territory-map');
    await map.scrollIntoViewIfNeeded();
    const mapBox = await map.boundingBox();
    if (!mapBox) throw new Error('Mapa sin dimensiones para dibujo.');
    await page.mouse.click(mapBox.x + mapBox.width * .4, mapBox.y + mapBox.height * .4);
    await page.mouse.click(mapBox.x + mapBox.width * .6, mapBox.y + mapBox.height * .6);
    await page.locator('[data-split-geometry]').scrollIntoViewIfNeeded();
    await page.locator('[data-split-geometry]').click();
    await expect(page.locator('[data-scenario-history]')).toContainText('corte geométrico experimental');
  }
  await page.locator('[data-assign-competence]').click();
  await page.locator('[data-change-government]').click();
  await page.locator('[data-finance="transferencias"]').check();
  await page.locator('[data-change-finance]').click();
  await page.locator('[data-change-planning]').click();
  await expect(page.locator('[data-scenario-history]')).toContainText('financiación');
  await page.locator('[data-undo]').click();
  await page.locator('[data-redo]').click();
  await expect(page.locator('[data-save-status]')).toContainText('Guardado');
  await page.getByText('Descargas e intercambio', { exact: true }).click();
  const downloadPromise = page.waitForEvent('download');
  await page.locator('[data-export-json]').click();
  expect((await downloadPromise).suggestedFilename()).toMatch(/scenario-.*\.json/);
  await page.getByText('Comparación', { exact: true }).click();
  await page.locator('[data-compare-current]').click();
  await expect(page.locator('[data-comparison-output]')).toContainText('Impacto jurídico');
  await page.reload({ waitUntil: 'networkidle' });
  await page.getByRole('button', { name: /SEMILLAS/ }).click();
  expect(await page.locator('[data-local-scenarios] option').count()).toBeGreaterThan(1);
  await page.screenshot({ path: screenshot(`v2-seeds-${testInfo.project.name}`), fullPage: true });
});

test('fallo GeoJSON muestra error y conserva alternativa textual', async ({ page }, testInfo) => {
  await page.route('**/data/territorial/geography/departments.geojson', (route) => route.fulfill({ status: 503, contentType: 'application/json', body: '{}' }));
  await page.reload({ waitUntil: 'networkidle' });
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-panel="map"]').click();
  await expect(page.locator('[data-map-status]')).toHaveAttribute('data-state', 'error');
  await expect(page.getByRole('button', { name: 'Reintentar mapa' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Tabla territorial y selección' })).toBeVisible();
});

test('fallo IndexedDB no bloquea RAÍCES ni el mapa', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, 'indexedDB', { configurable: true, get: () => { throw new Error('IndexedDB bloqueada para prueba'); } });
  });
  await page.reload({ waitUntil: 'networkidle' });
  await expect(page.locator('[data-workspace="roots"]')).toBeVisible();
  await expect(page.locator('[data-map-status]')).toHaveAttribute('data-state', 'ready');
  await expect(page.locator('[data-operation-status]')).toContainText('IndexedDB');
});

test('captura comparación y vista móvil', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'mobile', 'Captura móvil solo en el proyecto móvil.');
  await page.getByRole('button', { name: /SEMILLAS/ }).click();
  await page.locator('[data-mobile-panel="map"]').click();
  const map = page.locator('#territory-map');
  await expect(map).toBeVisible();
  expect((await map.boundingBox())?.height ?? 0).toBeGreaterThanOrEqual(440);
  await page.screenshot({ path: screenshot('v2-mobile'), fullPage: true });
});
