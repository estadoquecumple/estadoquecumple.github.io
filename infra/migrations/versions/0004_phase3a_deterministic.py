"""Grafo, resolución, optimización y evidencia deterministas."""
from alembic import op

revision = "0004_phase3a_deterministic"
down_revision = "0003_territorial_coverage_utf8"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
      CREATE TABLE graph_nodes (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        node_type text NOT NULL CHECK (node_type IN (
          'territory','entity','organization','body','position','law','competence',
          'contract','project','service','infrastructure','indicator','source')),
        canonical_key text NOT NULL, name text NOT NULL, properties jsonb NOT NULL DEFAULT '{}',
        valid_from timestamptz NOT NULL DEFAULT now(), valid_to timestamptz,
        source_id uuid REFERENCES sources(id), quality_status quality_state NOT NULL DEFAULT 'unknown',
        created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
        UNIQUE(node_type,canonical_key)
      );
      CREATE TABLE graph_edges (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        source_node_id uuid NOT NULL REFERENCES graph_nodes(id),
        target_node_id uuid NOT NULL REFERENCES graph_nodes(id),
        relation_type text NOT NULL CHECK (relation_type IN (
          'contains','belongs_to','governs','elects','appoints','finances','contracts',
          'executes','supervises','regulates','provides','limits','depends_on',
          'modifies','replaces','derives_from')),
        valid_from timestamptz NOT NULL, valid_to timestamptz,
        source_id uuid NOT NULL REFERENCES sources(id), evidence jsonb NOT NULL,
        confidence numeric(5,4) NOT NULL CHECK(confidence BETWEEN 0 AND 1),
        method text NOT NULL, review_status text NOT NULL CHECK(review_status IN (
          'pending','approved','rejected')),
        created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
        CHECK(source_node_id <> target_node_id)
      );
      CREATE INDEX ix_graph_edges_source_time ON graph_edges(source_node_id,valid_from,valid_to);
      CREATE INDEX ix_graph_edges_target_time ON graph_edges(target_node_id,valid_from,valid_to);
      CREATE TABLE entity_resolution_candidates (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(), raw_name text NOT NULL,
        normalized_name text NOT NULL, official_identifier text, identifier_type text,
        candidate_node_id uuid REFERENCES graph_nodes(id), score numeric(5,4) NOT NULL,
        method text NOT NULL, status text NOT NULL DEFAULT 'pending',
        evidence jsonb NOT NULL DEFAULT '{}', created_at timestamptz NOT NULL DEFAULT now()
      );
      CREATE TABLE entity_resolution_decisions (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        candidate_id uuid NOT NULL REFERENCES entity_resolution_candidates(id),
        decision text NOT NULL CHECK(decision IN ('approved','rejected')),
        rationale text NOT NULL, decided_by text NOT NULL,
        decided_at timestamptz NOT NULL DEFAULT now(), previous_decision_id uuid REFERENCES entity_resolution_decisions(id)
      );
      CREATE TABLE optimization_runs (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(), optimization_type text NOT NULL,
        state text NOT NULL, input jsonb NOT NULL, formulation jsonb NOT NULL,
        solver text NOT NULL DEFAULT 'OR-Tools CP-SAT', solver_version text NOT NULL,
        seed integer NOT NULL, duration_ms integer, solution jsonb, alternatives jsonb NOT NULL DEFAULT '[]',
        infeasibility jsonb, sensitivity jsonb NOT NULL DEFAULT '{}',
        result_kind text NOT NULL DEFAULT 'calculated',
        created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
      );
      CREATE TABLE review_cases (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(), method text NOT NULL,
        subject_type text NOT NULL, subject_key text NOT NULL, metric text NOT NULL,
        observed_value numeric, score numeric, explanation text NOT NULL,
        label text NOT NULL DEFAULT 'caso para revisar',
        evidence jsonb NOT NULL DEFAULT '{}', status text NOT NULL DEFAULT 'pending',
        created_at timestamptz NOT NULL DEFAULT now()
      );
      CREATE TABLE documents (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(), original_name text NOT NULL,
        safe_name text NOT NULL, media_type text NOT NULL, size_bytes bigint NOT NULL,
        sha256 text NOT NULL UNIQUE, source_url text, document_date date,
        extraction_status text NOT NULL, security_findings jsonb NOT NULL DEFAULT '[]',
        metadata jsonb NOT NULL DEFAULT '{}', valid_from timestamptz NOT NULL DEFAULT now(),
        valid_to timestamptz, created_at timestamptz NOT NULL DEFAULT now()
      );
      CREATE TABLE document_fragments (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(), document_id uuid NOT NULL REFERENCES documents(id),
        ordinal integer NOT NULL, page integer, line_start integer, line_end integer,
        text text NOT NULL, sha256 text NOT NULL, result_kind text NOT NULL DEFAULT 'observed',
        created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(document_id,ordinal)
      );
      CREATE TABLE citations (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(), fragment_id uuid NOT NULL REFERENCES document_fragments(id),
        cited_by_type text NOT NULL, cited_by_id uuid, quote text NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now()
      );
    """)


def downgrade():
    op.execute("""
      DROP TABLE IF EXISTS citations;
      DROP TABLE IF EXISTS document_fragments;
      DROP TABLE IF EXISTS documents;
      DROP TABLE IF EXISTS review_cases;
      DROP TABLE IF EXISTS optimization_runs;
      DROP TABLE IF EXISTS entity_resolution_decisions;
      DROP TABLE IF EXISTS entity_resolution_candidates;
      DROP TABLE IF EXISTS graph_edges;
      DROP TABLE IF EXISTS graph_nodes;
    """)
