FROM postgres:16.4-bookworm
ARG PGVECTOR_VERSION=0.8.0
RUN apt-get update \
 && apt-get install -y --no-install-recommends postgresql-16-postgis-3 postgresql-16-postgis-3-scripts build-essential ca-certificates curl postgresql-server-dev-16 \
 && curl -fsSL "https://github.com/pgvector/pgvector/archive/refs/tags/v${PGVECTOR_VERSION}.tar.gz" -o /tmp/pgvector.tar.gz \
 && tar -xzf /tmp/pgvector.tar.gz -C /tmp \
 && make -C "/tmp/pgvector-${PGVECTOR_VERSION}" OPTFLAGS="" \
 && make -C "/tmp/pgvector-${PGVECTOR_VERSION}" install \
 && apt-get purge -y --auto-remove build-essential curl postgresql-server-dev-16 \
 && rm -rf /var/lib/apt/lists/* /tmp/pgvector*
LABEL org.opencontainers.image.source="https://github.com/pgvector/pgvector" \
      org.opencontainers.image.licenses="PostgreSQL"
