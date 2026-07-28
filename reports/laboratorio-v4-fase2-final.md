# Informe final — Laboratorio Territorial V4, Fase 2

Fecha de validación: 2026-07-27

Rama: `laboratorio-territorial-v4-backend-local`
Alcance: backend exclusivamente local y autoalojado; GitHub Pages continúa
siendo un frontend estático funcional sin API.

## Versiones, imágenes y licencias

- Docker Desktop/Engine 29.6.2, Compose 5.3.1, contexto `desktop-linux`/WSL 2.
- Python local 3.12.10, Node 24.18.0 y npm 11.16.0.
- PostgreSQL 16.14 sobre la imagen oficial `postgres:16.4-bookworm`
  (actualizaciones de seguridad del repositorio oficial PGDG durante el build).
- PostGIS 3.6.4 desde los paquetes oficiales PGDG.
- pgvector 0.8.0 compilado desde el tag oficial; licencia PostgreSQL.
- FastAPI 0.140.7, SQLAlchemy 2.0.51, Alembic 1.18.5 y psycopg 3.3.4.
- Imágenes locales: `estadoquecumple-territorial-v4-db` (~324 MB),
  `estadoquecumple-territorial-v4-api` (~170 MB) y
  `estadoquecumple-territorial-v4-worker` (~170 MB).

No se instalaron Redis, Celery, Kafka, Kubernetes, MinIO, SeaweedFS, Podman,
servicios pagos ni modelos de IA.

## Arquitectura y aislamiento

Compose usa el proyecto fijo `estadoquecumple-territorial-v4`, sin
`container_name`. La base publica `127.0.0.1:55432 → 5432`, FastAPI publica
`127.0.0.1:8001 → 8000` y el worker no publica puertos. Ambos puertos pueden
cambiarse en `.env.lab`.

El volumen persistente es `estadoquecumple-territorial-v4-postgres`. Los
recursos de `laboratorio-vial-bogota` no se iniciaron, inspeccionaron,
reutilizaron ni modificaron. Los límites máximos son 1.5 GiB/2 CPU para DB,
512 MiB/1 CPU para API y 512 MiB/1 CPU para worker.

La bóveda `local-filesystem` usa
`source/snapshot/sha256/original`, metadatos, escritura inmutable, protección
contra traversal y verificación SHA-256. Es almacenamiento local, no
distribuido, y dispone de una interfaz para otro proveedor futuro.

## Migraciones e importación

Alembic quedó en `0002_import_constraints`. La primera migración crea PostGIS,
pgvector, 24 tablas, tipos de estado, claves foráneas e índices espaciales,
temporales y de cola. La segunda impide duplicar hashes de snapshots y
versiones.

El importador offline e idempotente procesó:

- 10 fuentes;
- 12 manifiestos/snapshots con hashes y esquema;
- 7 productos versionados, incluidos SECOP y SGR;
- 7 indicadores;
- 33 departamentos con geometría PostGIS;
- 12 resultados de calidad.

Una versión inválida se registra pero no se promueve como válida; un hash
existente no se duplica y los cambios de esquema conservan versiones previas.

## API y worker

Endpoints implementados:

- `GET /health`, `GET /ready`;
- `GET /v1/catalog/sources`, `/v1/catalog/datasets`;
- `GET /v1/territories`, `/v1/territories/{id}`;
- `GET /v1/entities`, `/v1/indicators`, `/v1/legal/search`;
- `POST /v1/scenarios/compile`, `/v1/scenarios/run`;
- `GET /v1/scenarios/{run_id}`,
  `/v1/scenarios/{run_id}/artifacts`;
- `POST /v1/jobs/{job_id}/cancel`.

FastAPI publica OpenAPI, modelos Pydantic, paginación limitada, filtros,
request ID, logs JSON, CORS configurado, encabezados de seguridad, límite de
carga y rate limiting local.

El worker adquiere trabajos con `FOR UPDATE SKIP LOCKED`, usa clave de
idempotencia, estados explícitos, tres reintentos con backoff, timeout,
cancelación, progreso, artefactos y recuperación de trabajos obsoletos.

## Frontend degradable

La configuración rastreada conserva `PUBLIC_LAB_API_BASE_URL=`. Con valor
vacío no se consulta localhost y RAÍCES, SAVIA y SEMILLAS mantienen los datos
estáticos. En `.env.lab` se permite `http://localhost:8001`. El adaptador
implementa timeout, `AbortController`, dos intentos, circuit breaker, estado de
conexión y fallback honesto. Se probaron API activa, caída y deshabilitada.

## Seguridad

- `.env.lab`, bóveda y backups runtime están ignorados.
- `.env.lab.example` no contiene contraseñas funcionales.
- Administrador y usuario de aplicación son roles separados; API/worker usan
  el rol mínimo.
- DB y API solo escuchan en loopback.
- CORS no usa comodín ni credenciales.
- Consultas parametrizadas, validación de nombres, bloqueo de traversal,
  tamaño máximo y rate limit local.
- `npm audit`: 0 vulnerabilidades.
- Ningún secreto se incorpora al frontend o a respuestas.

La carpeta `.pytest_cache` heredó una ACL inaccesible de una ejecución previa.
No se cambiaron permisos globales: quedó ignorada y pytest usa un temporal
aislado `.pytest-tmp` con el proveedor de caché desactivado.

## Backup y restauración

`backend:backup` genera `pg_dump` lógico, archivo de bóveda, manifiesto y
checksums. El backup final `20260728T003918Z` validó ambos checksums.
`backend:restore-test` creó una base vacía, ejecutó `pg_restore --exit-on-error`,
consultó PostGIS 3.6.4 y pgvector 0.8.0 en la copia restaurada y retiró solo esa
base temporal. La política recomendada es 7 copias diarias y 4 semanales en
almacenamiento cifrado separado.

## Pruebas

- `backend:up`, `down`, `logs`, `migrate`, `seed`, `health`, `test`, `backup`
  y `restore-test`: implementados y ejercitados.
- Backend en contenedor: 8 aprobadas contra PostgreSQL real.
- `.venv\Scripts\python.exe -m pytest`: 18 aprobadas.
- Vitest territorial: 6 archivos, 53 pruebas.
- `npm run validate`: aprobado; 130 archivos Astro sin diagnósticos, 31
  páginas estáticas construidas y auditorías de datos, SEO, legales y
  funcionales aprobadas.
- Playwright: 44 ejecuciones aprobadas.
- Persistencia: conteos `12 snapshots / 33 territorios` idénticos antes y
  después de reiniciar DB, API y worker.
- `npm audit`: 0 vulnerabilidades.
- `git diff --check`: aprobado.

## Limitaciones y publicación futura

Todo el backend continúa siendo local; no se ofrece disponibilidad pública.
El rate limit es por proceso y apropiado solo para laboratorio local. La
bóveda no es distribuida. La compilación de escenarios de Fase 2 es
determinista y mínima; optimización, grafo e IA corresponden a Fase 3.

Una publicación futura requiere TLS, autenticación y autorización, gestión
externa de secretos, observabilidad, política operativa de retención,
backups cifrados fuera del equipo, pruebas de carga, alta disponibilidad y una
revisión de privacidad y seguridad. GitHub Pages no depende de esa futura
publicación.
