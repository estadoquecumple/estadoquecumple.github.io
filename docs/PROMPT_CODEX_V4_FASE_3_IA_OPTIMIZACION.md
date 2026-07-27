# PROMPT CODEX — LABORATORIO TERRITORIAL V4
# FASE 3: GRAFO, OPTIMIZACIÓN E INTELIGENCIA CAMS

No ejecutar antes de que la Fase 2 tenga base, API, worker, backups y calidad.

## Rama

`laboratorio-territorial-v4-inteligencia`

## Dependencias Python

Agregar según uso real:

- ortools;
- networkx;
- rapidfuzz;
- scikit-learn;
- sentence-transformers, solo si se aprueba modelo local;
- pgvector;
- mlflow, solo cuando exista modelo entrenado;
- onnxruntime, solo para exportación/validación local.

Frontend:

- `onnxruntime-web` únicamente cuando exista un modelo web validado;
- biblioteca de grafo seleccionada después de prototipo accesible.

## Grafo

Usar primero tablas relacionales + NetworkX.

Nodos y relaciones con:

- vigencia;
- fuente;
- confianza;
- evidencia.

Crear vista mapa ↔ grafo sincronizada.

## Resolución de entidades

Pipeline:

1. identificadores oficiales;
2. normalización;
3. reglas;
4. similitud RapidFuzz;
5. embeddings opcionales;
6. candidatos;
7. revisión humana;
8. decisión versionada.

No fusionar automáticamente por similitud semántica.

## OR-Tools

Implementar problemas reproducibles:

1. regiones contiguas;
2. localización de servicios;
3. distribución de capacidades;
4. asignación de competencias;
5. transición.

Cada ejecución debe almacenar:

- variables;
- restricciones;
- objetivos;
- solución;
- alternativas;
- inviabilidad;
- tiempo;
- solver;
- versión;
- semilla.

No presentar una única solución como política obligatoria.

## IA documental

Implementar primero:

- clasificación;
- extracción de entidades;
- detección de normas;
- búsqueda semántica;
- resumen con citas;
- explicación de escenarios.

Proveedores configurables:

- none;
- local;
- openai.

El modo `none` debe mantener funcional el sistema.

## RAG

La respuesta debe incluir:

- fragmentos;
- documento;
- fecha;
- fuente;
- vigencia;
- nivel de confianza;
- distinción entre observado, calculado, supuesto e interpretación.

La IA no decide constitucionalidad ni legalidad definitiva.

## Anomalías

Etiquetar:

`caso para revisar`

Nunca:

`corrupción detectada`

Validar contra línea base estadística simple.

## Modelos

Antes de producción:

- ficha de modelo;
- dataset;
- licencia;
- métricas;
- sesgos;
- límites;
- pruebas por territorio;
- aprobación;
- monitoreo.

MLflow solo cuando haya modelos reales.

## ONNX

Solo desplegar en navegador modelos:

- pequeños;
- rápidos;
- privados;
- evaluados;
- con fallback.

## Seguridad

- prompts y documentos no confiables;
- aislamiento de herramientas;
- listas permitidas;
- límites;
- confirmación antes de modificar escenario;
- auditoría;
- protección de datos.

## Pruebas

- resolución de entidades;
- explicaciones con citas;
- prompt injection;
- datos maliciosos;
- optimización;
- inviabilidad;
- alternativas;
- sesgo;
- fallback sin IA.

Genere:

`reports/laboratorio-v4-fase3-final.md`
