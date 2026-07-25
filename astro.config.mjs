import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const siteUrl =
  process.env.SITE_URL ??
  'https://estadoquecumple.github.io';

export default defineConfig({
  site: siteUrl,
  output: 'static',
  integrations: [sitemap({
    filter: (page) => !new URL(page).pathname.startsWith('/buscar/'),
  })],
});
