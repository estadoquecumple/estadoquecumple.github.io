# Informe final — Laboratorio Territorial V4, Fase 2

Fecha de validación correctiva: 2026-07-28
Rama correctiva: `corregir-fase2-backup-importacion-utf8`

## Resultado

La Fase 2 funciona con un backend exclusivamente local, gratuito y austero.
GitHub Pages conserva el frontend estático funcional cuando
`PUBLIC_LAB_API_BASE_URL=`; el laboratorio local puede usar
`PUBLIC_LAB_API_BASE_URL=http://localhost:8001`.

El stack usa únicamente Docker Compose, proyecto
`estadoquecumple-territorial-v4`, sin `container_name`: PostgreSQL/PostGIS/
pgvector en `127.0.0.1:55432`, FastAPI en `127.0.0.1:8001` y un worker sin
puerto público. Los puertos son configurables en `.env.lab`. No se instalaron
Podman, Redis, Celery, Kafka, Kubernetes, MinIO, SeaweedFS, servicios pagos ni
modelos de IA.

## Correcciones

- Los scripts de contenedor quedaron en LF y `.gitattributes` obliga
  `*.sh text eol=lf`, eliminando el fallo de intérprete causado por CRLF.
- `backend:backup` genera dump PostgreSQL UTF-8, archivo del vault, manifiesto,
  conteos y `SHA256SUMS`; todos se verifican antes de marcar el respaldo como
  válido.
- `backend:restore-test` restaura en una base vacía con
  `pg_restore --exit-on-error`, compara todos los conteos, comprueba PostGIS y
  pgvector, extrae el vault y valida cada original contra su SHA-256.
- Alembic quedó en `0003_territorial_coverage_utf8`, con nivel, tipo literal y
  normalizado, padre departamental, fuente, snapshot, hash, referencia y
  versión territorial.
- El importador excluye `index.json`, elimina defensivamente el artefacto
  espurio `source_key=index`, lee UTF-8/UTF-8-SIG y serializa JSON sin escapes
  ASCII destructivos.
- La API territorial filtra por nivel, tipo, departamento, DIVIPOLA y nombre.
- El cliente de pruebas obsoleto se reemplazó por transporte ASGI directo; las
  pruebas backend terminan sin advertencias.

## Importación real y UTF-8

La carga idempotente procesó 12 manifiestos, 6 productos válidos y 1.155
unidades territoriales:

- 33 departamentos;
- 1.122 unidades locales;
- 1.103 `MUNICIPIO`;
- 18 `ÁREA NO MUNICIPALIZADA`;
- 1 `ISLA`.

Todos los locales tienen padre; no hay DIVIPOLA duplicados ni territorios sin
geometría, fuente, hash o referencia. `source_key=index` tiene conteo cero.
`QUINDÍO` está almacenado con bytes UTF-8
`5155494e44c38d4f`. Las fuentes también conservan correctamente
`validación`, `Planeación`, `Estadística` y `Contratación Pública`. La
visualización corrupta observada inicialmente correspondía a la decodificación
de la consola, no a bytes dañados en los archivos o PostgreSQL.

## Evidencia ejecutada

- `backend:up`, `backend:migrate`, `backend:seed`, `backend:health`,
  `backend:test`, `backend:backup` y `backend:restore-test`: aprobados.
- PostGIS 3.6.4 y pgvector 0.8.0: consultas reales aprobadas.
- Backend en contenedor: 10/10 pruebas contra PostgreSQL real.
- `.\.venv\Scripts\python.exe -m pytest -q`: 20/20.
- `npm run validate`: aprobado; datos, Ruff, Astro, Vitest, compilación,
  auditorías funcionales, legales, SEO y de distribución aprobadas.
- Vitest: 53/53; Playwright: 44/44.
- `npm audit --registry=https://registry.npmjs.org`: 0 vulnerabilidades.
- Frontend compilado y probado con API local y sin API; la compilación final
  quedó en el modo público sin API.
- Respaldos restaurados correctamente antes y después de recrear los servicios:
  `20260728T071137Z` y `20260728T071249Z`.
- Persistencia posterior al reinicio: 33 departamentos y 1.122 locales.
- `git diff --check`: aprobado.

La auditoría npm se ejecutó una sola vez contra el registro público oficial,
con autorización expresa y sin aplicar reparaciones automáticas.

## Aislamiento

Los contenedores detenidos `laboratorio-vial-bogota-frontend-1`,
`laboratorio-vial-bogota-backend-1` y `laboratorio-vial-bogota-db-1`, sus
imágenes y el volumen `laboratorio-vial-bogota_postgis_data` permanecieron
intactos. No fueron iniciados, detenidos, modificados, renombrados, eliminados
ni usados; tampoco se inspeccionaron sus datos.

El archivo ajeno `reports/inventario-hardware-ia.json` fue preservado sin
cambios fuera del repositorio en
`C:\Users\Usuario\Desktop\estadoquecumple-reportes\inventario-hardware-ia.json`;
SHA-256:
`E2D9264CC771D28C6FDD28100490E51F8E3951498947A66DC925DF00061F1DC1`.
