# Build stage
FROM python:3.12.11-slim AS builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]