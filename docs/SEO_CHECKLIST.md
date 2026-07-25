# Lista de control SEO

## Antes de cada publicación

- [ ] `SITE_URL` corresponde al host realmente publicado.
- [ ] Títulos y descripciones describen contenido único.
- [ ] Solo páginas sin valor independiente usan `noindex, follow`.
- [ ] Fechas declaradas son reales y trazables.
- [ ] JSON-LD no atribuye cargos, licencias, cobertura o entidades inexistentes.
- [ ] La imagen Open Graph existe y conserva 1200 × 630 px.
- [ ] Los enlaces visibles permiten llegar a todas las páginas publicadas.
- [ ] `npm run validate` termina correctamente.

## Comprobación de salida

- [ ] Cada página indexable tiene una canonical absoluta y autorreferente.
- [ ] `og:url` coincide con canonical.
- [ ] `sitemap-index.xml` y `sitemap-0.xml` usan el host canónico.
- [ ] El sitemap excluye 404 y `/buscar/`.
- [ ] `robots.txt` permite rastreo y enlaza el sitemap.
- [ ] `site-index.json` y `llms.txt` usan las mismas URLs.
- [ ] No aparecen `localhost`, el host antiguo ni dominios futuros.
- [ ] La imagen social y los recursos internos responden.

## Consolas de buscadores

- [ ] El archivo real de verificación de Google permanece en la raíz.
- [ ] Search Console muestra la propiedad de prefijo correcta.
- [ ] Bing está verificado o importado desde Google.
- [ ] El sitemap fue enviado en ambas consolas.
- [ ] IndexNow solo se ejecuta con una clave real publicada.
