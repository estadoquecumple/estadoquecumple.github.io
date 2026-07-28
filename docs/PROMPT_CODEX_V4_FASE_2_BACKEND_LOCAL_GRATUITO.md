# PROMPT CODEX — LABORATORIO TERRITORIAL V4
# FASE 2 ACTUALIZADA: BACKEND LOCAL GRATUITO, POSTGIS, API, WORKER Y BÓVEDA

Trabaje en:

`C:\Users\Usuario\GitHub\estadoquecumple.github.io`

## 0. Límites

Esta fase es exclusivamente local y autoalojable.

No use:

- servicios administrados de base de datos;
- almacenamiento comercial;
- OpenAI API;
- Kimi API;
- OpenRouteService de pago;
- MinIO como dependencia predeterminada;
- Redis, Celery, Temporal, Kubernetes o Kafka;
- Docker Hub privado;
- secretos reales en Git;
- pull request;
- interfaz web de GitHub;
- force push.

GitHub Pages seguirá siendo el frontend público estático. El backend local no se presentará como servicio público disponible para otros usuarios.

## 1. Estado inicial y Git

Ejecute:

```powershell
git fetch origin --prune
git switch main
git pull --ff-only origin main
git status --short --branch
```

El árbol debe estar limpio.

Compruebe que la Fase 1 está integrada y que existen sus productos V4.

Cree:

```powershell
git switch -c laboratorio-territorial-v4-backend-local
```

Si la rama ya existe, úsela y no la recree.

No descarte cambios ajenos y no use `reset --hard`, `clean -f` o restauraciones globales.

## 2. Python

Use siempre:

```text
.\.venv\Scripts\python.exe
```

Nunca use el Python global.

Compruebe:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import pandera, duckdb, pyarrow, geopandas; print('entorno correcto')"
```

Instale solo dependencias realmente necesarias desde `requirements-api-free.txt`.

## 3. Motor de contenedores

Prefiera Podman.

Detecte:

```powershell
podman --version
podman info
podman compose version
```

Si Podman no existe, pruebe Docker:

```powershell
docker --version
docker compose version
```

Si ninguno existe o el motor no está operativo, deténgase y entregue el diagnóstico. No instale WSL o un motor desde Codex y no fuerce un reinicio.

Use una especificación Compose estándar y comandos compatibles con Podman Compose y Docker Compose.

## 4. Arquitectura

Cree:

```text
services/
  api/
  worker/
  shared/

infra/
  containers/
  migrations/
  backups/
  scripts/

data/
  vault/
```

No separe todavía en varios repositorios.

## 5. PostgreSQL, PostGIS y pgvector

Construya una imagen local reproducible usando fuentes oficiales y versiones fijadas.

Debe contener:

- PostgreSQL;
- PostGIS;
- pgvector.

Requisitos:

- versión mayor fijada;
- extensiones creadas por migración;
- imagen o Containerfile versionado;
- healthcheck;
- volumen persistente;
- base no accesible fuera de localhost;
- usuario administrador separado del usuario de aplicación;
- credenciales únicamente en `.env.lab`;
- ninguna contraseña por defecto en archivos rastreados;
- límites de memoria y almacenamiento documentados.

No use una imagen comunitaria desconocida que combine extensiones sin documentar su procedencia.

## 6. Esquema y migraciones

Use SQLAlchemy 2 y Alembic.

Implemente como mínimo:

- sources;
- source_snapshots;
- datasets;
- dataset_versions;
- territorial_units;
- territorial_unit_versions;
- entities;
- entity_aliases;
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
- job_events;
- lineage_events;
- quality_results.

Use:

- UUID o identificadores canónicos;
- `valid_from` y `valid_to`;
- `created_at` y `updated_at`;
- claves foráneas;
- restricciones únicas;
- índices espaciales;
- índices temporales;
- índices vectoriales solo donde tengan uso real;
- estado explícito de procedencia y calidad.

## 7. Importación de Fase 1

Construya un comando idempotente que importe:

- catálogo;
- snapshots;
- territorios;
- tipos DANE;
- indicadores;
- productos SGR;
- agregados SECOP;
- manifiestos;
- hashes;
- resultados de calidad.

Debe:

- registrar el hash;
- evitar duplicados;
- detectar cambios de esquema;
- conservar versiones anteriores;
- no reemplazar una versión válida por una defectuosa;
- producir un informe de importación;
- funcionar con fixtures sin internet.

## 8. Bóveda local inmutable

Implemente un proveedor inicial `local-filesystem`.

Ruta lógica:

```text
source/snapshot/hash/original
```

Características:

- escritura inmutable;
- SHA-256;
- metadatos;
- bloqueo frente a sobrescritura;
- verificación de integridad;
- exportación;
- backup;
- restauración probada.

No presente el sistema de archivos como almacenamiento distribuido.

Defina una interfaz para un proveedor futuro compatible con objetos, pero no instale SeaweedFS todavía.

## 9. API FastAPI

Implemente:

```text
GET  /health
GET  /ready
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
POST /v1/jobs/{job_id}/cancel
```

Incluya:

- OpenAPI;
- Pydantic;
- paginación;
- filtros;
- límites;
- errores estructurados;
- request ID;
- logs JSON;
- CORS restringido;
- encabezados de seguridad;
- sin datos personales;
- sin secretos en respuestas;
- endpoints de salud separados de disponibilidad completa.

## 10. Worker y cola PostgreSQL

No use Redis.

Implemente una cola durable en PostgreSQL:

- `queued`;
- `running`;
- `succeeded`;
- `failed`;
- `cancel_requested`;
- `cancelled`.

Debe soportar:

- adquisición segura;
- idempotencia;
- reintentos limitados;
- backoff;
- timeout;
- cancelación;
- progreso;
- recuperación tras reinicio;
- artefactos;
- límite de memoria y tamaño;
- bloqueo de dos workers sobre el mismo trabajo.

Use `FOR UPDATE SKIP LOCKED` o mecanismo equivalente correctamente probado.

## 11. Linaje y calidad

Conserve Pandera.

Implemente eventos propios de linaje compatibles conceptualmente con OpenLineage, sin instalar infraestructura adicional.

Cada ejecución debe relacionar:

- fuente;
- snapshot;
- dataset;
- transformación;
- escenario;
- artefacto;
- commit;
- tiempo;
- resultado de calidad.

## 12. Frontend y modo degradado

Cree un adaptador API.

La configuración predeterminada pública será:

```text
PUBLIC_LAB_API_BASE_URL=
```

Con valor vacío:

- GitHub Pages usa datos estáticos;
- no intenta `localhost`;
- no muestra funciones de backend como disponibles;
- conserva RAÍCES, SAVIA y SEMILLAS estáticas.

En desarrollo local se permitirá:

```text
PUBLIC_LAB_API_BASE_URL=http://localhost:8000
```

Implemente:

- timeout;
- cancelación;
- reintentos limitados;
- circuit breaker sencillo;
- estado de conexión;
- fallback estático;
- mensajes honestos;
- prueba de backend caído.

## 13. Seguridad

- `.env.lab` ignorado;
- `.env.lab.example` sin secretos;
- usuario DB de mínimo privilegio;
- CORS permitido únicamente para orígenes configurados;
- no usar `*` con credenciales;
- rate limiting local;
- tamaño máximo de carga;
- validación de nombres de archivo;
- protección contra traversal;
- logs sin tokens;
- consultas parametrizadas;
- escaneo de dependencias;
- backup sin credenciales;
- secretos nunca enviados al navegador.

## 14. Backups

Implemente:

- backup lógico de PostgreSQL;
- backup de la bóveda;
- manifiesto;
- checksum;
- restauración en una base vacía;
- prueba automatizada de restore;
- política local de retención documentada.

## 15. Comandos

Agregue scripts equivalentes a:

```text
backend:up
backend:down
backend:logs
backend:migrate
backend:seed
backend:test
backend:backup
backend:restore-test
backend:health
```

Deben detectar Podman o Docker sin duplicar la implementación.

## 16. Pruebas

- unitarias;
- migraciones desde cero;
- PostGIS;
- pgvector;
- importación idempotente;
- API;
- CORS;
- worker concurrente;
- reintentos;
- cancelación;
- recuperación;
- bóveda;
- integridad;
- backup y restore;
- frontend con API;
- frontend sin API;
- E2E;
- seguridad básica.

## 17. Validación

Ejecute:

```powershell
.\.venv\Scripts\python.exe -m pytest
npm run validate
npm run lab:e2e
npm audit
git diff --check
```

Levante el stack y pruebe:

```powershell
npm run backend:up
npm run backend:migrate
npm run backend:seed
npm run backend:health
npm run backend:test
npm run backend:backup
npm run backend:restore-test
```

No declare aprobado si el backend solo funciona con mocks.

## 18. Publicación del código

Esta fase publica código y configuración, no un backend público.

Cuando todo esté verde:

```powershell
git add -A
git commit -m "Implementar backend local y ejecución durable del Laboratorio Territorial V4"

git fetch origin --prune
git merge --no-ff origin/main -m "Integrar main antes de publicar backend local V4"

.\.venv\Scripts\python.exe -m pytest
npm run validate
npm run lab:e2e
git diff --check

git switch main
git pull --ff-only origin main
git merge --no-ff laboratorio-territorial-v4-backend-local -m "Publicar backend local del Laboratorio Territorial V4"

.\.venv\Scripts\python.exe -m pytest
npm run validate
npm run lab:e2e
git push origin main
```

No use force push.

## 19. Informe

Genere:

`reports/laboratorio-v4-fase2-final.md`

Incluya:

- versiones;
- imágenes;
- licencias;
- arquitectura;
- migraciones;
- endpoints;
- pruebas;
- seguridad;
- backup/restore;
- limitaciones;
- qué sigue siendo local;
- requisitos para una publicación futura.
