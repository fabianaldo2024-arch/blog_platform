#!/usr/bin/env bash
# docker-diag.sh — Diagnostic tool for Docker Compose setup

set -e

echo "🔍 1. Status of ALL containers (including stopped ones):"
docker compose ps -a

echo -e "\n🔍 2. Recent logs for all services (last 100 lines):"
docker compose logs --tail=100

echo -e "\n🔍 3. Failed containers (exit code != 0):"
docker ps -a --filter "name=$(basename $PWD)" --format "table {{.Names}}\t{{.Status}}" | grep -E "Exited \([1-9]" || echo "None with errors."

echo -e "\n🔍 4. Mapped ports and status:"
docker compose ps --format "table {{.Service}}\t{{.Ports}}"

echo -e "\n✅ Diagnostic finished."
