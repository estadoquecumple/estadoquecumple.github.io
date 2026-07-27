# Plan maestro de mejora y ampliación
# Laboratorio Territorial Estado que Cumple — V4

## 1. Punto de partida revisado

La versión actual ya mejoró de forma importante:

- el despliegue bloquea la publicación con `npm run validate` y `npm run lab:e2e`;
- existe actualización territorial programada;
- hay auditorías funcionales más honestas;
- se redujo el uso inseguro de `innerHTML`;
- existe `scenarioToMapCollections`;
- existe `calculateScenarioDiff`;
- solo tres ejemplos permanecen habilitados;
- SAVIA no produce un resultado incondicional cuando faltan datos.

Pero el repositorio sigue siendo fundamentalmente una aplicación estática:

- dependencias de producción: Astro, MapLibre, Zod y sitemap;
- datos publicados principalmente como JSON/GeoJSON;
- sin base PostgreSQL/PostGIS;
- sin API propia;
- sin almacenamiento versionado de originales;
- sin motor analítico SQL en el navegador;
- sin optimización matemática;
- sin búsqueda semántica o resolución asistida de entidades;
- sin ejecución durable de escenarios.

Limitaciones comprobadas del código actual:

1. El recolector DANE no conserva `MPIO_TIPO`, `MPIO_NAREA` ni la resolución de creación.
2. SECOP solo publica conteos de cuatro conjuntos; no produce agregados territoriales.
3. SGR consulta como máximo 5.000 filas y declara una muestra parcial.
4. Población, tipologías, IDF y MDM permanecen como fuentes manuales.
5. La actualización semanal produce un artefacto temporal, pero no promueve automáticamente una versión validada.
6. La unión cartográfica conserva un `MultiPolygon`, pero no realiza un disolvido topológico completo.
7. No existe una cápsula reproducible integral para cada escenario.
8. No existe un catálogo operacional de fuentes, versiones y transformaciones consumible por toda la interfaz.
9. No existe grafo institucional ni registro canónico de entidades.
10. No existe backend para trabajos pesados, escenarios persistentes, IA o optimización.

## 2. Objetivo V4

Convertir el Laboratorio en una infraestructura de cuatro subsistemas:

### Bóveda RAÍCES

Conserva originales, versiones, hashes, metadatos, licencias, vigencias y evidencia.

### Red SAVIA

Recoge, valida, normaliza, relaciona, agrega y publica datos territoriales.

### Motor SEMILLAS

Compila, ejecuta, compara, optimiza y reproduce escenarios institucionales.

### Inteligencia CAMS

Busca, extrae, relaciona, explica y propone operaciones, sin reemplazar reglas deterministas, evidencia ni control humano.

La cadena obligatoria será:

`fuente → original inmutable → validación → normalización → versión publicada → escenario → reglas → geometría → consecuencias → optimización → expediente reproducible`.

---

# 3. Arquitectura objetivo

```text
Fuentes oficiales y académicas reproducibles
    │
    ├── ArcGIS REST
    ├── Socrata / SoQL / OData
    ├── CSV / XLSX / ZIP
    ├── PDF / HTML oficial
    └── OGC / STAC
    │
    ▼
Bóveda de originales inmutables
    ├── archivo original
    ├── SHA-256
    ├── fecha de publicación
    ├── fecha de descarga
    ├── licencia
    └── manifiesto
    │
    ▼
Validación y normalización
    ├── esquemas
    ├── DIVIPOLA
    ├── resolución de entidades
    ├── geometría
    ├── calidad
    └── linaje
    │
    ▼
Banco analítico
    ├── Parquet
    ├── GeoParquet
    ├── DuckDB
    └── JSON pequeños para fallback
    │
    ▼
Núcleo operacional
    ├── PostgreSQL
    ├── PostGIS
    ├── pgvector
    └── SeaweedFS autoalojado en fase posterior
    │
    ▼
Motores
    ├── reglas
    ├── compilador de escenarios
    ├── geometría
    ├── optimización OR-Tools
    ├── grafo
    └── IA asistida por fuentes
    │
    ▼
API FastAPI
    │
    ▼
Astro + MapLibre
RAÍCES · SAVIA · SEMILLAS
```

---

# 4. Principios no negociables

1. No sobrescribir originales.
2. No presentar una fuente más reciente sin conservar las anteriores.
3. No ejecutar un escenario sin registrar versiones y hashes de sus insumos.
4. No llamar dato observado a una estimación.
5. No inferir una categoría legal que la fuente no suministre.
6. No declarar “óptimo” un escenario político mediante una sola puntuación.
7. No usar una red neuronal para validar geometría, sumas, jerarquía o legalidad.
8. No exponer secretos en Astro ni en JavaScript público.
9. No permitir que una actualización defectuosa sustituya la última versión válida.
10. No publicar si fallan calidad, pruebas o reproducibilidad.

---

# 5. Fases de implementación

## Fase 1 — Fundación de datos y análisis estático

Se mantiene GitHub Pages como frontend. Todo lo pesado se procesa en CI o localmente.

### 5.1 Dependencias web

Instalar:

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

No instalar todo `@turf/turf`; usar módulos individuales para reducir el bundle.

### 5.2 Dependencias Python de procesamiento

Agregar a un archivo separado `requirements-platform-core.txt`:

- DuckDB;
- PyArrow;
- H3;
- Pandera;
- Pydantic y validadores propios;
- NetworkX;
- RapidFuzz;
- pytest;
- ruff.

### 5.3 Estructura de datos

```text
data/
  catalog/
  schemas/
  snapshots/
    <source-id>/
      <snapshot-id>/
        raw/
        normalized/
        quality/
        manifest.json
  registry/
  rules/
  models/
public/data/territorial/
  catalog/
  current/
  history/
  analytics/
```

Los archivos grandes no deben duplicarse innecesariamente en Git. En Fase 1 se usan artefactos del workflow y backup local. SeaweedFS autoalojado se reserva para la fase de backend.

### 5.4 Catálogo único de fuentes

Reemplazar el YAML mínimo por un catálogo validado con:

- ID;
- entidad;
- URL;
- tipo de acceso;
- frecuencia esperada;
- fecha del dato;
- fecha de publicación;
- fecha de descarga;
- cobertura;
- granularidad;
- clave territorial;
- licencia;
- campos;
- transformaciones;
- limitaciones;
- política de actualización;
- SHA-256;
- versión publicada;
- última versión válida;
- estado de calidad.

### 5.5 DANE

Modificar el recolector para conservar:

- `MPIO_TIPO`;
- `MPIO_NAREA`;
- `MPIO_NANO`;
- `MPIO_CRSLCION`;
- códigos originales;
- nombres originales;
- geometría oficial y geometría web simplificada en productos distintos.

No calcular centroides promediando vértices. Usar centroide geométrico o punto representativo.

Publicar conteos por tipo y pruebas contra el catálogo oficial.

### 5.6 SECOP

Reemplazar conteos por agregados reproducibles:

- por año;
- departamento;
- municipio;
- entidad contratante;
- lugar de ejecución;
- sector;
- modalidad;
- estado;
- proveedor;
- UNSPSC;
- valor;
- duración;
- adiciones;
- modificaciones.

Separar explícitamente:

- ubicación de la entidad;
- lugar de ejecución;
- cobertura contractual;
- procedencia del proveedor.

Usar SoQL agregado, paginación, caché, reintentos y un `SOCRATA_APP_TOKEN` opcional.

### 5.7 SGR

Eliminar el límite de 5.000 como supuesto de cobertura.

Recoger de forma paginada o mediante agregación SoQL:

- BPIN;
- nombre;
- estado;
- valor total;
- sector;
- ejecutor;
- código del ejecutor;
- territorio;
- fecha disponible.

No sumar registros duplicados. Publicar totales y cobertura con controles.

### 5.8 DNP

Crear adaptadores para:

- Tipologías 2026;
- IDF 2024;
- MDM: conservar la vigencia real disponible;
- metadatos CIFFIT o archivos descargables estables.

Cuando una descarga directa sea inestable:

- almacenar la URL de la página oficial;
- detectar vínculos descargables;
- descargar el original;
- fallar de forma segura si cambia;
- conservar importación manual reproducible como respaldo.

### 5.9 Parquet, GeoParquet y DuckDB

Generar:

- indicadores territoriales Parquet;
- geometría analítica GeoParquet;
- catálogo Parquet;
- base DuckDB opcional para pruebas y producción de agregados.

En el navegador:

- cargar solo columnas necesarias;
- usar Web Worker;
- imponer límite de tamaño;
- conservar fallback JSON;
- no descargar SECOP crudo.

### 5.10 H3

Crear una capa analítica opcional, no administrativa:

- resoluciones documentadas;
- equivalencia H3 ↔ DIVIPOLA;
- población/indicadores agregados;
- reglas de contención explícitas;
- no usar H3 para reemplazar límites legales.

### 5.11 Geometría

Usar Turf para operaciones interactivas pequeñas:

- disolvido;
- diferencia;
- intersección;
- validez;
- limpieza;
- detección de solape;
- contacto.

Usar Shapely/PostGIS para operaciones nacionales o de alta precisión.

### 5.12 Cápsula reproducible

Cada escenario debe registrar:

- ID de ejecución;
- fecha;
- commit Git;
- versión del contrato;
- versión del registro legal;
- datasets y hashes;
- reglas;
- modelos;
- supuestos;
- restricciones;
- semilla aleatoria;
- resultados;
- validaciones;
- advertencias.

### 5.13 Compilador de escenarios

Estados:

- borrador;
- geométricamente válido;
- institucionalmente completo;
- fiscalmente evaluado;
- jurídicamente clasificado;
- listo para deliberación.

Debe bloquear:

- unidades sin padre;
- duplicados;
- vacíos;
- ciclos;
- competencias sin responsable;
- responsabilidades sin financiación;
- autoridades sin forma de selección;
- órganos sin control;
- geometrías inválidas;
- ruta jurídica ausente;
- transición incompleta.

### 5.14 Interfaz

Agregar:

- catálogo de fuentes;
- fecha y vigencia;
- evidencia pulsable;
- comparación antes/después;
- historial versionado;
- modo guiado;
- modo experto;
- gráficos vinculados al mapa;
- vista de grafo institucional;
- expediente reproducible.

---

## Fase 2 — Infraestructura interna y API

Esta fase introduce un servicio dinámico. GitHub Pages continúa como frontend.

### 5.15 Herramientas del sistema

- Docker Desktop con WSL2;
- GitHub CLI opcional;
- PostgreSQL/PostGIS mediante contenedor;
- SeaweedFS autoalojado para almacenamiento de objetos;
- FastAPI en contenedor propio.

### 5.16 Componentes

```text
services/
  api/
  worker/
infra/
  docker/
  migrations/
  monitoring/
```

### 5.17 Base de datos

Tablas mínimas:

- `sources`;
- `source_snapshots`;
- `datasets`;
- `dataset_versions`;
- `territorial_units`;
- `territorial_unit_versions`;
- `entities`;
- `entity_aliases`;
- `organizations`;
- `legal_instruments`;
- `legal_rules`;
- `competences`;
- `indicators`;
- `indicator_values`;
- `projects`;
- `contracts`;
- `scenario_definitions`;
- `scenario_runs`;
- `scenario_artifacts`;
- `lineage_events`;
- `quality_results`.

Todas las entidades temporales deben tener vigencia.

### 5.18 API

Endpoints iniciales:

```text
GET  /health
GET  /v1/catalog/sources
GET  /v1/catalog/datasets
GET  /v1/territories
GET  /v1/territories/{id}
GET  /v1/entities
GET  /v1/indicators
GET  /v1/legal/search
POST /v1/scenarios/compile
POST /v1/scenarios/run
GET  /v1/scenarios/{run_id}
GET  /v1/scenarios/{run_id}/artifacts
POST /v1/search
```

Agregar OpenAPI automático, CORS restringido, límites y caché.

### 5.19 Ejecución de trabajos

Primera versión:

- tabla de trabajos;
- worker separado;
- bloqueo optimista;
- reintentos;
- idempotencia;
- cancelación;
- timeouts;
- límites de memoria;
- estados persistidos.

No instalar Temporal al inicio. Evaluarlo cuando existan flujos largos y concurrentes reales.

### 5.20 Almacenamiento

Bóveda de originales:

- objetos inmutables;
- rutas por fuente/fecha/hash;
- versionado;
- retención;
- checksum;
- backups.

No guardar originales pesados dentro de `public/`.

### 5.21 Calidad y linaje

- Pandera, Pydantic y validadores propios para suites de datos;
- manifiestos propios desde Fase 1;
- OpenLineage cuando la API/worker estén activos;
- página pública de calidad y cobertura.

---

## Fase 3 — Optimización, grafo e IA

### 5.22 Grafo

Comenzar con PostgreSQL + tablas de relaciones y NetworkX.

No instalar Neo4j inicialmente.

Nodos:

- territorio;
- entidad;
- órgano;
- norma;
- competencia;
- contrato;
- proyecto;
- servicio;
- infraestructura;
- indicador;
- fuente.

Relaciones con vigencia, fuente y confianza.

### 5.23 Registro canónico y resolución de entidades

Implementar:

- normalización de NIT;
- DIVIPOLA;
- alias;
- nombres históricos;
- RapidFuzz;
- reglas deterministas;
- candidatos de IA;
- cola de revisión humana.

Nunca fusionar entidades automáticamente con baja confianza.

### 5.24 Optimización

Instalar OR-Tools y construir problemas con:

- variables;
- restricciones;
- objetivos múltiples;
- soluciones factibles;
- alternativas de Pareto;
- explicación de por qué una solución fue descartada.

Primeros problemas:

1. agrupación territorial contigua;
2. localización de servicios;
3. distribución de capacidades;
4. asignación de competencias;
5. rutas de transición.

### 5.25 IA documental y búsqueda

Primero:

- extracción de metadatos;
- clasificación documental;
- reconocimiento de territorio/norma/entidad;
- búsqueda semántica;
- resumen con citas;
- detección de documentos duplicados.

Usar pgvector en PostgreSQL.

Proveedores:

- `none`: sin IA;
- `local`: embeddings/modelos locales;
- no se integra ningún proveedor de pago por consumo.

Ningún secreto se envía al navegador.

### 5.26 Redes neuronales

No entrenar una red neuronal propia antes de tener:

- tarea definida;
- conjunto etiquetado;
- línea base no neuronal;
- división de entrenamiento/validación/prueba;
- métricas;
- análisis de sesgo;
- registro de modelo;
- supervisión humana.

Usos iniciales razonables:

- clasificación de documentos oficiales;
- extracción de entidades;
- similitud semántica;
- detección de anomalías como alerta;
- pronósticos con incertidumbre cuando exista historia suficiente.

### 5.27 Registro de modelos

Instalar MLflow solo cuando exista el primer modelo entrenado o más de un experimento.

Registrar:

- versión;
- datos;
- métricas;
- sesgos;
- ámbito;
- usos prohibidos;
- estado;
- responsable.

### 5.28 ONNX en navegador

Instalar `onnxruntime-web` únicamente cuando exista un modelo pequeño, validado y útil sin conexión.

No cargar modelos grandes en móvil.

---

# 6. APIs y secretos

## Sin clave

- DANE ArcGIS REST;
- Datos Abiertos/Socrata con límites públicos;
- DNP páginas y descargas públicas;
- SGR;
- SECOP;
- SIGEP;
- OGC/STAC públicos.

## Recomendado

### Socrata

Variable:

```text
SOCRATA_APP_TOKEN=
```

Usar solo en scripts/Actions/backend, nunca en frontend.

### Accesibilidad

Opciones:

- matrices precalculadas, fixtures y fuentes abiertas en Fase 1;
- Valhalla u OSRM autoalojados en backend;
- OpenTripPlanner autoalojado para transporte público.

### IA

Opcional:

```text
LLM_PROVIDER=none
EMBEDDING_PROVIDER=none
```

El Laboratorio debe funcionar sin una API de IA.

### Base y objetos

```text
DATABASE_URL=
OBJECT_STORAGE_ENDPOINT=
```

---

# 7. Repositorios

No separar de inmediato. Primero crear carpetas internas estables.

Separar cuando exista backend desplegado:

- `estadoquecumple-web`;
- `estadoquecumple-data`;
- `estadoquecumple-engine`;
- `estadoquecumple-models`;
- `estadoquecumple-infra`.

---

# 8. Criterios de aceptación

La V4 no se declara terminada hasta que:

1. DANE conserve `MPIO_TIPO`.
2. SECOP tenga agregados territoriales reales.
3. SGR deje de ser muestra de 5.000.
4. cada fuente tenga snapshot y hash;
5. cada escenario tenga cápsula reproducible;
6. el compilador bloquee escenarios incoherentes;
7. DuckDB-Wasm funcione con fallback;
8. las geometrías pequeñas se disuelvan de verdad;
9. las operaciones grandes se envíen al backend;
10. la actualización defectuosa no sustituya la última válida;
11. el catálogo muestre vigencia y calidad;
12. el motor de optimización muestre varias alternativas;
13. la IA cite fuentes y no emita decisiones legales;
14. ningún secreto llegue al bundle público;
15. exista recuperación y copia de seguridad;
16. pruebas unitarias, integración, E2E, datos y seguridad pasen.

---

# 9. Orden recomendado

1. Ejecutar Fase 1 completa.
2. Publicar Fase 1 y observar rendimiento.
3. Diseñar y levantar Fase 2 localmente.
4. Migrar operaciones pesadas al backend.
5. Incorporar Fase 3 por casos de uso.
6. No entrenar redes propias antes de estabilizar datos y reglas.
