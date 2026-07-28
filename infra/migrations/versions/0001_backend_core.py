"""Núcleo territorial, cola durable, linaje y calidad."""
from alembic import op

revision = "0001_backend_core"
down_revision = None
branch_labels = None
depends_on = None

TABLES = (
    "sources source_snapshots datasets dataset_versions territorial_units "
    "territorial_unit_versions entities entity_aliases organizations "
    "legal_instruments legal_rules competences indicators indicator_values "
    "projects contracts scenario_definitions scenario_runs scenario_artifacts "
    "jobs job_events lineage_events quality_results"
).split()

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE TYPE quality_state AS ENUM ('unknown','valid','warning','invalid')")
    op.execute("CREATE TYPE job_state AS ENUM ('queued','running','succeeded','failed','cancel_requested','cancelled')")
    for name in TABLES:
        extras = ""
        if name == "territorial_units":
            extras = ", canonical_code text UNIQUE, name text, unit_type text, geom geometry(MultiPolygon,4326)"
        elif name == "jobs":
            extras = """, kind text NOT NULL DEFAULT 'scenario', state job_state NOT NULL DEFAULT 'queued',
              payload jsonb NOT NULL DEFAULT '{}', result jsonb, idempotency_key text UNIQUE,
              attempts integer NOT NULL DEFAULT 0, max_attempts integer NOT NULL DEFAULT 3,
              available_at timestamptz NOT NULL DEFAULT now(), locked_at timestamptz,
              locked_by text, progress integer NOT NULL DEFAULT 0, error text,
              timeout_seconds integer NOT NULL DEFAULT 300"""
        elif name == "scenario_runs":
            extras = ", definition_id uuid, job_id uuid, state text NOT NULL DEFAULT 'queued', capsule jsonb NOT NULL DEFAULT '{}'"
        elif name == "scenario_artifacts":
            extras = ", run_id uuid, path text NOT NULL, sha256 text NOT NULL, size_bytes bigint NOT NULL DEFAULT 0"
        elif name in ("source_snapshots", "dataset_versions"):
            extras = ", parent_id uuid, content_hash text NOT NULL, schema_hash text, is_valid boolean NOT NULL DEFAULT false, metadata jsonb NOT NULL DEFAULT '{}'"
        elif name == "sources":
            extras = ", source_key text UNIQUE NOT NULL, name text NOT NULL, metadata jsonb NOT NULL DEFAULT '{}'"
        elif name == "datasets":
            extras = ", dataset_key text UNIQUE NOT NULL, name text NOT NULL, source_id uuid"
        elif name == "indicators":
            extras = ", indicator_key text UNIQUE, name text"
        elif name == "indicator_values":
            extras = ", indicator_id uuid, territorial_unit_id uuid, value numeric, observed_at date"
        elif name == "job_events":
            extras = ", job_id uuid, event_type text NOT NULL, payload jsonb NOT NULL DEFAULT '{}'"
        elif name in ("lineage_events", "quality_results"):
            extras = ", event_type text, payload jsonb NOT NULL DEFAULT '{}', commit_sha text"
        else:
            extras = ", name text, metadata jsonb NOT NULL DEFAULT '{}'"
        op.execute(f"""CREATE TABLE {name} (
          id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
          valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz,
          quality_status quality_state NOT NULL DEFAULT 'unknown',
          provenance_status text NOT NULL DEFAULT 'recorded',
          created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
          {extras})""")
    op.execute("ALTER TABLE source_snapshots ADD CONSTRAINT fk_snapshot_source FOREIGN KEY(parent_id) REFERENCES sources(id)")
    op.execute("ALTER TABLE datasets ADD CONSTRAINT fk_dataset_source FOREIGN KEY(source_id) REFERENCES sources(id)")
    op.execute("ALTER TABLE dataset_versions ADD CONSTRAINT fk_version_dataset FOREIGN KEY(parent_id) REFERENCES datasets(id)")
    op.execute("ALTER TABLE indicator_values ADD CONSTRAINT fk_value_indicator FOREIGN KEY(indicator_id) REFERENCES indicators(id)")
    op.execute("ALTER TABLE indicator_values ADD CONSTRAINT fk_value_territory FOREIGN KEY(territorial_unit_id) REFERENCES territorial_units(id)")
    op.execute("ALTER TABLE job_events ADD CONSTRAINT fk_event_job FOREIGN KEY(job_id) REFERENCES jobs(id) ON DELETE CASCADE")
    op.execute("ALTER TABLE scenario_runs ADD CONSTRAINT fk_run_job FOREIGN KEY(job_id) REFERENCES jobs(id)")
    op.execute("ALTER TABLE scenario_artifacts ADD CONSTRAINT fk_artifact_run FOREIGN KEY(run_id) REFERENCES scenario_runs(id)")
    op.execute("CREATE INDEX ix_territorial_geom ON territorial_units USING gist(geom)")
    op.execute("CREATE INDEX ix_jobs_claim ON jobs(state, available_at)")
    op.execute("CREATE INDEX ix_jobs_created ON jobs(created_at)")
    op.execute("CREATE INDEX ix_versions_validity ON dataset_versions(valid_from, valid_to)")
    op.execute("CREATE INDEX ix_snapshots_hash ON source_snapshots(content_hash)")

def downgrade():
    for name in reversed(TABLES):
        op.execute(f"DROP TABLE IF EXISTS {name} CASCADE")
    op.execute("DROP TYPE IF EXISTS job_state")
    op.execute("DROP TYPE IF EXISTS quality_state")
