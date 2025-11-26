
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/* && pip install uv

WORKDIR /app

COPY . .

RUN uv sync --frozen --no-cache

EXPOSE 8080
CMD ["uv", "run", "main.py"]
