import { expect, test } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const route = '/observatorio/laboratorio-territorial/';
const screenshot = (name: string) => resolve(`artifacts/playwright/${name}.png`);

test('renderiza 33 departamentos y permite selección departamental y municipal', async ({ page }, testInfo) => {
  const consoleErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });
  page.on('pageerror', (error) => consoleErrors.push(error.message));
  const geoJSONResponse = page.waitForResponse((response) =>
    response.url().endsWith('/data/territorial/geography/departments.geojson')
    && response.request().headers().accept?.includes('application/geo+json'),
  );

  await page.goto(route, { waitUntil: 'networkidle' });
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-tab="map"]').click();
  const response = await geoJSONResponse;
  expect(response.status()).toBe(200);
  const collection = await response.json();
  expect(collection.type).toBe('FeatureCollection');
  expect(collection.features).toHaveLength(33);

  const container = page.locator('#territory-map');
  await expect(container).toBeVisible();
  const containerBox = await container.boundingBox();
  expect(containerBox?.height ?? 0).toBeGreaterThan(400);
  const canvas = container.locator('.maplibregl-canvas');
  await expect(canvas).toBeVisible();
  const canvasBox = await canvas.boundingBox();
  expect(canvasBox?.width ?? 0).toBeGreaterThan(0);
  expect(canvasBox?.height ?? 0).toBeGreaterThan(0);
  await expect(page.locator('[data-map-status]')).toHaveAttribute('data-state', 'ready');

  const contract = await page.evaluate(() => {
    const map = (window as typeof window & { __territorialMap?: any }).__territorialMap;
    return {
      source: Boolean(map?.getSource('departments')),
      fill: Boolean(map?.getLayer('departments-fill')),
      line: Boolean(map?.getLayer('departments-line')),
      features: new Set(map?.querySourceFeatures('departments').map((feature: any) => feature.properties?.code)).size,
      rendered: map?.queryRenderedFeatures({ layers: ['departments-fill'] }).length ?? 0,
    };
  });
  expect(contract).toEqual({ source: true, fill: true, line: true, features: 33, rendered: expect.any(Number) });
  expect(contract.rendered).toBeGreaterThan(0);

  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-tab="controls"]').click();
  await page.locator('[data-department-select]').selectOption('05');
  await expect(page.locator('[data-municipality-select]')).toBeEnabled();
  await page.locator('[data-municipality-select]').selectOption({ index: 1 });
  await expect(page.locator('[data-selection-summary]')).not.toHaveText('Ninguna');
  expect(consoleErrors).toEqual([]);

  mkdirSync(resolve('artifacts/playwright'), { recursive: true });
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-tab="map"]').click();
  await page.screenshot({
    path: screenshot(testInfo.project.name === 'mobile' ? 'raices-mobile' : 'raices-escritorio'),
    fullPage: true,
  });
});

test('expone error HTTP, reintento y acceso a la tabla alternativa', async ({ page }, testInfo) => {
  await page.route('**/data/territorial/geography/departments.geojson', async (route) => {
    const accept = route.request().headers().accept ?? '';
    if (accept.includes('application/geo+json')) {
      await route.fulfill({ status: 503, contentType: 'application/json', body: '{"error":"Fallo de prueba"}' });
    } else {
      await route.continue();
    }
  });
  await page.goto(route, { waitUntil: 'networkidle' });
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-tab="map"]').click();
  const status = page.locator('[data-map-status]');
  await expect(status).toHaveAttribute('data-state', 'error');
  await expect(status).toContainText('Error HTTP 503');
  await expect(page.locator('[data-map-retry]')).toBeVisible();
  const tableLink = page.getByRole('link', { name: 'Ver datos en tabla' });
  await expect(tableLink).toBeVisible();
  await tableLink.click();
  await expect(page.locator('[data-territory-table]')).toBeVisible();
  await expect(page.locator('[data-territory-table] tr')).toHaveCount(33);
  if (testInfo.project.name === 'chromium') {
    await page.screenshot({ path: screenshot('error-con-tabla-accesible'), fullPage: true });
  }
});
