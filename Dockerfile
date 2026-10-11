# The gate in a clean, pinned environment (docs/versioning.md; owner O64):
#   docker build -t cinematic-compiler . && docker run --rm cinematic-compiler
# Python matches mise.toml; uv matches the lock's tool; dependencies come only from uv.lock.
FROM python:3.12.14-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.12 /uv /uvx /bin/
# The venv lives outside /repo so a mounted checkout (the nightly workflow) keeps the locked environment.
ENV UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /repo
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project
COPY . .
RUN uv sync --locked
CMD ["sh", "scripts/verify.sh"]
