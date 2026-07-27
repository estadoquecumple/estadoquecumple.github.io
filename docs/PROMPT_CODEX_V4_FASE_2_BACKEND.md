# PROMPT CODEX — LABORATORIO TERRITORIAL V4
# FASE 2: POSTGRESQL/POSTGIS, API, BÓVEDA Y EJECUCIÓN ESTABLE

No ejecute esta fase antes de publicar y validar la Fase 1.

## Rama

Desde `main` actualizado:

`laboratorio-territorial-v4-backend`

No use pull request, web de GitHub ni force push.

## Requisitos del sistema

Compruebe:

- Docker Desktop;
- WSL2;
- Python 3.12;
- Node 22;
- Git;
- espacio libre.

Si Docker no está instalado, informe y entregue el comando `winget`, pero no fuerce reinicio.

## Estructura

```text
services/api
services/worker
infra/docker
infra/migrations
infra/backups
```

## Python backend

Cree `requirements-api.txt` con:

- fastapi;
- uvicorn[standard];
- pydantic-settings;
- sqlalchemy;
- alembic;
- psycopg[binary];
- geoalchemy2;
- pgvector;
- httpx;
- tenacity;
- orjson;
- python-multipart;
- structlog;
- prometheus-client.

## Contenedores

Cree:

- PostgreSQL + PostGIS;
- extensión pgvector;
- API;
- worker;
- MinIO opcional;
- healthchecks;
- volúmenes;
- red interna.

No exponga la base públicamente.

## Esquema

Implemente migraciones para:

- sources;
- snapshots;
- datasets;
- dataset_versions;
- territorial_units;
- territorial_unit_versions;
- entities;
- aliases;
- organizations;
- legal_instruments;
- legal_rules;
- competences;
- indicators;
- indicator_values;
- projects;
- contracts;
- scenario_definitions;
- scenario_runs;
- scenario_artifacts;
- jobs;
- lineage_events;
- quality_results.

Use vigencia temporal y claves canónicas.

## API

Implemente:

- health;
- catálogo;
- territorios;
- entidades;
- indicadores;
- búsqueda legal;
- compilación;
- ejecución;
- estado de trabajo;
- artefactos.

OpenAPI, validación Zod/Pydantic compatible, CORS restringido, límites, paginación y cache.

## Worker

Implementar:

- cola en PostgreSQL;
- idempotencia;
- reintentos;
- timeout;
- cancelación;
- registro de progreso;
- recuperación;
- límites.

No instalar Temporal todavía.

## Bóveda

Objetos inmutables por:

`source/snapshot/hash/original`

Agregar:

- checksum;
- metadata;
- versionado;
- backup;
- restore probado.

## Calidad y linaje

- Great Expectations en ingesta;
- OpenLineage en API/worker;
- IDs de corrida;
- relación entrada-salida;
- página de calidad.

## Frontend

Agregar cliente API con:

- timeout;
- retries limitados;
- circuit breaker simple;
- modo degradado;
- fallback estático;
- estado de conexión;
- no enviar secretos.

## Seguridad

- `.env`;
- secretos fuera de Git;
- mínimo privilegio;
- usuario DB separado;
- CORS;
- encabezados;
- rate limit;
- logs sin secretos;
- escaneo de dependencias;
- backup.

## Pruebas

- unitarias;
- migraciones;
- API;
- PostGIS;
- worker;
- idempotencia;
- cancelación;
- recuperación;
- modo degradado;
- E2E.

## Publicación

Primero despliegue local documentado. Después seleccione un proveedor compatible con contenedores y PostgreSQL/PostGIS.

No cambie GitHub Pages como frontend.

Genere:

`reports/laboratorio-v4-fase2-final.md`
