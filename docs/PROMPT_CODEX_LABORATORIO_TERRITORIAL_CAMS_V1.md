# PROMPT MAESTRO PARA CODEX
# LABORATORIO TERRITORIAL CAMS — IMPLEMENTACIÓN COMPLETA V1

Trabaje directamente sobre el repositorio Astro abierto en VS Code y en la rama actual `laboratorio-territorial-v1`.

## Mandato

Implemente una primera versión completa, funcional, verificable y publicable del **Laboratorio Territorial CAMS** dentro del sitio Astro existente. No entregue solo una maqueta, diagnóstico o plan. Edite el repositorio, instale dependencias, construya la página, cree la infraestructura de datos, descargue y procese fuentes oficiales cuando exista acceso estable, genere los archivos públicos, implemente mapa y comparadores, añada metodología, trazabilidad, pruebas y validación.

No haga `git commit`, `git merge` ni `git push`. No migre a otro framework. No elimine contenido existente ni rompa rutas. Mantenga la jerarquía `Carlos Arturo Martínez Sánchez → CAMS → Estado que Cumple / Observatorio / Laboratorio Territorial`.

## Lectura previa obligatoria

Inspeccione `README.md`, `package.json`, `astro.config.mjs`, `src/layouts/`, `src/components/global/`, `src/components/brand/`, `src/pages/observatorio/`, `src/pages/estado-que-cumple/`, `src/styles/global.css`, `src/scripts/`, `public/assets/`, `.github/workflows/` y los scripts de auditoría actuales.

## Ruta e integración

Cree:

- `/observatorio/laboratorio-territorial/`

Añada accesos desde:

- `/observatorio/`
- `/estado-que-cumple/`
- `/estado-que-cumple/aplicaciones/`

Título: `Laboratorio Territorial CAMS`.

Subtítulo: `Compare cómo cambiarían la administración, las competencias, la planeación y los recursos bajo distintos escenarios de organización territorial.`

Aviso visible: `Herramienta exploratoria y no oficial. Distingue datos observados, resultados calculados e hipótesis. No constituye una predicción, concepto jurídico ni propuesta territorial definitiva.`

## Modos

Implemente tres modos:

1. **RAÍCES — Ver el Estado actual**
2. **SAVIA — Evaluar capacidad y escala**
3. **SEMILLAS — Comparar escenarios y pilotos**

## Escenarios V1

### 0. Colombia actual

Línea base con departamentos, municipios/distritos, DIVIPOLA y capas de población, tipologías territoriales, desempeño fiscal, desempeño municipal si existe una fuente oficial válida, proyectos SGR y contratación pública agregada.

### 1. Estado unitario regional — escenario exploratorio

Agrupe municipios en 8–12 regiones mediante archivos declarativos. Muestre población agregada, número de municipios, capacidad fiscal disponible, capital o nodo propuesto claramente identificado como supuesto, riesgos, costo de transición cualitativo, requisitos jurídicos y nivel de incertidumbre. No afirme ahorros exactos.

### 2. Municipios conservados con servicios compartidos

Mantenga límites municipales y simule administración compartida para catastro, contratación especializada, defensa jurídica, agua y saneamiento, infraestructura, gestión tributaria y sistemas de información. Implemente al menos una agrupación demostrativa por territorio y una estructura extensible.

## Territorios demostrativos

Incluya:

- Bogotá–Sabana
- Pacífico Medio
- una subregión de municipios pequeños seleccionada con criterios documentados

No invente cifras. Use `Sin dato disponible` cuando corresponda.

## Tecnología

Use **MapLibre GL JS** integrado en Astro. No use React ni Next.js. Instale solo dependencias necesarias:

- `maplibre-gl`
- `zod`
- módulos específicos de Turf cuando sean necesarios
- `vitest`
- `@playwright/test` si encaja sin romper el proyecto

No cargue MapLibre ni los datos del laboratorio en otras páginas.

## Arquitectura sugerida

```text
src/
├── components/territorial/
│   ├── TerritorialLab.astro
│   ├── ModeSelector.astro
│   ├── ScenarioSelector.astro
│   ├── TerritorySelector.astro
│   ├── MetricSelector.astro
│   ├── LayerControl.astro
│   ├── TerritoryMap.astro
│   ├── TerritoryProfile.astro
│   ├── ResultsPanel.astro
│   ├── ComparisonPanel.astro
│   ├── MethodologyDrawer.astro
│   ├── SourcesPanel.astro
│   ├── DataStatus.astro
│   ├── UncertaintyNotice.astro
│   ├── AccessibleDataTable.astro
│   └── DownloadPanel.astro
├── data/territorial/
├── scripts/territorial/
├── workers/territorial.worker.ts
└── pages/observatorio/laboratorio-territorial/index.astro
```

Use Web Worker para agregaciones pesadas.

## Interfaz

En escritorio: configuración a la izquierda, mapa al centro y resultados a la derecha; metodología y descargas debajo. En móvil use pestañas accesibles.

Incluya:

- parámetros URL compartibles: `mode`, `scenario`, `territory`, `metric`, `year`;
- estados de carga/error/reintento;
- leyenda;
- tooltip seguro;
- ficha territorial;
- zoom a departamentos/municipios;
- tabla alternativa completa;
- descargas;
- impresión;
- teclado y `prefers-reduced-motion`.

Mantenga el branding CAMS y una estética de atlas institucional público, no de tablero SaaS.

## Fuentes oficiales iniciales

Cree `data/sources.yml` o un registro tipado. Cada fuente debe incluir entidad, URL, tipo de acceso, frecuencia, fecha del dato, fecha de descarga, cobertura, llave, licencia/condición, transformaciones, limitaciones, estado y hash.

### DANE — cartografía DIVIPOLA MGN 2025

Servicio:

`https://geoportal.dane.gov.co/mparcgis/rest/services/Divipola/Serv_DIVIPOLA_MGN_2025/FeatureServer`

Cree adaptador ArcGIS REST: consulte metadatos, identifique IDs reales, use `query`, `outFields=*`, reproyecte a EPSG:4326, pagine, valide geometrías y conserve códigos DIVIPOLA.

Salida:

```text
public/data/territorial/geography/
├── departments.geojson
├── municipalities-index.json
├── municipalities/05.geojson ...
├── municipality-centroids.json
└── geography-manifest.json
```

Divida municipios por departamento y simplifique para web registrando método y tolerancia. No almacene shapefiles brutos.

### DANE — población

Use proyecciones municipales oficiales basadas en CNPV 2018, series 2018–2042. Normalice por DIVIPOLA, conserve año y área cuando sea viable y genere archivos agregados livianos.

### DNP — tipologías 2026

Use la base oficial y diccionario. Registre 7 tipologías municipales/distritales y 3 departamentales, y la advertencia de que no reemplazan categorías legales ni asignan recursos. Si no hay URL estable, implemente importación manual documentada; no haga scraping frágil.

### DNP — desempeño fiscal

Use resultados oficiales del IDF territorial, inicialmente vigencia 2024 salvo que encuentre una posterior publicada oficialmente. Distinga fecha de publicación y vigencia.

### DNP — desempeño municipal

Use la fuente oficial más reciente y metodológicamente válida. No use copias comunitarias si existe descarga oficial.

### DNP — proyectos SGR

Dataset `mzgh-shtp`:

`https://www.datos.gov.co/resource/mzgh-shtp.json`

Agregue entidad ejecutora, territorio, valor, sector, estado, ejecución física/financiera y enfoques cuando existan. Muestre fecha real del dato.

### Colombia Compra Eficiente — SECOP II

Datasets:

- procesos `p6dx-8zbt`
- contratos `jbjy-vk9h`
- ubicaciones de ejecución `gra4-pcp2`
- ejecución `mfmm-jqmq`

No descargue millones de filas al navegador. Use consultas SoQL agregadas por municipio, departamento, año y sector. Distinga municipio de entidad contratante y municipio de ejecución. Use paginación, reintentos, límites y caché.

### DNP — SisPT / TerriData

Integre solo descargas estables y documentadas. No automatice Power BI ni scraping visual.

### IGAC / IDEAM

Prepare registro y adaptadores. Para V1 incorpore como máximo una capa ambiental liviana si existe acceso estable. No cargue raster nacionales pesados.

## Pipeline Python

Cree:

```text
scripts/territorial/
├── fetch_all.py
├── fetch_dane_geography.py
├── fetch_dane_population.py
├── fetch_dnp_typologies.py
├── fetch_dnp_fiscal.py
├── fetch_dnp_mdm.py
├── fetch_sgr.py
├── fetch_secop.py
├── normalize_divipola.py
├── validate_sources.py
├── build_geography.py
├── build_indicators.py
├── build_scenarios.py
└── build_manifest.py
```

Además:

- `requirements-data.txt`
- `data/manual/README.md`
- `data/crosswalks/divipola-exceptions.csv`
- `data/schemas/`
- `data/cache/` ignorado por Git
- `public/data/territorial/` como salida

Dependencias sugeridas: `requests`, `pandas`, `geopandas`, `pyogrio`, `shapely`, `pyproj`, `pydantic`, `pyyaml`, `tenacity`, `openpyxl`.

El pipeline debe descargar, guardar metadatos, calcular hashes, validar columnas, normalizar DIVIPOLA, registrar rechazos, detectar duplicados, validar rangos, simplificar geometrías, producir archivos públicos y generar informe de calidad. No impute valores silenciosamente.

## Contrato de datos

Use DIVIPOLA como llave. Toda variable debe distinguir:

- `observed`
- `calculated`
- `assumption`

Toda visualización debe mostrar el tipo, año, fuente y fecha de corte.

## Escenarios declarativos

Cree archivos de datos separados para `current`, `regional-exploratory` y `shared-services`. Cada escenario debe incluir versión, autoría, estado, objetivo, unidades, asignación territorial, autoridades, competencias, financiación, planeación, supuestos, riesgos, requisitos jurídicos, incertidumbre, fuentes e historial. No codifique agrupaciones dentro de componentes.

## Cálculos permitidos

Implemente población agregada, número de municipios, población promedio, concentración, sumas fiscales disponibles, dependencia ponderada, cantidad/valor de SGR, contratación agregada, cobertura y porcentaje sin dato.

No calcule ahorros exactos, crecimiento futuro, reducción de corrupción, efectos causales ni mejoras exactas de capacidad.

## Metodología

Cada escenario debe tener `¿Cómo se construyó este escenario?` con objetivo, criterios, variables, fuentes, fecha, supuestos, limitaciones, incertidumbre, decisiones jurídicas, alternativas, historial y archivos descargables.

Añada glosario y distinción entre territorio, región, distrito funcional, capacidad, escala, autonomía, coordinación, dato, cálculo e hipótesis.

## Descargas

Permita descargar CSV de vista, JSON de perfil, GeoJSON visible, ficha metodológica, manifiesto de fuentes y configuración del escenario. No exponga datos brutos masivos.

## GitHub Actions

Cree `.github/workflows/refresh-territorial-data.yml` con `workflow_dispatch` y `schedule` fuera de la hora en punto. Debe descargar, procesar, validar, generar artefactos y un informe. No fusione automáticamente con `main`; actualice una rama `data-refresh` o deje artefacto para revisión manual. Use permisos mínimos. Mantenga separado el despliegue.

## Rendimiento

GitHub Pages no debe recibir bases masivas. Cargue municipios por departamento, capas bajo demanda, caché, agregados SECOP, sin shapefiles/raster brutos. Controle tamaño y registre descargas.

## Accesibilidad y seguridad

El mapa no puede ser la única vía. Añada tabla, buscador territorial, foco, ARIA, patrones además de color, contraste AA, teclado y reducción de movimiento. No inserte HTML no confiable; use `textContent`, Zod, URLs declaradas, sin secretos ni datos personales.

## Pruebas

Añada pruebas unitarias para agregaciones, tipos de resultado, escenarios, cobertura, DIVIPOLA y parámetros URL. Añada pruebas de interfaz para cargar página, cambiar modo/escenario, seleccionar territorio, mostrar fuentes, abrir metodología y descargar.

Cree scripts:

- `npm run data:refresh`
- `npm run data:validate`
- `npm run lab:test`
- `npm run lab:audit`
- integre todo en `npm run validate`

Amplíe auditoría para verificar ruta, assets, datos, manifest, enlaces, metadatos, JSON válido, DIVIPOLA de cinco caracteres, fechas, fuentes, tamaños, ausencia de `NaN`, `Infinity` y cifras simuladas.

## Fallos de fuentes

Estados permitidos: `current`, `stale`, `partial`, `manual-required`, `unavailable`. El sitio debe seguir funcionando con la última versión válida. Muestre la fecha real del dato. Si una fuente no se automatiza, documente importación manual y no la sustituya por datos inventados.

## README

Documente propósito, arquitectura, fuentes, instalación, Python, actualización, validación, Actions, cómo agregar variables/escenarios/territorios, metodología, límites, privacidad y licencias.

## Terminación

No termine hasta que:

1. exista la ruta;
2. el mapa cargue;
3. DANE DIVIPOLA se procese;
4. exista población oficial;
5. exista fuente fiscal/capacidad;
6. exista SGR agregado;
7. exista SECOP agregado;
8. funcionen tres escenarios;
9. funcionen tres territorios;
10. se distingan datos/cálculos/hipótesis;
11. se muestren fuentes/fechas;
12. funcionen descargas y tabla;
13. exista metodología y workflow;
14. existan pruebas;
15. `npm run validate` termine bien;
16. no haya enlaces rotos ni cifras inventadas.

## Informe final

Entregue resumen, árbol de archivos, dependencias, fuentes conectadas, fuentes manuales, fechas, archivos y tamaños, escenarios, resultados de pruebas, salida exacta de `data:validate`, `lab:test`, `build`, `audit` y `validate`, advertencias metodológicas y comandos para revisión, commit, push, merge y publicación.

No haga commit ni push.
