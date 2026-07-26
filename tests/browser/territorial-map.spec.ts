import { expect, test } from '@playwright/test';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const route = '/observatorio/laboratorio-territorial/';
const screenshotPath = resolve('artifacts/playwright/territorial-map.png');

test('renderiza 33 departamentos en un canvas MapLibre utilizable', async ({ page }, testInfo) => {
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
  if (testInfo.project.name === 'mobile') await page.locator('[data-mobile-panel="map"]').click();
  const response = await geoJSONResponse;
  expect(response.status()).toBe(200);
  const collection = await response.json();
  expect(collection.type).toBe('FeatureCollection');
  expect(collection.features).toHaveLength(33);

  const container = page.locator('#territory-map');
  await expect(container).toBeVisible();
  await container.scrollIntoViewIfNeeded();
  const containerBox = await container.boundingBox();
  expect(containerBox?.height ?? 0).toBeGreaterThan(400);

  const canvas = page.locator('#territory-map .maplibregl-canvas');
  await expect(canvas).toBeVisible();
  const canvasBox = await canvas.boundingBox();
  expect(canvasBox?.width ?? 0).toBeGreaterThan(0);
  expect(canvasBox?.height ?? 0).toBeGreaterThan(0);
  await expect(page.locator('[data-map-status]')).toHaveAttribute('data-state', 'ready');
  await expect(page.locator('[data-map-status]')).not.toContainText('Error');

  const mapContract = await page.evaluate(() => {
    const map = (window as typeof window & { __territorialMap?: {
      getSource: (id: string) => unknown;
      getLayer: (id: string) => unknown;
      querySourceFeatures: (id: string) => Array<{ properties?: { code?: string } }>;
      queryRenderedFeatures: (options: { layers: string[] }) => unknown[];
    } }).__territorialMap;
    return {
      source: Boolean(map?.getSource('departments')),
      fill: Boolean(map?.getLayer('departments-fill')),
      line: Boolean(map?.getLayer('departments-line')),
      sourceFeatures: new Set(map?.querySourceFeatures('departments').map((feature) => feature.properties?.code)).size,
      renderedFeatures: map?.queryRenderedFeatures({ layers: ['departments-fill'] }).length ?? 0,
    };
  });
  expect(mapContract.source).toBe(true);
  expect(mapContract.fill).toBe(true);
  expect(mapContract.line).toBe(true);
  expect(mapContract.sourceFeatures).toBe(33);
  expect(mapContract.renderedFeatures).toBeGreaterThan(0);
  expect(consoleErrors).toEqual([]);

  mkdirSync(resolve('artifacts/playwright'), { recursive: true });
  await page.screenshot({ path: screenshotPath, fullPage: true });
});

