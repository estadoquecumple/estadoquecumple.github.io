#!/bin/sh
set -eu

latest_file="$BACKUP_ROOT/latest"
tables="alembic_version sources source_snapshots datasets dataset_versions territorial_units territorial_unit_versions indicators quality_results jobs graph_nodes graph_edges entity_resolution_candidates entity_resolution_decisions optimization_runs review_cases documents document_fragments citations"

database_counts() {
  database_name="$1"
  for table in $tables; do
    count="$(psql --dbname="$database_name" --tuples-only --no-align --set=ON_ERROR_STOP=1 --command="SELECT count(*) FROM $table")"
    printf '%s=%s\n' "$table" "$count"
  done
}

if [ "${1:-}" = "backup" ]; then
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  target="$BACKUP_ROOT/$stamp"
  mkdir -p "$target"
  pg_dump --format=custom --no-owner --no-acl --encoding=UTF8 --file="$target/database.dump"
  tar -C "$VAULT_ROOT" -czf "$target/vault.tar.gz" .
  database_counts "$PGDATABASE" > "$target/database-counts.txt"
  printf '{"created_at":"%s","database":"%s","encoding":"UTF8","dump":"database.dump","vault":"vault.tar.gz","counts":"database-counts.txt"}\n' "$stamp" "$PGDATABASE" > "$target/manifest.json"
  (cd "$target" && sha256sum database.dump vault.tar.gz database-counts.txt manifest.json > SHA256SUMS)
  (cd "$target" && sha256sum -c SHA256SUMS)
  printf '%s' "$stamp" > "$latest_file"
  echo "Backup verificado: $stamp"
elif [ "${1:-}" = "restore-test" ]; then
  stamp="$(cat "$latest_file")"
  target="$BACKUP_ROOT/$stamp"
  cd "$target"
  sha256sum -c SHA256SUMS
  grep -q '"encoding":"UTF8"' manifest.json
  test_db="${PGDATABASE}_restore_test"
  restore_vault="$(mktemp -d)"
  cleanup() {
    dropdb --if-exists "$test_db" >/dev/null 2>&1 || true
    rm -rf "$restore_vault"
  }
  trap cleanup EXIT INT TERM
  dropdb --if-exists "$test_db"
  createdb "$test_db"
  pg_restore --exit-on-error --no-owner --no-acl --dbname="$test_db" database.dump
  database_counts "$test_db" > restored-counts.txt
  cmp database-counts.txt restored-counts.txt
  psql --dbname="$test_db" --command='SELECT PostGIS_Full_Version(); SELECT extversion FROM pg_extension WHERE extname = $$vector$$;'
  tar -xzf vault.tar.gz -C "$restore_vault"
  find "$restore_vault" -name metadata.json -type f | while IFS= read -r metadata; do
    original_file="$(dirname "$metadata")/original"
    expected="$(sed -n 's/.*"sha256"[[:space:]]*:[[:space:]]*"\([0-9a-f]*\)".*/\1/p' "$metadata")"
    test -n "$expected"
    test "$(sha256sum "$original_file" | cut -d ' ' -f 1)" = "$expected"
  done
  echo "Restauración real aprobada: $stamp"
else
  echo "Uso: backup|restore-test" >&2
  exit 2
fi
