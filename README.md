# 📦 Parcel Delivery API

> FastAPI service for parcel management

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://mysql.com)
[![Redis](https://img.shields.io/badge/Redis-7.4-red.svg)](https://redis.io)

## 📋 Requirements

- Docker & Docker Compose
- Python 3.12+ (for local development)

## ⚡ Quick Start

```bash
# Clone repository
git clone https://github.com/beckrus/test-ra_delta
cd test-ra_delta

# Setup environment
cp .env_example .env
🔴fill in .env file❗
# Start services
docker-compose up -d

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs

❗ docker-compose_test.yml - db and redis for tests