# Laboratorio Territorial V4 — cierre de Fase 1

Fecha de verificación: 2026-07-26 (America/Bogota)

## Resultado

La Fase 1 queda implementada sobre una arquitectura local, gratuita, de código
abierto y autoalojable. La aplicación no utiliza OpenAI API ni servicios con
tarjeta, suscripción o pago por consumo. Los proveedores de LLM y embeddings
permanecen configurados en `none`.

## Entorno y dependencias

- Entorno conservado: `.venv`, Python 3.12.10.
- Importaciones verificadas: DuckDB, PyArrow, H3, Great Expectations,
  NetworkX, RapidFuzz y Pandera.
- Pandera reemplaza a Great Expectations en el código y los requisitos de la
  plataforma después de implementar y aprobar las validaciones equivalentes.
- Great Expectations no fue desinstalado del entorno existente.
- `requirements-platform-core.txt` coincide con
  `requirements-platform-core-free.txt`.
- No se instalaron Docker, PostGIS, SeaweedFS, Valhalla, OSRM,
  OpenTripPlanner, Ollama, modelos locales, embeddings, MLflow ni ONNX. Sus
  usos previstos permanecen documentados para fases posteriores.

## Datos, catálogo y trazabilidad

- Catálogo validado con Pydantic, Pandera y JSON Schema; registra fuente
  oficial, licencia, cobertura, granularidad, periodicidad, transformación,
  limitaciones, estado, calidad y política de actualización.
- Snapshots inmutables con originales preservados, productos normalizados,
  SHA-256, manifiesto, resultados de calidad, puntero `current` e historial.
- Una actualización defectuosa no promociona ni sustituye la última versión
  válida.
- DANE: 1.122 unidades territoriales con los campos oficiales `MPIO_TIPO`,
  `MPIO_NAREA`, `MPIO_NANO` y `MPIO_CRSLCION`: 1.103 municipios, 18 áreas no
  municipalizadas y 1 isla. Los puntos se calculan con geometría
  representativa, no con promedio de vértices.
- SGR: descarga completa de 35.006 filas; 33.252 BPIN únicos y 1.754
  duplicados identificados. El snapshot vigente está marcado completo.
- SECOP II: agregaciones oficiales por territorio contratante, entidad,
  sector, modalidad, estado, proveedor y UNSPSC; 25.147 filas agregadas y
  5.876.030 registros contabilizados en dimensiones completas. El resultado
  se publica explícitamente como parcial por los topes de entidad/proveedor y
  la indisponibilidad temporal de la dimensión anual.
- DNP: adaptadores para descubrir descargas públicas oficiales en formatos
  abiertos. Tipologías, IDF y MDM quedan en `manual-required` mientras no
  exista un original oficial conservado; no se fabrican datos ni snapshots.

## Productos técnicos

- Parquet de catálogo e indicadores.
- GeoParquet de departamentos con CRS.
- Índice H3/DIVIPOLA en Parquet y respaldo JSON para el navegador.
- DuckDB-Wasm autocontenido y cargado de forma diferida, sin CDN, con tiempo
  máximo, cancelación, límite de bytes y respaldo JSON.
- Operaciones Turf reales para unión, diferencia, intersección, limpieza,
  validación, solapamiento, contacto y separación de geometrías; las
  operaciones grandes se derivan explícitamente al backend futuro.
- Compilador de escenarios con validaciones territoriales, financieras,
  jurídicas, de gobernanza y transición.
- Cápsula reproducible con hashes de datos, commit base, reglas, supuestos,
  restricciones, semilla, entradas, salidas, validaciones y proveedores.
- Selector guiado/experto, catálogo público consultable, exportación e
  importación de escenarios V4 y capa H3 marcada como analítica, no jurídica.

## Huellas de los productos analíticos

| Producto | Bytes | SHA-256 |
|---|---:|---|
| `catalog.parquet` | 18.029 | `d57a83b3f5de6a5d29bb23a8c942c375538a15e042033ed240b03401f9a17adf` |
| `indicators.parquet` | 1.631.028 | `14e749b6ae2483065167e2905f718d14d7b9679cd27b2906f24ea49ad7c9d60e` |
| `departments.geoparquet` | 115.485 | `9296dbf9bc72f6021c62b15ce704c444ecd044a388b13ef065ab6c918c4d00cb` |
| `h3-divipola.parquet` | 16.737 | `5a6e1d58e8bdab8695a509f4517e0054e3aaa7c02c0988fa0cb1267dd9e6571e` |

La regla `scenario-compiler-v4` versión 4.0.0 tiene SHA-256
`ae021ff81012a3f504dc7f5de4e73d11a85ac30d52289475c58af7dba93ae0a1`.

## Verificación

- 7 pruebas Python aprobadas.
- Ruff aprobado.
- Validación de catálogo, snapshots, hashes, Parquet, GeoParquet, CRS y H3
  aprobada.
- 48 pruebas Vitest aprobadas.
- Astro Check aprobado sin errores ni advertencias.
- Construcción de producción y auditorías de rutas, SEO, contratos de botones
  y controles funcionales aprobadas.
- 38 ejecuciones Playwright aprobadas en los proyectos configurados.
- `npm run validate`: aprobado.
- `npm run lab:e2e`: aprobado.
- `git diff --check`: aprobado.

## Limitaciones declaradas

- SECOP II no se presenta como descarga contractual exhaustiva en el cliente:
  solo se publican agregados; entidad y proveedor están limitados y la
  dimensión anual requiere una futura actualización cuando el servicio
  oficial responda de forma estable.
- Los productos DNP sin original descargable conservado no se promocionan.
- H3 es una malla analítica y no sustituye límites oficiales.
- El cálculo pesado, el ruteo avanzado, la infraestructura espacial, los
  modelos locales y MLOps pertenecen a fases posteriores y no fueron
  instalados en esta fase.
