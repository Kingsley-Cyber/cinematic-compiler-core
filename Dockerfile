# The gate in a clean, pinned environment (docs/versioning.md; owner O64):
#   docker build -t cinematic-compiler . && docker run --rm cinematic-compiler
# Python matches mise.toml; uv matches the lock's tool; dependencies come only from uv.lock.
FROM python:3.12.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.12 /uv /uvx /bin/
ENV UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /repo
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project
COPY . .
RUN uv sync --locked
CMD ["sh", "scripts/verify.sh"]
