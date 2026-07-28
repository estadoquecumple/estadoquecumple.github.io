# Laboratorio territorial V4 — informe final de Fase 3A determinista

Fecha de validación: 2026-07-28  
Rama de trabajo: `laboratorio-territorial-v4-fase3a-grafo-optimizacion`  
Base de Fase 2: `8d2e005cee8fb4068d42ad7549bf18a0dfd2b357`

## Resultado

La Fase 3A incorpora grafo institucional temporal, resolución determinista de
entidades, cinco optimizadores OR-Tools, alternativas multiobjetivo, casos para
revisar e ingestión documental trazable. Todo opera sobre PostgreSQL real y la
cola transaccional existente. GitHub Pages conserva su modo público sin API.

La configuración se mantiene en `LLM_PROVIDER=none` y
`EMBEDDING_PROVIDER=none`. No se generaron embeddings ficticios ni se
descargaron modelos.

## Arquitectura

- PostgreSQL 16 persiste el grafo temporal, decisiones de resolución,
  ejecuciones de optimización, casos para revisar, documentos, fragmentos y
  citas.
- FastAPI expone consultas acotadas del grafo, creación y revisión de
  relaciones, resolución de entidades, optimización síncrona o en cola,
  anomalías, carga documental y citas verificables.
- El worker usa la cola PostgreSQL de Fase 2 para ejecutar trabajos de
  optimización. Conserva cancelación, reintentos, bloqueo y recuperación de
  trabajos abandonados.
- OR-Tools CP-SAT resuelve los cinco problemas deterministas con semilla,
  límite de tiempo, formulación y estado persistidos.
- Astro ofrece vistas de Grafo, Relaciones, Optimización, Evidencia,
  Documentos y Casos para revisar. La selección se sincroniza con el mapa
  mediante eventos del navegador.
- El modo guiado expone explicaciones y valores de ejemplo; el modo experto
  muestra formulación, parámetros, evidencia y JSON detallado. Ambos se
  probaron de forma independiente.

El stack mantiene el nombre Compose
`estadoquecumple-territorial-v4`, PostgreSQL en `55432` y FastAPI en `8001`,
configurables mediante `.env.lab`, sin `container_name`.

## Migración, nodos y relaciones

Alembic `0004_phase3a_deterministic` crea:

- `graph_nodes` y `graph_edges`;
- `entity_resolution_candidates` y `entity_resolution_decisions`;
- `optimization_runs` y `review_cases`;
- `documents`, `document_fragments` y `citations`;
- índices temporales, de recorrido, búsqueda y auditoría.

Tipos de nodo admitidos: territorio, entidad, competencia, fuente, documento,
indicador y servicio. Las relaciones admitidas son contiene, depende de,
coordina con, financia, presta, regula, supervisa, comparte competencia,
transfiere a y documenta.

Cada relación guarda vigencia, fuente, evidencia JSON, confianza, método y
estado de revisión. Los caminos usan una CTE recursiva, fecha efectiva y
profundidad obligatoriamente acotada entre 1 y 5.

El seed idempotente produjo:

- 1.155 nodos territoriales: 33 departamentos y 1.122 unidades locales;
- 1.122 relaciones territoriales `contains`;
- 1.164 nodos y 1.127 relaciones totales tras incluir fuentes, entidades y
  casos de prueba auditables.

Se ejecutó `downgrade` a `0003_territorial_coverage_utf8`, se comprobó la
ausencia de las tablas, y luego `upgrade head` a `0004_phase3a_deterministic`.

## Resolución canónica

La normalización aplica Unicode NFKD, minúsculas, eliminación de diacríticos,
espacios y puntuación normalizados. La resolución prioriza identificadores y
nombres exactos; RapidFuzz sólo propone candidatos aproximados con método y
puntaje explícitos.

No hay fusiones automáticas: cada candidato requiere aprobación o rechazo
humano. Ambas decisiones conservan responsable, justificación y fecha. Las
pruebas cubren coincidencia exacta, falso positivo y dos decisiones auditables.

## Optimización

Todos los datos de entrada se marcan como `user_defined`; los resultados del
solver son `calculated`. No se inventan población, costos, recaudo, tiempos,
capacidades, accesibilidad ni impactos.

1. Regiones contiguas: variables binarias `x[u,r]`; asignación única, región no
   vacía, anclajes y conectividad por adyacencia. Minimiza la diferencia entre
   tamaños máximo y mínimo.
2. Localización de servicios: `open[s]` y `assign[d,s]` binarias; cobertura,
   capacidad, presupuesto, distancia máxima y una asignación por demanda.
   Minimiza costo y distancia ponderados.
3. Distribución de capacidades: asignaciones enteras; respeta oferta, mínimos y
   compatibilidad. Minimiza capacidad sin usar.
4. Asignación de competencias: asignaciones enteras con las mismas garantías
   estructurales de oferta, mínimos y compatibilidad.
5. Transición institucional: intervalos de tareas, precedencias y no
   superposición de recursos. Minimiza el `makespan`.

Los problemas inviables retornan `INFEASIBLE`, resumen comprensible y lista de
restricciones potencialmente conflictivas; no producen una solución ficticia.
Las pruebas incluyen casos factibles e inviables.

La localización repite la solución con distintos pesos de distancia y elimina
resultados duplicados para presentar alternativas no dominadas aproximadas. La
respuesta conserva objetivos, soluciones y sensibilidad a parámetros. Los
otros optimizadores exponen su alternativa óptima y su formulación.

## Casos para revisar

El análisis explicable usa rango intercuartílico, puntaje robusto basado en
mediana/MAD y duplicados exactos. Cada señal incluye método, variables y umbral.
La etiqueta es siempre `caso para revisar`; nunca afirma fraude, corrupción ni
irregularidad comprobada. No se añadió scikit-learn porque la línea base robusta
resuelve el alcance sin una dependencia de aprendizaje automático.

## Ingestión, citas y seguridad documental

Se extrae contenido determinísticamente de PDF con texto, DOCX, XLSX, CSV,
HTML, TXT, Markdown y JSON. Cada documento conserva SHA-256, MIME, tamaño,
nombre seguro y hallazgos. Los fragmentos conservan ordinal, página cuando
existe, líneas, texto y SHA-256. Una cita sólo se acepta si su texto existe
realmente dentro del fragmento y devuelve el hash de éste.

Los documentos se tratan como datos, nunca como instrucciones. Las pruebas
reales cubren:

- prompt injection documental, marcada sin ejecutarse;
- scripts, atributos activos y elementos HTML peligrosos;
- fórmulas CSV/XLSX neutralizadas;
- macros Office rechazadas;
- traversal y nombres hostiles;
- MIME falso;
- ZIP sobredimensionado;
- archivos por encima del límite de 10 MiB;
- enlaces externos conservados únicamente como texto;
- patrones de secretos redactados antes de persistir;
- PDF real con texto y número de página.

No se ejecutan macros, JavaScript, fórmulas, enlaces, código ni instrucciones
contenidas en documentos. No se implementó OCR.

## Persistencia, respaldo y recursos

Antes y después de bajar y levantar el stack se obtuvieron exactamente los
mismos conteos: `1164|1127|8|1` para nodos, relaciones, ejecuciones y
documentos. El volumen propio se preservó.

El backup verificado `20260728T094734Z` se restauró en una base vacía. Se
compararon también los conteos de todas las tablas nuevas. La base restaurada
confirmó PostGIS 3.6.4 y pgvector 0.8.0.

Instantánea de recursos en reposo:

| Servicio | CPU | Memoria |
| --- | ---: | ---: |
| db | 4,66 % | 71,79 MiB |
| api | 0,12 % | 113,9 MiB |
| worker | 0,14 % | 82 MiB |

Los límites Compose son 1,5 GiB para PostgreSQL y 512 MiB para API y worker.
No se añadieron Redis, Celery, Kafka, Kubernetes ni almacenamiento de objetos.

## Pruebas

- Backend contra PostgreSQL/PostGIS/pgvector reales: 16 aprobadas.
- Pytest local con Python 3.12 del `.venv`: 26 aprobadas.
- Vitest: 56 aprobadas en 7 archivos.
- Astro check: 133 archivos, 0 errores, 0 advertencias, 0 pistas.
- Build: 31 páginas.
- Playwright sin API: 46 aprobadas.
- Playwright con `PUBLIC_LAB_API_BASE_URL=http://localhost:8001`: 46 aprobadas.
- Modo público final reconstruido con `PUBLIC_LAB_API_BASE_URL=` vacío.
- Migración y rollback: aprobados.
- Reinicio y persistencia: aprobados.
- Backup y restauración real: aprobados.
- `git diff --check`: aprobado.
- `npm audit --registry=https://registry.npmjs.org`: 0 vulnerabilidades.

Las pruebas cubren temporalidad, profundidad, resolución y falsos positivos,
decisiones auditables, cinco optimizadores, inviabilidad, explicación,
alternativas, sensibilidad, cola, cancelación y recuperación del worker,
anomalías, documentos, citas, seguridad, mapa-grafo, modos guiado/experto,
frontend con y sin API, móvil y accesibilidad.

## Limitaciones y Fase 3B aplazada

El grafo inicial representa relaciones verificables de contención territorial
y fuentes disponibles; ampliar relaciones institucionales requiere nueva
evidencia observada. Pareto se aproxima mediante barrido determinista de pesos,
no pretende enumerar exhaustivamente todo el frente. Las señales estadísticas
son priorización para revisión humana, no conclusiones causales.

Quedan expresamente aplazados a Fase 3B: embeddings, búsqueda vectorial
semántica, RAG generativo, asistente LLM, inferencia local, selección de
modelos, descarga de pesos y OCR. No se instalaron Ollama, llama.cpp, vLLM,
SGLang, Qwen, DeepSeek, Kimi, Moonshot, BGE-M3, Qwen3-Embedding,
sentence-transformers, transformers, torch, PaddleOCR, ONNX Runtime ni MLflow.

No se descargó ningún modelo durante la Fase 3A.
