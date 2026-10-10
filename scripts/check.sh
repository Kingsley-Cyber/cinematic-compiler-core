#!/bin/sh
# One gate for every slice: lint, tests, the three hash logs, and the two generated files.
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
echo "check: PASS"
