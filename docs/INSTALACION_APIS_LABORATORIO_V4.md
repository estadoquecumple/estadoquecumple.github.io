# Entorno y stack libre del Laboratorio Territorial V4

## Fase 1 activa

La Fase 1 funciona de forma estática, sin tarjeta, suscripción ni pago por consumo:

- Python 3.12 en el `.venv` preservado;
- Pandera, Pydantic y validadores propios para calidad;
- DuckDB, Arrow, Parquet y GeoParquet;
- GeoPandas, Shapely y H3;
- DuckDB-Wasm, Arrow, Turf modular, MapLibre y Astro;
- archivos inmutables, SHA-256, snapshots y backup local;
- fuentes públicas DANE, DNP y Socrata.

No se debe recrear ni reinstalar `.venv` cuando sus importaciones ya funcionan. En Windows, toda operación Python local usa explícitamente:

```powershell
.\.venv\Scripts\python.exe
.\.venv\Scripts\python.exe -m pip list
.\.venv\Scripts\python.exe -m pytest tests\data
```

Great Expectations puede permanecer instalado en entornos antiguos, pero ya no es requisito ni certifica calidad. Su reemplazo obligatorio es Pandera después de aprobar las pruebas equivalentes.

## Variables permitidas

```text
SOCRATA_APP_TOKEN=
LLM_PROVIDER=none
EMBEDDING_PROVIDER=none
```

El token Socrata es opcional y gratuito. Sólo se usa en scripts o CI; nunca se incorpora al bundle público. El pipeline funciona sin token con los límites públicos.

## Componentes deliberadamente aplazados

No se instalan en la Fase 1:

- Docker, PostgreSQL, PostGIS y pgvector;
- SeaweedFS;
- Valhalla, OSRM y OpenTripPlanner;
- Pelias o Nominatim;
- Ollama o llama.cpp;
- Qwen, DeepSeek y modelos de embeddings;
- OR-Tools, MLflow y ONNX;
- OpenTelemetry, Prometheus y Grafana OSS.

Son alternativas libres y autoalojables para fases posteriores, sujetas a caso de uso, capacidad y pruebas.

## Decisiones de fases posteriores

- Objetos: SeaweedFS autoalojado; no MinIO administrado ni S3 comercial por defecto.
- Rutas: matrices precalculadas y fixtures en Fase 1; Valhalla u OSRM propios en backend; OpenTripPlanner para transporte público.
- IA: `none` por defecto. Una opción local futura podrá usar Ollama/llama.cpp y modelos abiertos sólo después de verificar RAM, VRAM, disco, licencia y evaluación.
- Observabilidad: OpenTelemetry, Prometheus y Grafana OSS autoalojados.

No se integran OpenAI API, OpenRouteService comercial, bases administradas, almacenamiento comercial, SaaS de calidad ni SaaS de observabilidad.
