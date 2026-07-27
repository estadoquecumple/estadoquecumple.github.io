# Estado que Cumple

Sitio público de Estado que Cumple, con CAMS como nombre alternativo e identidad editorial de Carlos Arturo Martínez Sánchez. El repositorio público es `estadoquecumple/estadoquecumple.github.io`.

URL pública y canónica actual: `https://estadoquecumple.github.io/`.

## Requisitos y uso local

- Node.js 22 LTS o compatible.
- Instalar: `npm ci`
- Desarrollo: `npm run dev`
- Comprobación Astro/TypeScript: `npm run check`
- Compilación estática: `npm run build`
- Auditoría de `dist/`: `npm run audit`
- Validación completa: `npm run validate`

## Estructura editorial

- `src/pages/`: rutas públicas; Astro genera HTML estático.
- `src/layouts/` y `src/components/global/`: estructura, SEO, navegación y piezas editoriales reutilizables.
- `src/components/tools/`: interacciones cargadas únicamente en el capítulo correspondiente.
- `src/data/`: navegación e índice de búsqueda como fuentes únicas tipadas.
- `public/assets/`: imágenes, PDF y JSON públicos usados por herramientas.
- `.github/ISSUE_TEMPLATE/`: correcciones, fuentes y colaboraciones públicas.
- `tools/audit-dist.mjs`: auditoría posterior al build.

## Agregar contenido

### Propuestas

Cree una ruta o fuente tipada solo cuando exista ficha con problema, tesis, evidencia, alternativas, ruta institucional, instrumentos, condiciones, riesgos, versión, fecha y uno de estos estados: idea registrada, investigación, borrador, propuesta pública, piloto o archivada. Agregue la ruta a `src/data/site.ts`.

### Documentos

Publique el archivo una sola vez en `public/assets/documentos/`, cree una ficha en `src/pages/documentos/` e informe autoría, resumen, versión, fecha, tamaño, extensión, citación, historial, licencia y huella cuando proceda.

### Artículos

No anuncie una entrada como publicada hasta que exista el texto completo, fuentes y metadatos. Cuando haya al menos una entrada real puede crearse una colección de contenido y RSS; el sitio no genera un feed vacío.

## Despliegue

`astro.config.mjs` usa salida estática, `SITE_URL` como fuente del dominio y la integración oficial de sitemap. Si no se define la variable, el valor seguro es `https://estadoquecumple.github.io`. No se usa `base`.

Comandos principales:

```text
npm install
npm run dev
npm run check
npm run build
npm run audit
npm run seo:audit
npm run seo:report
npm run validate
```

`reports/seo-report.json` registra páginas indexables, páginas `noindex`, canonical, JSON-LD y errores encontrados. La búsqueda interna y 404 son las únicas salidas `noindex`.

La preparación de Google Search Console, Bing e IndexNow está en [docs/INDEXACION.md](docs/INDEXACION.md). La lista operativa para migrar en el futuro, sin elegir todavía entre los dos dominios considerados, está en [docs/MIGRACION_DOMINIO.md](docs/MIGRACION_DOMINIO.md). El control editorial previo a cada publicación está en [docs/SEO_CHECKLIST.md](docs/SEO_CHECKLIST.md).

Para cambiar de dominio no se editan componentes: se configura `SITE_URL`, se ajustan GitHub Pages y DNS, y se vuelven a verificar los buscadores. Canonical, sitemap, robots, Open Graph, JSON-LD, `site-index.json` y `llms.txt` se regeneran desde esa fuente.

`.github/workflows/deploy.yml` compila y despliega GitHub Pages al actualizar `main`. `.github/workflows/indexnow.yml` es manual, se ejecuta después del despliegue y requiere el secreto real `INDEXNOW_KEY`.

## Laboratorio Territorial CAMS

La ruta `/observatorio/laboratorio-territorial/` es un atlas institucional estático con MapLibre cargado solo allí. Usa DIVIPOLA como llave y separa `observed`, `calculated` y `assumption`. El mapa tiene tabla alternativa, filtro, teclado, parámetros URL, impresión y descargas acotadas.

- `scripts/territorial/`: adaptadores ArcGIS REST, Socrata y manuales; normalización, construcción y calidad.
- `data/sources.yml`, `data/schemas/`, `data/scenarios/`: registro, contratos y escenarios declarativos.
- `public/data/territorial/`: GeoJSON particionado, agregados, configuraciones y manifiesto con hashes.
- `src/components/territorial/`: mapa, comparación, metodología, fuentes, tabla y descargas.
- `tests/territorial/` y `tools/audit-territorial.mjs`: pruebas y auditoría.

Instale Python con `pip install -r requirements-data.txt` y ejecute `npm run data:refresh`. Para conservar la última copia válida sin red use `python scripts/territorial/fetch_all.py --offline`. Las fuentes `manual-required` se importan según `data/manual/README.md`; nunca se imputan faltantes. Valide con `npm run data:validate`, `npm run lab:test` y `npm run validate`.

Para agregar variables declare fuente, esquema, tipo, año y corte, añada un adaptador y pruebe cobertura. Para escenarios o territorios edite `data/scenarios/`, documente supuestos, riesgos, requisitos jurídicos, incertidumbre e historial y regenere; no codifique agrupaciones en componentes.

`refresh-territorial-data.yml` corre manualmente y los martes a las 08:23 UTC, genera un artefacto de revisión y no fusiona ni despliega. No se procesan datos personales ni secretos. La reutilización depende de las condiciones de DANE, DNP y Datos Abiertos Colombia. Los escenarios no predicen, prueban causalidad ni calculan ahorros exactos.

### Límites de conservación y publicación de la Fase 1

Los originales `raw` descargados no están versionados en Git. Los artefactos producidos por GitHub Actions se conservan durante 30 días y sirven para revisión, no como bóveda durable. El workflow de `refresh` valida y empaqueta datos, pero no publica, fusiona ni despliega automáticamente. Una bóveda durable y su operación pertenecen a la Fase 2 y no forman parte de este cierre.

La migración de seguridad actualiza explícitamente Astro 5.18.2 a 7.1.3, junto con `sharp` 0.35.3, `esbuild` 0.28.1, `@astrojs/check` 0.9.9 y `@astrojs/sitemap` 3.7.3. El sitio ya usaba configuración estática compatible; no fue necesario cambiar rutas, colecciones, adaptadores ni APIs de componentes. La única incompatibilidad encontrada fue la retirada del ejecutable interno `astro/astro.js`: el lanzador E2E ahora usa el binario público declarado por Astro en `bin/astro.mjs`.

DuckDB-Wasm queda fijado en la versión estable 1.29.0. La extensión oficial libre de Parquet se sirve desde `public/assets/duckdb/` para que una consulta válida no dependa de `extensions.duckdb.org`; el fallback JSON se reserva para fallos reales y se prueba por separado.
