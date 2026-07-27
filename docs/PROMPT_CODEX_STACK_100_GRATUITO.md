# Mandato para Codex
# Ajustar el Laboratorio Territorial V4 a un stack 100 % gratuito y autoalojable

Trabaje en el repositorio actual.

## Condición

No utilice servicios que requieran tarjeta, suscripción o pago por consumo.

No integre:

- OpenAI API;
- OpenRouteService comercial;
- bases de datos administradas;
- almacenamiento S3 comercial;
- SaaS de calidad de datos;
- SaaS de observabilidad;
- APIs propietarias obligatorias.

El sistema debe funcionar sin conexión a una API de IA.

## Entorno actual

El entorno correcto es `.venv`, usa Python 3.12.10 y no debe recrearse, borrarse ni reinstalarse. Los entornos de respaldo no se modifican. Toda operación Python local usa `.\.venv\Scripts\python.exe`.

## Calidad de datos

Reemplace Great Expectations como dependencia obligatoria por:

- Pydantic;
- Pandera;
- pytest;
- validadores propios.

Great Expectations puede quedar documentado como opción, pero no requerido.

Actualice:

`requirements-platform-core.txt`

con el contenido de:

`requirements-platform-core-free.txt`

## Stack aprobado

- DuckDB;
- Arrow;
- Parquet/GeoParquet;
- H3;
- Shapely/GeoPandas;
- Turf modular;
- PostgreSQL;
- PostGIS;
- pgvector;
- SeaweedFS;
- Valhalla;
- OSRM;
- OpenTripPlanner;
- Pelias o Nominatim autoalojado;
- Ollama o llama.cpp;
- Qwen3;
- DeepSeek-R1 Distill Qwen;
- Qwen3-Embedding o BGE-M3;
- PaddleOCR;
- Docling;
- OR-Tools;
- OpenTelemetry;
- Prometheus;
- Grafana OSS.

No instale todo ahora. Mantenga la implementación por fases.

## IA

La configuración predeterminada será:

```text
LLM_PROVIDER=none
EMBEDDING_PROVIDER=none
```

La configuración local opcional será:

```text
LLM_PROVIDER=local
LOCAL_LLM_RUNTIME=ollama
LOCAL_LLM_MODEL=qwen3:4b
EMBEDDING_PROVIDER=local
```

No descargue modelos sin verificar RAM, VRAM y almacenamiento.

## Almacenamiento

Primera etapa:

- archivos inmutables;
- hashes;
- snapshots;
- backup local.

Fase de backend:

- SeaweedFS.

No configure MinIO como opción predeterminada.

## Rutas

Primera etapa:

- matrices precalculadas;
- fixtures;
- fuentes abiertas.

Fase de backend:

- Valhalla u OSRM autoalojado;
- OpenTripPlanner para transporte público.

## Verificación

Ejecute:

```powershell
python --version
python -c "import duckdb, pyarrow, h3, networkx, rapidfuzz; print('núcleo gratuito OK')"
python -c "import pandera; print('pandera OK')"
npm run validate
npm run lab:e2e
git diff --check
```

No fusione ni publique hasta que todo pase.
