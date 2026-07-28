from sqlalchemy import text

ALLOWED_RELATIONS = {
    "contains", "belongs_to", "governs", "elects", "appoints", "finances",
    "contracts", "executes", "supervises", "regulates", "provides", "limits",
    "depends_on", "modifies", "replaces", "derives_from",
}


def neighborhood(db, node_id, at=None, depth=2, limit=200):
    if not 1 <= depth <= 5:
        raise ValueError("depth debe estar entre 1 y 5")
    query = text("""
      WITH RECURSIVE walk(node_id,depth,path) AS (
        SELECT CAST(:node AS uuid),0,ARRAY[CAST(:node AS uuid)]
        UNION ALL
        SELECT CASE WHEN e.source_node_id=w.node_id THEN e.target_node_id ELSE e.source_node_id END,
          w.depth+1,w.path||CASE WHEN e.source_node_id=w.node_id THEN e.target_node_id ELSE e.source_node_id END
        FROM walk w JOIN graph_edges e
          ON e.source_node_id=w.node_id OR e.target_node_id=w.node_id
        WHERE w.depth<:depth
          AND e.valid_from<=COALESCE(CAST(:at AS timestamptz),now())
          AND (e.valid_to IS NULL OR e.valid_to>COALESCE(CAST(:at AS timestamptz),now()))
          AND NOT (CASE WHEN e.source_node_id=w.node_id THEN e.target_node_id ELSE e.source_node_id END=ANY(w.path))
      )
      SELECT DISTINCT n.id,n.node_type,n.canonical_key,n.name,n.properties,min(w.depth) AS depth
      FROM walk w JOIN graph_nodes n ON n.id=w.node_id
      GROUP BY n.id ORDER BY depth,n.name LIMIT :limit
    """)
    nodes = db.execute(query, {"node": str(node_id), "at": at, "depth": depth, "limit": limit}).mappings().all()
    ids = [row["id"] for row in nodes]
    edges = []
    if ids:
        edges = db.execute(text("""
          SELECT id,source_node_id,target_node_id,relation_type,valid_from,valid_to,
            confidence,method,review_status,evidence
          FROM graph_edges WHERE source_node_id=ANY(:ids) AND target_node_id=ANY(:ids)
          AND valid_from<=COALESCE(CAST(:at AS timestamptz),now())
          AND (valid_to IS NULL OR valid_to>COALESCE(CAST(:at AS timestamptz),now()))
          ORDER BY relation_type,id
        """), {"ids": ids, "at": at}).mappings().all()
    return {"nodes": [dict(row) for row in nodes], "edges": [dict(row) for row in edges], "depth": depth}
