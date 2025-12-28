#!/usr/bin/env bash
set -euo pipefail

echo "==> dbt preflight: generating manifest for Dagster..."

DBT_PROJECT_DIR="${DBT_PROJECT_DIR:-/app/transform/dbt/earthquake}"
DBT_PROFILES_DIR="${DBT_PROFILES_DIR:-/app/transform/dbt}"

echo "DBT_PROJECT_DIR=$DBT_PROJECT_DIR"
echo "DBT_PROFILES_DIR=$DBT_PROFILES_DIR"

cd "$DBT_PROJECT_DIR"

# Ensure clean state (important since target/ is dockerignored)
rm -rf target dbt_packages logs || true

echo "==> Running dbt deps..."
dbt deps --profiles-dir "$DBT_PROFILES_DIR"

echo "==> Running dbt parse..."
dbt parse --profiles-dir "$DBT_PROFILES_DIR"

echo "==> Manifest generated:"
ls -la target/manifest.json

echo "==> Starting Dagster user-code gRPC server..."
exec "$@"
