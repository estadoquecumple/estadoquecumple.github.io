# Informe final — Laboratorio Territorial V4, Fase 1

Fecha de ejecución: 2026-07-27  
Rama de trabajo: `laboratorio-territorial-v4-datos`

## Alcance

Se ejecutó únicamente la Fase 1 estática. Se conservó la funcionalidad V3 y no
se instalaron ni implementaron Docker, PostgreSQL/PostGIS, SeaweedFS, FastAPI,
OR-Tools, MLflow, ONNX, modelos neuronales ni componentes de las fases 2 y 3.

## Dependencias instaladas

- Web: DuckDB-Wasm 1.29.0, Apache Arrow 21.2.0, H3 4.5.0, PMTiles 4.4.1,
  Observable Plot 0.6.17 y módulos Turf 7.3.5.
- Python 3.12.10: DuckDB 1.5.5, PyArrow 22.0.0, H3 4.5.0, Pandera 0.32.1,
  NetworkX 3.6.1, RapidFuzz 3.14.5, pytest 8.4.2, ruff 0.16.0,
  pandas 2.3.3, GeoPandas 1.1.4, Shapely 2.1.2 y Pydantic 2.13.4.
- `npm install`, instalación de `requirements-data.txt` y
  `requirements-platform-core.txt`, `npm ls --depth=0` y `pip check`: correctos.

## Fuentes, cobertura y calidad

| Fuente | Estado | Cobertura comprobada | Control principal |
|---|---:|---:|---|
| DANE DIVIPOLA/MGN 2025 | current | 33 departamentos; 1.122 unidades | 1.103 municipios, 18 áreas no municipalizadas y 1 isla; `MPIO_TIPO`, `MPIO_NAREA`, `MPIO_NANO` y `MPIO_CRSLCION` conservados |
| SECOP II | current | 1.244.978 filas agregadas | 10 dimensiones; entidad y ejecución separadas; sin contratos crudos en navegador |
| SGR | current | 35.006/35.006 filas | 33.252 BPIN únicos; 1.754 duplicados descartados; cobertura 1,0 |
| DNP Tipologías | current | 1.103 municipios + 32 departamentos | vigencia 2026; XLSX oficial archivado |
| DNP IDF | current | 1.103 municipios + 32 departamentos | vigencia real 2024 |
| DNP MDM | current | 1.103 municipios + 32 departamentos | vigencia real 2024 |
| DANE población | manual-required | sin original estable importado | no se inventaron ni promovieron registros |

SECOP conserva conteos por año, territorio de la entidad, entidad, sector,
modalidad, estado, proveedor, UNSPSC, ubicación de ejecución y modificación.
Los totales contractuales por las dimensiones principales son 5.876.030; las
ubicaciones de ejecución suman 6.137.726 registros y las modificaciones
24.995.248 eventos. La procedencia territorial del proveedor no está
estructurada en los conjuntos oficiales consultados y no se infiere.

## Snapshots promovidos

| Fuente | Snapshot | SHA-256 combinado del original |
|---|---|---|
| DANE | `dane-divipola-mgn-2025-fd80363ddd2c754a` | `5751e0404554be2d7928a37824a715d3087706a163e38da322fc0589b2a91832` |
| SGR | `dnp-sgr-mzgh-shtp-cb36ce84588ac238` | `c8255f8852b8a229e71f34799d76b832b6bfc9c09fa3e63c3c8e87a64f32cecd` |
| SECOP | `secop-ii-a602739aa1712d21` | `4e426631bc06549752225194d21a0543fd716e309ded169cc25b3a4d46b7fb51` |
| Tipologías | `dnp-typologies-2026-33cad88b6d05269e` | `6d6b2e17bbb1cb05cb8dfbfbfa45f9992f452f17e97829871b1f240dc77b05aa` |
| IDF | `dnp-idf-2024-4dd54028af0292f4` | `6d6b2e17bbb1cb05cb8dfbfbfa45f9992f452f17e97829871b1f240dc77b05aa` |
| MDM | `dnp-mdm-6a75e689e5f25884` | `6d6b2e17bbb1cb05cb8dfbfbfa45f9992f452f17e97829871b1f240dc77b05aa` |

El original DNP común tiene SHA-256
`20f602065a120fa354dc1d6fdf72e16335eee73b2776e1e09cdb910545ec139e`.
Cada manifiesto marca el snapshot como inmutable. Una actualización incompleta
de SECOP, SGR o DNP escribe evidencia de fallo en caché y conserva la última
versión publicada.

## Productos analíticos

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| `catalog.parquet` | 19.137 | `1f1035496ca2c8165628c4c4b9cc56d36ee69974525def8de5200b6b41c9f3a3` |
| `indicators.parquet` | 1.559.917 | `b81b782cdaf0a99b6f45107cf38de9f6f9c943f4137ea945a23270f65bbb71da` |
| `series.parquet` | 147.135 | `2b7400f9e2bc396f534ed8c28ccf8e9e979d7f1ceaac4bedef4110bf0813690a` |
| `entities.parquet` | 18.037 | `c08b93db0005d3183e19ddbc8f944e9a9a8a81c053e9e4136b98390dcab06bbc` |
| `sgr-aggregates.parquet` | 191.320 | `ce1bda82d1aeb42c885b57a30ea33fcba23909f50f5e450d7a2abae7470b3e77` |
| `secop-aggregates.parquet` | 14.571.215 | `39c9b5ca49f9ba195f3f955f2c3bc8cc9dc008748d68ed542bdf3d34bc5bbd34` |
| `departments.geoparquet` | 115.485 | `9296dbf9bc72f6021c62b15ce704c444ecd044a388b13ef065ab6c918c4d00cb` |
| `h3-divipola.parquet` | 16.737 | `5a6e1d58e8bdab8695a509f4517e0054e3aaa7c02c0988fa0cb1267dd9e6571e` |

DuckDB-Wasm se inicializa de forma diferida en Web Worker y conserva fallback
JSON. El detalle SECOP de alta cardinalidad queda solo en Parquet. H3 es una
capa analítica optativa y no una división legal. Turf realiza unión,
diferencia, intersección, validez, limpieza, solape y contacto; las operaciones
que superan el umbral se marcan como requeridas por backend.

## Compilador y reproducibilidad

La cápsula registra ejecución, commit, contrato, registro legal, datasets,
hashes, reglas, modelos, supuestos, restricciones, semilla, entradas, salidas,
validaciones y advertencias. El compilador bloquea incoherencias de jerarquía,
geometría, cobertura, duplicados, competencias, financiación, autoridad,
control, ruta jurídica y transición.

## Resultados exactos de pruebas

- `npm run data:refresh`: adquisición oficial ejecutada; el primer intento
  Socrata falló por timeout y no fue promovido; el reintento completo terminó
  con SECOP `current`.
- pytest: **10 passed**.
- ruff: **All checks passed**.
- validación de datos: **26 archivos obligatorios verificados**.
- Vitest: **5 archivos, 50 pruebas aprobadas**.
- Astro check: **127 archivos, 0 errores, 0 advertencias, 0 hints**.
- Astro build: **31 páginas**.
- auditoría de distribución: **32 HTML, 31 rutas obligatorias**.
- SEO: **29 indexables, 2 noindex, 0 errores, 0 avisos**.
- auditorías territorial, legal, botones y funcional: aprobadas.
- Playwright: **44 ejecuciones aprobadas** en escritorio y móvil.
- `git diff --check`: sin errores.

## Rendimiento y limitaciones

- `secop-aggregates.parquet` pesa 14.571.215 bytes y activa la advertencia
  informativa de archivo analítico mayor de 8 MB. No se carga en portada; usa
  DuckDB-Wasm diferido y fallback JSON de 5.362.273 bytes.
- La actualización SECOP completa tardó 12 min 47 s sin token Socrata.
- DANE población continúa `manual-required`; no se declara conectada.
- Socrata puede agotar tiempo sin `SOCRATA_APP_TOKEN`; el token es opcional y
  nunca se expone al bundle.
- pytest termina correctamente, pero Windows emite al salir un
  `PermissionError` no fatal al limpiar `pytest-current`.
- El build conserva una advertencia informativa de chunk mayor de 500 kB; la
  analítica pesada continúa en carga diferida.

## Commits e integración

- `c536059` — `Completar fuentes y analítica de la Fase 1 territorial V4`.
- El commit documental y el commit de fusión en `main` se registran en la
  entrega final, porque sus hashes solo existen después de cerrar este informe.
