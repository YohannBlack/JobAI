FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set workdir
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy project
COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Default command to run the scraper
CMD ["scrapy", "crawl", "linkedin_scraper"]


