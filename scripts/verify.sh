#!/bin/sh
# The one gate (owner O67): lint, tests, the four hash logs, the generated files, the examples byte for byte (golden),
# the reference docs and the docs plane. Runs before every commit (.githooks/pre-commit), in CI and nightly.
# Exit 0 and the last line "check: PASS" = green. Never pipe it into a command that hides the exit code.
set -e
cd "$(dirname "$0")/.."
if command -v mise >/dev/null 2>&1; then RUN="mise exec -- uv run --locked"; else RUN="uv run --locked"; fi
$RUN ruff check .
$RUN pytest -q
for log in schemas library kernel docs; do
  $RUN python -m kernel.schema_log --log "$log" verify > /dev/null
done
$RUN python -m kernel.build_ir_schema --check
$RUN python -m kernel.shared_schemas --check
$RUN python -m kernel_extraction.control_inventory --check
$RUN python -m compiler.examples
$RUN python -m kernel.build_docs --check
$RUN python -m kernel.docs_plane
echo "check: PASS"
