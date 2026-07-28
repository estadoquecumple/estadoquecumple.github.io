#!/bin/sh
set -eu
latest_file="$BACKUP_ROOT/latest"
if [ "${1:-}" = "backup" ]; then
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  target="$BACKUP_ROOT/$stamp"
  mkdir -p "$target"
  pg_dump --format=custom --no-owner --no-acl --file="$target/database.dump"
  tar -C "$VAULT_ROOT" -czf "$target/vault.tar.gz" .
  sha256sum "$target/database.dump" "$target/vault.tar.gz" > "$target/SHA256SUMS"
  printf '{"created_at":"%s","database":"%s","vault":"vault.tar.gz"}\n' "$stamp" "$PGDATABASE" > "$target/manifest.json"
  printf '%s' "$stamp" > "$latest_file"
  echo "Backup verificado: $stamp"
elif [ "${1:-}" = "restore-test" ]; then
  stamp="$(cat "$latest_file")"
  target="$BACKUP_ROOT/$stamp"
  cd "$target"
  sha256sum -c SHA256SUMS
  test_db="${PGDATABASE}_restore_test"
  dropdb --if-exists "$test_db"
  createdb "$test_db"
  pg_restore --exit-on-error --no-owner --no-acl --dbname="$test_db" database.dump
  original="$(psql --tuples-only --no-align --command='SELECT count(*) FROM alembic_version')"
  restored="$(psql --tuples-only --no-align --dbname="$test_db" --command='SELECT count(*) FROM alembic_version')"
  test "$original" = "$restored"
  psql --dbname="$test_db" --command='SELECT PostGIS_Full_Version(); SELECT extversion FROM pg_extension WHERE extname = $$vector$$;'
  dropdb "$test_db"
  mkdir -p /tmp/vault-restore
  tar -xzf vault.tar.gz -C /tmp/vault-restore
  echo "Restauración real aprobada: $stamp"
else
  echo "Uso: backup|restore-test" >&2
  exit 2
fi
