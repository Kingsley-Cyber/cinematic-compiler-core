#!/bin/sh
# One gate for every slice: lint, tests, the three hash logs, the generated files and the reference docs.
set -e
cd "$(dirname "$0")/.."
mise exec -- uv run --locked ruff check .
mise exec -- uv run --locked pytest -q
for log in schemas library kernel; do
  mise exec -- uv run --locked python -m kernel.schema_log --log "$log" verify > /dev/null
done
mise exec -- uv run --locked python -m kernel.build_ir_schema --check
mise exec -- uv run --locked python -m kernel_extraction.control_inventory --check
mise exec -- uv run --locked python -m compiler.examples
mise exec -- uv run --locked python -m kernel.build_docs --check
mise exec -- uv run --locked python -m kernel.docs_plane
echo "check: PASS"
