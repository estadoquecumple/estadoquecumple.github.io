"""Restricciones idempotentes para importación."""
from alembic import op

revision = "0002_import_constraints"
down_revision = "0001_backend_core"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE UNIQUE INDEX uq_source_snapshot_hash ON source_snapshots(parent_id,content_hash)")
    op.execute("CREATE UNIQUE INDEX uq_dataset_version_hash ON dataset_versions(parent_id,content_hash)")

def downgrade():
    op.execute("DROP INDEX IF EXISTS uq_dataset_version_hash")
    op.execute("DROP INDEX IF EXISTS uq_source_snapshot_hash")
