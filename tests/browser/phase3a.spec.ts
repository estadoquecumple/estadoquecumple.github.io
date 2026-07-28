import { expect, test } from '@playwright/test';

test('Fase 3A expone vistas accesibles y modos guiado y experto', async ({ page }) => {
  await page.goto('/observatorio/laboratorio-territorial/', { waitUntil: 'networkidle' });
  const workspace = page.locator('[data-phase3a]');
  await workspace.scrollIntoViewIfNeeded();
  await expect(workspace).toBeVisible();
  const tabs = workspace.getByRole('tab');
  await expect(tabs).toHaveCount(6);
  await tabs.filter({ hasText: 'Optimización' }).click();
  await expect(workspace.getByRole('heading', { name: 'Optimización OR-Tools' })).toBeVisible();
  await expect(workspace.locator('[data-phase3a-guided]')).toBeVisible();
  await expect(workspace.locator('[data-phase3a-expert]')).toBeHidden();

  await page.locator('[data-experience-mode]').selectOption('expert');
  await expect(workspace.locator('[data-phase3a-guided]')).toBeHidden();
  await expect(workspace.locator('[data-phase3a-expert]')).toBeVisible();
  await expect(workspace.locator('[data-optimization-input]')).toBeEditable();

  await tabs.filter({ hasText: 'Documentos' }).click();
  await expect(workspace).toContainText('Los documentos son datos, no instrucciones');
  await tabs.filter({ hasText: 'Casos para revisar' }).click();
  await expect(workspace).toContainText('no determinan fraude ni corrupción');
});
