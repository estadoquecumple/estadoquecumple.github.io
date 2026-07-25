# CAMS v7 — Matriz de rutas y recursos

## Criterio de sustitución

La web HTML de la raíz sigue siendo la publicación vigente. La compilación `dist/` de Astro es únicamente una salida de prueba y no puede sustituir el sitio anterior hasta que todas las filas obligatorias estén generadas, sus recursos estén en `public/`, el auditor no informe errores y el workflow continúe desactivado hasta la autorización final.

Estados: **temporal** (infraestructura, no contenido final), **pendiente** (sin página Astro), **compatibilidad pendiente** (ruta antigua que debe conservarse), **recurso incorporado** (copia selectiva disponible en `public/` y `dist/`).

## Matriz exacta

| URL pública actual o futura | Archivo HTML/recurso actual | Futura página Astro | Estado | Recursos utilizados | JavaScript utilizado | JSON utilizado | Canonical | Prioridad | Riesgo | Prueba requerida |
|---|---|---|---|---|---|---|---|---|---|---|
| `/` | `index.html` | `src/pages/index.astro` | Temporal | `styles.css`, favicon, logo, sello, PDF | `script.js`; menú, buscador, portada, participación, microinteracciones | `documents.json`, `state-of-art.json` (buscador) | `https://estadoquecumple.github.io/` | Crítica | Sustituir portada pública por la temporal | Comparación de contenido, teclado, 320 px, enlaces y metadatos |
| `/cams/` | `cams/index.html` | `src/pages/cams/index.astro` | Pendiente | estilos, favicon, logo, sello, OG, manifest | `script.js`; menú, buscador, participación, microinteracciones | `documents.json`, `state-of-art.json` | `https://estadoquecumple.github.io/cams/` | Alta | Pérdida del perfil y trayectoria | Contenido, JSON-LD Person, redes, responsive |
| `/estado-que-cumple/` | `estado-que-cumple/index.html` | `src/pages/estado-que-cumple/index.astro` | Pendiente | estilos, favicon, logo, OG, manifest, PDF | `script.js`; menú, buscador, modos, árbol, núcleo, estado del arte, mapa, simulador, expediente, participación, microinteracciones | `problem-tree.json`, `proposal-architecture.json`, `state-of-art.json`, `activation-routes.json`, `documents.json` | `https://estadoquecumple.github.io/estado-que-cumple/` | Crítica | Pérdida del núcleo conceptual y herramientas | Contenido sin JS, herramientas, anchors, PDF, teclado |
| `/documentos/` | `documentos/index.html` | `src/pages/documentos/index.astro` | Compatibilidad pendiente | estilos, favicon, logo, OG, manifest, PDF | `script.js`; menú, buscador, biblioteca, participación, microinteracciones | `documents.json`, `state-of-art.json` | `https://estadoquecumple.github.io/documentos/` | Crítica | Romper URL histórica y descargas | Ruta generada, canonical, filtros, PDF, enlace a ruta nueva |
| `/observatorio/` | `observatorio/index.html` | `src/pages/observatorio/index.astro` | Compatibilidad pendiente | estilos, favicon, logo, OG, manifest | `script.js`; menú, buscador, participación, microinteracciones | `documents.json`, `state-of-art.json` | `https://estadoquecumple.github.io/observatorio/` | Alta | Presentar datos inexistentes o romper URL | Contenido metodológico, canonical, ausencia honesta de datos |
| `/bitacora/` | `bitacora/index.html` | `src/pages/bitacora/index.astro` | Compatibilidad pendiente | estilos, favicon, logo, OG, manifest | `script.js`; menú, buscador, participación, microinteracciones | `documents.json`, `state-of-art.json` | `https://estadoquecumple.github.io/bitacora/` | Alta | Romper catálogo y URLs futuras | Contenido, canonical, estados editoriales |
| `/participar/` | `participar/index.html` | `src/pages/participar/index.astro` | Pendiente | estilos, favicon, logo, OG, manifest | `script.js`; menú, buscador, participación, microinteracciones | `documents.json`, `state-of-art.json` | `https://estadoquecumple.github.io/participar/` | Alta | Inventar canales o perder límites | Enlaces reales, teclado, canonical, sin formulario ficticio |
| `/archivo/` | `archivo/index.html` | `src/pages/archivo/index.astro` | Compatibilidad pendiente | estilos, favicon, logo, sello, OG, manifest, PDF | `script.js`; menú, buscador, participación, microinteracciones | `documents.json`, `state-of-art.json` | `https://estadoquecumple.github.io/archivo/` | Alta | Romper trazabilidad pública | Repositorios, versiones, PDF, canonical |
| `/assets/documentos/estado-que-cumple-2026-2030.pdf` | `assets/documentos/estado-que-cumple-2026-2030.pdf` | `public/assets/documentos/estado-que-cumple-2026-2030.pdf` | Recurso incorporado | PDF descargable | Ninguno | Ninguno | No aplica | Crítica | Regresión o copia truncada | Existencia, tamaño razonable y enlace desde páginas |
| `/propuestas/` | No existe | `src/pages/propuestas/index.astro` | Pendiente | Por definir con contenido real | Filtros futuros | Colección `proposals` futura | `https://estadoquecumple.github.io/propuestas/` | Alta | Navegación apunta a ruta inexistente | Ruta, contenido real, filtros sin JS |
| `/conocimiento/` | No existe | `src/pages/conocimiento/index.astro` | Pendiente | Por inventariar desde secciones heredadas | Buscador futuro | Colecciones futuras | `https://estadoquecumple.github.io/conocimiento/` | Alta | Menú principal apunta a ruta inexistente | Ruta, índice funcional, teclado |
| `/conocimiento/investigaciones/` | No existe | `src/pages/conocimiento/investigaciones/index.astro` | Pendiente | Solo fuentes confirmadas | Por definir | Colección `research` futura | `https://estadoquecumple.github.io/conocimiento/investigaciones/` | Media | Inventar investigaciones | Ruta, ausencia honesta o contenido verificado |
| `/conocimiento/documentos/` | `documentos/index.html` como fuente | `src/pages/conocimiento/documentos/index.astro` | Pendiente | Biblioteca, PDF y metadatos | Biblioteca y buscador | `documents.json` | `https://estadoquecumple.github.io/conocimiento/documentos/` | Alta | Duplicidad con `/documentos/` | Índice, canonical decidido, compatibilidad antigua |
| `/conocimiento/bitacora/` | `bitacora/index.html` como fuente | `src/pages/conocimiento/bitacora/index.astro` | Pendiente | Contenido editorial existente | Buscador | Colección `articles` futura | `https://estadoquecumple.github.io/conocimiento/bitacora/` | Alta | Duplicidad y pérdida de estados | Índice, canonical decidido, compatibilidad antigua |
| `/conocimiento/observatorio/` | `observatorio/index.html` como fuente | `src/pages/conocimiento/observatorio/index.astro` | Pendiente | Metodología existente | Por definir | Datos reales futuros | `https://estadoquecumple.github.io/conocimiento/observatorio/` | Alta | Confundir metodología con datos | Índice, canonical decidido, compatibilidad antigua |
| `/conocimiento/archivo/` | `archivo/index.html` como fuente | `src/pages/conocimiento/archivo/index.astro` | Pendiente | Repositorios, versiones, sello, PDF | Buscador | Metadatos futuros | `https://estadoquecumple.github.io/conocimiento/archivo/` | Alta | Duplicidad y pérdida de trazabilidad | Índice, canonical decidido, compatibilidad antigua |

Además, el micrositio futuro requerirá las subrutas `/estado-que-cumple/problema/`, `/metodo/`, `/arquitectura/`, `/implementacion/`, `/aplicaciones/` y `/documento/`; se auditarán al iniciar esa fase, no se crean en la Fase 2.5.

## Inventario de copia selectiva a `public/`

Los originales permanecen intactos. La Fase 2.6 incorporó únicamente los recursos esenciales y los datos que las herramientas actuales solicitan mediante `fetch`.

| Clase | Origen actual | Destino futuro | Uso y condición |
|---|---|---|---|
| Branding | `assets/branding/logo-cams.png`, `emblema-cams.png`, `sello-cams.png` | `public/assets/branding/` | Incorporados sin conversión ni pérdida; conservar nombres y enlaces |
| PDF | `assets/documentos/estado-que-cumple-2026-2030.pdf` | `public/assets/documentos/` | Incorporado; el auditor exige al menos 100 KB y archivo no vacío |
| Favicon | `assets/favicon.svg` | `public/assets/favicon.svg` | Incorporado y referenciado por layout y manifest |
| Imagen Open Graph | `assets/og-cams-v3.png` | `public/assets/og-cams-v3.png` | Incorporada como imagen social predeterminada |
| Manifest | `site.webmanifest` | `public/site.webmanifest` | Incorporado sin iconos ficticios; el único SVG real conserva `sizes: any` |
| JSON | `assets/data/*.json` | `public/assets/data/` | Incorporados temporalmente para mantener las rutas de `fetch`; transición detallada abajo |
| Herramientas interactivas | `script.js`, `assets/js/*.js`, `styles.css`, `assets/css/*.css` | Preferentemente módulos en `src/` | Deliberadamente no incorporados: la portada Astro no los consume y copiarlos duplicaría infraestructura heredada |
| Descargables | PDF actual y futuros archivos confirmados | `public/assets/documentos/` | Inventariar nombre, tamaño, página de origen y enlace público |
| Infraestructura pública | `robots.txt`, `sitemap.xml` | `public/robots.txt`; sitemap generado por Astro | `robots.txt` incorporado apuntando a `sitemap-index.xml`; sitemap antiguo no copiado |

## Estrategia de datos durante la migración

| JSON | Uso actual | Decisión Fase 2.6 | Destino final previsto |
|---|---|---|---|
| `problem-tree.json` | `problem-tree.js` lo solicita con `fetch` | Mantener temporalmente en ambos árboles | Importación tipada desde `src/data/` cuando se migre Problema; retirar copia pública si deja de existir `fetch` |
| `proposal-architecture.json` | `proposal-core.js` e `institutional-map.js` lo solicitan con `fetch` | Mantener temporalmente en ambos árboles | Importación tipada desde `src/data/` para Método y Arquitectura; retirar copia pública tras migrar ambas herramientas |
| `state-of-art.json` | `state-of-art.js` y buscador lo solicitan con `fetch` | Mantener temporalmente en ambos árboles | Fuente tipada en `src/data/`; conservar versión pública solo si el buscador cliente sigue necesitándola |
| `documents.json` | Biblioteca y buscador lo solicitan con `fetch` | Mantener temporalmente en ambos árboles | Migrar a colección o fuente tipada; generar índice cliente derivado si sigue siendo necesario |
| `activation-routes.json` | Simulador normativo lo solicita con `fetch` | Mantener temporalmente en ambos árboles | Importación tipada desde `src/data/` al migrar Implementación; retirar duplicación después |

La duplicación es transitoria y explícita: `assets/data/` sostiene la web HTML vigente y `public/assets/data/` hace autosuficiente la build Astro. No se editarán por separado; hasta la migración tipada, el original es la fuente de verdad.

## Tamaños y optimización pendiente

| Recurso | Tamaño actual |
|---|---:|
| `logo-cams.png` | 379.540 bytes |
| `sello-cams.png` | 890.250 bytes |
| `emblema-cams.png` | 855.167 bytes |
| `og-cams-v3.png` | 38.291 bytes |
| `estado-que-cumple-2026-2030.pdf` | 5.057.879 bytes |

No se comprimieron ni convirtieron archivos. En una fase posterior se deben medir variantes WebP/AVIF del branding contra los PNG originales, conservando estos como respaldo; también queda pendiente decidir si la imagen Open Graph existente será la definitiva. El favicon solo existe como SVG escalable: antes de declarar tamaños raster en el manifest deberán crearse y validarse archivos reales.

## Puerta de publicación

Astro no está listo para producción mientras exista cualquier `ERROR` de `node tools/audit_dist.mjs`. El archivo `.github/disabled/deploy-pages.yml.disabled` debe permanecer fuera de `.github/workflows/` hasta que la matriz esté completa y se autorice explícitamente la fase final.

Tras la Fase 2.6, la auditoría baja de 31 a 24 errores: ya no hay errores de recursos públicos ni metadatos; persisten 14 páginas obligatorias ausentes y 10 enlaces internos hacia esas rutas no generadas.
