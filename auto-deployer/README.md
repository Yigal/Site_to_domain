# Auto-Deployer

Enterprise-grade asynchronous orchestration system for automated frontend deployment across AWS, GitHub, Cloudflare, and Google Cloud Platform.

## Quick Start

### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- Cloud accounts: AWS, GitHub, Cloudflare, GCP

### Setup

1. **Clone the repository**
   ```bash
   cd auto-deployer
   ```

2. **Create virtual environment**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Start Redis**
   ```bash
   docker run -d -p 6379:6379 redis:7-alpine
   ```

### Running the Application

**Terminal 1: Start FastAPI server**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2: Start Celery worker**
```bash
celery -A worker.celery_app worker --loglevel=info
```

**Terminal 3: Start Celery beat (optional)**
```bash
celery -A worker.celery_app beat --loglevel=info
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Architecture

### Three-Tier Architecture

```
PRESENTATION LAYER
├── FastAPI REST API (Port 8000)
└── Pydantic models for validation

ORCHESTRATION LAYER
├── Celery Task Queue
├── Redis Message Broker
└── Saga Pattern for transactions

INTEGRATION LAYER
├── AWS (S3, Secrets Manager)
├── GitHub API
├── Cloudflare API
└── Google Cloud APIs
```

## Project Structure

```
auto-deployer/
├── app/                    # FastAPI application
│   ├── main.py            # API endpoints
│   ├── config.py          # Configuration management
│   ├── models/            # Pydantic schemas
│   ├── services/          # Cloud service integrations
│   └── utils/             # Utilities (AST, middleware, etc.)
├── worker/                # Celery background tasks
│   ├── celery_app.py      # Celery configuration
│   └── tasks.py           # Task definitions
├── tests/                 # Test suite
├── deployment/            # Docker configuration
├── scripts/               # Automation scripts
├── documentation/         # Agent and skill specs
├── requirements.txt       # Python dependencies
└── .env.example          # Environment template
```

## Development

### Running Tests
```bash
pytest tests/ --cov=app --cov=worker
```

### Building Docker Image
```bash
docker build -t auto-deployer:latest .
```

### Running with Docker Compose
```bash
docker-compose up -d
```

## Documentation

- **Agent Specifications**: `documentation/agents/`
- **Skill Specifications**: `documentation/skills/`
- **API Reference**: `documentation/API.md`
- **Deployment Guides**: `../execution_plan_and_review/plans/`

## Support

For issues and questions, refer to:
1. `../product_description_to_execution.md` - Complete project guide
2. `../project_description.md` - Technical architecture
3. `../execution_plan_and_review/` - Detailed execution plans

## License

Proprietary - All rights reserved

---

**Created**: January 25, 2026
**Version**: 1.0.0
**Status**: Development
