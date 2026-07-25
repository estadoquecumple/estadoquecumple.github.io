# Estado que Cumple

Sitio público de Estado que Cumple, con CAMS como nombre alternativo e identidad editorial de Carlos Arturo Martínez Sánchez. El repositorio público es `estadoquecumple/estadoquecumple.github.io`.

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

`astro.config.mjs` usa salida estática, sitio canónico `https://estadoquecumple.github.io` y sitemap. `.github/workflows/deploy.yml` ejecuta comprobación, compila con la acción oficial de Astro y despliega GitHub Pages al actualizar `main`.

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
