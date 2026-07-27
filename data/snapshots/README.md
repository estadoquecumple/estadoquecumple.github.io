# Bóveda de snapshots

Cada snapshot se identifica por fuente y SHA-256 combinado:

```text
<source-id>/<snapshot-id>/
  raw/
  normalized/
  quality/results.json
  manifest.json
```

Los originales no se sobrescriben. Un resultado defectuoso no modifica el puntero publicado en `public/data/territorial/current/`. Los originales grandes viajan como artefactos del workflow y no dentro de `public/`.
