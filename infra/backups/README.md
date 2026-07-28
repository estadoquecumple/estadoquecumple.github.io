# Backups locales

`npm run backend:backup` crea un `pg_dump` lógico, un archivo de la bóveda,
un manifiesto y checksums SHA-256 en `runtime/` (ignorado por Git).
`backend:restore-test` restaura el dump en una base vacía efímera, consulta
PostGIS/pgvector y elimina únicamente esa base de prueba. Retención recomendada:
7 copias diarias y 4 semanales, siempre en almacenamiento cifrado separado.
