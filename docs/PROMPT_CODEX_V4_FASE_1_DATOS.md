# PROMPT CODEX — LABORATORIO TERRITORIAL V4
# FASE 1: BANCO REPRODUCIBLE, DATOS REALES Y MOTOR ANALÍTICO ESTÁTICO

Trabaje en:

`C:\Users\Usuario\GitHub\estadoquecumple.github.io`

## Estado y Git

1. Ejecute `git fetch origin --prune`.
2. Cambie a `main`.
3. Ejecute `git pull --ff-only origin main`.
4. Compruebe árbol limpio.
5. Cree:

`laboratorio-territorial-v4-datos`

No use pull request.
No use la interfaz web.
No use force push.
No fusione en `main` hasta completar todas las pruebas.
No elimine funcionalidad V3.

## Objetivo

Implementar la Fundación V4 sin backend obligatorio:

- banco de datos versionado;
- catálogo de fuentes;
- DANE con tipo territorial;
- SECOP y SGR agregados reales;
- Parquet/GeoParquet;
- DuckDB-Wasm;
- H3;
- geometría Turf;
- cápsula reproducible;
- compilador de escenarios;
- evidencia y gráficos.

## Instalación npm

Ejecute:

```powershell
npm install `
  @duckdb/duckdb-wasm `
  apache-arrow `
  h3-js `
  pmtiles `
  @observablehq/plot `
  @turf/union `
  @turf/difference `
  @turf/intersect `
  @turf/boolean-valid `
  @turf/boolean-intersects `
  @turf/boolean-overlap `
  @turf/boolean-touches `
  @turf/clean-coords `
  @turf/unkink-polygon `
  @turf/helpers
```

Use imports modulares y carga diferida. No incremente innecesariamente el bundle inicial.

## Instalación Python

Cree `.venv` si no existe y agregue `requirements-platform-core.txt`.

Instale:

```text
duckdb
pyarrow
h3
pandera[pandas]
networkx
rapidfuzz
pytest
ruff
```

Conserve `requirements-data.txt` para compatibilidad y haga que el workflow instale ambos.

## Tarea 1 — Bóveda y snapshots

Cree:

```text
data/catalog
data/schemas
data/snapshots
data/registry
data/rules
public/data/territorial/catalog
public/data/territorial/current
public/data/territorial/history
public/data/territorial/analytics
```

Implemente:

- SHA-256;
- ID de snapshot;
- manifiesto;
- archivo original;
- producto normalizado;
- resultado de calidad;
- puntero `current`;
- retención de última versión válida.

Nunca reemplace el original.

## Tarea 2 — Catálogo de fuentes

Amplíe `data/sources.yml` y cree esquema Pydantic/JSON Schema.

Debe validar:

- ID;
- entidad;
- URL;
- acceso;
- frecuencia;
- fechas;
- cobertura;
- granularidad;
- clave;
- licencia;
- campos;
- transformaciones;
- limitaciones;
- hash;
- snapshot;
- calidad;
- estado.

Genere un catálogo JSON público y una vista en RAÍCES.

## Tarea 3 — DANE

Modifique `fetch_dane_geography.py`.

Conserve:

- MPIO_TIPO;
- MPIO_NAREA;
- MPIO_NANO;
- MPIO_CRSLCION;
- códigos y nombres originales.

Genere:

- conteo por tipo;
- `territorial-unit-types.json`;
- geometría oficial sin simplificación destructiva para procesamiento;
- geometría web simplificada;
- punto representativo geométrico;
- pruebas de clasificación.

No llame municipios a todas las 1.122 unidades.

## Tarea 4 — SECOP

Reemplace conteos por agregados territoriales.

Use SoQL y paginación.

Separe:

- entidad contratante;
- lugar de ejecución;
- proveedor.

Agregue por:

- año;
- territorio;
- sector;
- modalidad;
- estado;
- UNSPSC;
- valor;
- contratos;
- proveedores;
- modificaciones.

Use `SOCRATA_APP_TOKEN` cuando exista.

No exponga el token.

No descargue 5,64 millones de filas al navegador.

## Tarea 5 — SGR

Elimine la muestra fija de 5.000.

Use paginación completa o SoQL agregado.

Publique:

- BPIN;
- estado;
- valor;
- sector;
- ejecutor;
- código territorial;
- conteos;
- sumas;
- cobertura;
- calidad.

No extrapole datos.

## Tarea 6 — DNP

Cree adaptadores para:

- Tipologías 2026;
- IDF 2024;
- MDM con vigencia explícita.

Solo fuentes oficiales.

Descubra y archive los archivos descargables. Si no hay URL estable, conserve importación manual reproducible con hash y plantilla.

No automatice Power BI mediante scraping visual.

## Tarea 7 — Parquet y GeoParquet

Produzca:

- catálogo;
- indicadores;
- entidades;
- geometrías analíticas;
- series;
- SECOP agregado;
- SGR agregado.

Valide GeoParquet.

Conserve JSON pequeño como fallback.

## Tarea 8 — DuckDB-Wasm

Implemente un servicio analítico en Web Worker:

- inicialización diferida;
- consulta Parquet;
- timeout;
- cancelación;
- límite de memoria;
- error visible;
- fallback JSON;
- prueba escritorio y móvil.

No cargue datos analíticos en la portada inicial.

## Tarea 9 — H3

Implemente una capa H3 optativa:

- resolución seleccionable;
- metadatos;
- asociación con DIVIPOLA;
- agregados;
- advertencia de que no es división legal.

## Tarea 10 — Geometría real

Reemplace la unión MultiPolygon nominal con Turf union.

Implemente:

- unión;
- diferencia;
- intersección;
- validación;
- limpieza;
- solapes;
- contactos.

Cuando la operación exceda umbral, no bloquee el navegador: indíquela como operación de backend requerida.

## Tarea 11 — Cápsula reproducible

Cree esquema V4:

- runId;
- commit;
- versiones;
- hashes;
- reglas;
- modelos;
- supuestos;
- restricciones;
- semilla;
- entradas;
- salidas;
- validaciones.

Inclúyala en exportación e importación.

## Tarea 12 — Compilador

Implemente validadores de:

- jerarquía;
- geometría;
- cobertura;
- duplicados;
- competencias;
- financiación;
- autoridad;
- control;
- ruta jurídica;
- transición.

Muestre estado de compilación y errores accionables.

## Tarea 13 — Interfaz

Agregar:

- catálogo;
- evidencia pulsable;
- fecha/vigencia;
- gráfico vinculado;
- historial;
- comparación;
- modo guiado;
- modo experto;
- expediente JSON/CSV y borrador de informe.

## Tarea 14 — Workflows

Actualice `refresh-territorial-data.yml`:

- instalar `requirements-data.txt` y `requirements-platform-core-free.txt`;
- usar secretos opcionales;
- generar snapshot;
- validar;
- comparar;
- no promover si falla;
- publicar artefactos;
- conservar última versión válida.

No hacer auto-commit a `main` en esta fase.

## Pruebas

Añada:

- snapshots;
- hashes;
- esquemas;
- DANE tipos;
- SECOP agregados;
- SGR cobertura;
- Parquet;
- GeoParquet;
- DuckDB;
- H3;
- Turf;
- compilador;
- cápsula;
- evidencia;
- errores;
- móvil.

Ejecute:

```powershell
npm run data:refresh
npm run validate
npm run lab:e2e
git diff --check
```

Si una fuente externa falla, use fixture y conserve el fallo visible. No invente datos.

## Commit e integración

Cuando todo esté verde:

```powershell
git add -A
git commit -m "Implementar fundación de datos y análisis del Laboratorio Territorial V4"
git fetch origin --prune
git merge --no-ff origin/main -m "Integrar main antes de publicar fundación V4"
npm run validate
npm run lab:e2e
```

Luego:

```powershell
git switch main
git pull --ff-only origin main
git merge --no-ff laboratorio-territorial-v4-datos -m "Publicar fundación de datos del Laboratorio Territorial V4"
npm run validate
npm run lab:e2e
git push origin main
```

No use force push.

## Informe

Genere:

`reports/laboratorio-v4-fase1-final.md`

Incluya:

- dependencias;
- datos;
- fuentes;
- snapshots;
- calidad;
- rendimiento;
- pruebas;
- hashes;
- limitaciones.
