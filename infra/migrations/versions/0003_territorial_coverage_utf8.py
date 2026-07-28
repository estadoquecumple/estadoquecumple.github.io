"""Cobertura territorial completa, procedencia y limpieza de fuentes auxiliares."""
from alembic import op

revision = "0003_territorial_coverage_utf8"
down_revision = "0002_import_constraints"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
      ALTER TABLE territorial_units
        ADD COLUMN level text NOT NULL DEFAULT 'department',
        ADD COLUMN literal_type text,
        ADD COLUMN normalized_type text,
        ADD COLUMN department_id uuid REFERENCES territorial_units(id),
        ADD COLUMN source_id uuid REFERENCES sources(id),
        ADD COLUMN snapshot_id uuid REFERENCES source_snapshots(id),
        ADD COLUMN content_hash text,
        ADD COLUMN geometry_reference text
    """)
    op.execute("""
      ALTER TABLE territorial_unit_versions
        ADD COLUMN territorial_unit_id uuid REFERENCES territorial_units(id),
        ADD COLUMN source_snapshot_id uuid REFERENCES source_snapshots(id),
        ADD COLUMN content_hash text,
        ADD COLUMN geom geometry(MultiPolygon,4326)
    """)
    op.execute("UPDATE territorial_units SET literal_type='DEPARTAMENTO', normalized_type='departamento'")
    op.execute("CREATE INDEX ix_territorial_level_type ON territorial_units(level,normalized_type)")
    op.execute("CREATE INDEX ix_territorial_department ON territorial_units(department_id)")
    op.execute("CREATE UNIQUE INDEX uq_territorial_level_code ON territorial_units(level,canonical_code)")
    op.execute("CREATE UNIQUE INDEX uq_territorial_version_hash ON territorial_unit_versions(territorial_unit_id,content_hash)")
    op.execute("DELETE FROM dataset_versions WHERE parent_id IN (SELECT id FROM datasets WHERE dataset_key='phase1-index')")
    op.execute("DELETE FROM datasets WHERE dataset_key='phase1-index'")
    op.execute("DELETE FROM indicators WHERE indicator_key='index'")
    op.execute("DELETE FROM sources WHERE source_key='index'")

def downgrade():
    op.execute("DROP INDEX IF EXISTS uq_territorial_version_hash")
    op.execute("DROP INDEX IF EXISTS uq_territorial_level_code")
    op.execute("DROP INDEX IF EXISTS ix_territorial_department")
    op.execute("DROP INDEX IF EXISTS ix_territorial_level_type")
    op.execute("ALTER TABLE territorial_unit_versions DROP COLUMN geom, DROP COLUMN content_hash, DROP COLUMN source_snapshot_id, DROP COLUMN territorial_unit_id")
    op.execute("ALTER TABLE territorial_units DROP COLUMN geometry_reference, DROP COLUMN content_hash, DROP COLUMN snapshot_id, DROP COLUMN source_id, DROP COLUMN department_id, DROP COLUMN normalized_type, DROP COLUMN literal_type, DROP COLUMN level")
