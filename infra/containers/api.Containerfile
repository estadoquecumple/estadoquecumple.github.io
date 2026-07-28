FROM python:3.12.10-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app
WORKDIR /app
COPY requirements-api-free.txt requirements-data.txt ./
RUN pip install --no-cache-dir -r requirements-api-free.txt -r requirements-data.txt
COPY alembic.ini ./
COPY infra/migrations infra/migrations
COPY services services
COPY tests/backend tests/backend
RUN useradd --create-home --uid 10001 lab && chown -R lab:lab /app
USER lab
