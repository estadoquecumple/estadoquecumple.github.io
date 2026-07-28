# Backend local V4

Stack local y autoalojado: PostgreSQL 16.4, PostGIS 3 (paquete Debian oficial),
pgvector 0.8.0 compilado desde su repositorio oficial, FastAPI y un worker.
Consume como máximo 2.9 GiB entre servicios; la base usa un volumen Compose
propio y los originales se guardan inmutables en `data/vault`.

Copie `.env.lab.example` a `.env.lab`, reemplace ambos secretos y use los
comandos `npm run backend:*`. La base y la API solo publican en loopback; los
puertos predeterminados son 55432 y 8001. GitHub Pages conserva
`PUBLIC_LAB_API_BASE_URL=` y funciona únicamente con datos estáticos.

No es almacenamiento distribuido. Una publicación futura requiere TLS,
autenticación/autorización, gestión externa de secretos, monitoreo,
almacenamiento de backups cifrado fuera del equipo y una revisión de capacidad.
