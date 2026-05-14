# REST API Service

## 📋 Project Overview

A RESTful API service built with FastAPI that provides a modern, high-performance backend solution. This API follows OpenAPI standards and includes automated interactive documentation, request validation, and comprehensive error handling.

### Description

This service implements a lightweight yet powerful API with three core endpoints designed for managing resources efficiently. The API supports standard CRUD operations with JSON request/response formats and follows REST best practices.

**Key Features:**
- 🚀 High-performance async endpoints powered by FastAPI
- 📝 Automatic OpenAPI (Swagger) documentation
- ✅ Request/response validation with Pydantic
- 🔒 Type-safe data models
- 🧪 Comprehensive test coverage
- 📊 JSON-based communication

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Framework** | FastAPI | ^0.104.0 |
| **ASGI Server** | Uvicorn | ^0.24.0 |
| **Validation** | Pydantic | ^2.0.0 |
| **Testing** | Pytest | ^7.4.0 |
| **Python** | Python | 3.9+ |

### Requirements

- **Python**: 3.9 or higher
- **pip**: Latest version recommended
- **virtualenv**: For isolated environment management

---

## 🔧 Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install fastapi uvicorn pydantic pytest httpx

# Or install from requirements.txt (if available)
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
```

---

## 🚀 Running the Service

### Start the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Verify Server is Running

```bash
curl http://localhost:8000/health
```

### Access Interactive Documentation

Once the server is running, access the auto-generated documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📚 API Endpoints Documentation

### Base URL

```
http://localhost:8000
```

### Authentication

Currently, the API does not require authentication. For production deployments, consider implementing JWT tokens or API keys.

---

## 🔌 Endpoint Reference

### 1. Health Check

**Description**: Check if the service is running and healthy.

**Endpoint**: `GET /health`

**Request Headers**:
```
Content-Type: application/json
```

**cURL Example**:
```bash
curl -X GET http://localhost:8000/health \
  -H "Content-Type: application/json"
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "REST API Service",
  "version": "1.0.0",
  "timestamp": "2024-05-14T12:00:00Z"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| status | string | Current health status of the service |
| service | string | Service name identifier |
| version | string | API version number |
| timestamp | string | ISO 8601 formatted timestamp |

---

### 2. Create Resource

**Description**: Create a new resource with the provided data.

**Endpoint**: `POST /api/v1/resources`

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Sample Resource",
  "description": "A detailed description of the resource",
  "type": "standard",
  "metadata": {
    "category": "general",
    "priority": "high",
    "tags": ["important", "active"]
  }
}
```

**Request Schema**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Resource name (max 100 chars) |
| description | string | Yes | Detailed description (max 500 chars) |
| type | string | Yes | Resource type: standard, premium, or enterprise |
| metadata | object | No | Additional metadata key-value pairs |

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/v1/resources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sample Resource",
    "description": "A detailed description of the resource",
    "type": "standard",
    "metadata": {
      "category": "general",
      "priority": "high",
      "tags": ["important", "active"]
    }
  }'
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Sample Resource",
  "description": "A detailed description of the resource",
  "type": "standard",
  "metadata": {
    "category": "general",
    "priority": "high",
    "tags": ["important", "active"]
  },
  "created_at": "2024-05-14T12:00:00Z",
  "updated_at": "2024-05-14T12:00:00Z",
  "status": "active"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique identifier for the resource |
| name | string | Resource name |
| description | string | Resource description |
| type | string | Resource type |
| metadata | object | Additional metadata |
| created_at | string | ISO 8601 creation timestamp |
| updated_at | string | ISO 8601 last update timestamp |
| status | string | Current status of the resource |

**Error Response** (400 Bad Request):
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["body", "type"],
      "msg": "value is not a valid enumeration member; permitted: 'standard', 'premium', 'enterprise'",
      "type": "type_error.enum"
    }
  ]
}
```

---

### 3. Get Resource

**Description**: Retrieve a specific resource by its unique identifier.

**Endpoint**: `GET /api/v1/resources/{resource_id}`

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| resource_id | string (UUID) | Yes | Unique identifier of the resource |

**Request Headers**:
```
Content-Type: application/json
```

**cURL Example**:
```bash
curl -X GET http://localhost:8000/api/v1/resources/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json"
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Sample Resource",
  "description": "A detailed description of the resource",
  "type": "standard",
  "metadata": {
    "category": "general",
    "priority": "high",
    "tags": ["important", "active"]
  },
  "created_at": "2024-05-14T12:00:00Z",
  "updated_at": "2024-05-14T12:00:00Z",
  "status": "active"
}
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Resource not found",
  "resource_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-05-14T12:00:00Z"
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["path", "resource_id"],
      "msg": "value is not a valid uuid",
      "type": "type_error.uuid"
    }
  ]
}
```

---

### 4. List Resources

**Description**: Retrieve a paginated list of all resources with optional filtering.

**Endpoint**: `GET /api/v1/resources`

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| skip | integer | No | 0 | Number of records to skip |
| limit | integer | No | 10 | Maximum number of records to return (max: 100) |
| type | string | No | - | Filter by resource type |
| status | string | No | - | Filter by status |

**Request Headers**:
```
Content-Type: application/json
```

**cURL Example (Basic)**:
```bash
curl -X GET "http://localhost:8000/api/v1/resources?skip=0&limit=10" \
  -H "Content-Type: application/json"
```

**cURL Example (With Filters)**:
```bash
curl -X GET "http://localhost:8000/api/v1/resources?skip=0&limit=10&type=standard&status=active" \
  -H "Content-Type: application/json"
```

**Response** (200 OK):
```json
{
  "total": 42,
  "skip": 0,
  "limit": 10,
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Sample Resource",
      "description": "A detailed description of the resource",
      "type": "standard",
      "metadata": {
        "category": "general",
        "priority": "high",
        "tags": ["important", "active"]
      },
      "created_at": "2024-05-14T12:00:00Z",
      "updated_at": "2024-05-14T12:00:00Z",
      "status": "active"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Another Resource",
      "description": "Another detailed description",
      "type": "premium",
      "metadata": {
        "category": "special",
        "priority": "medium",
        "tags": ["new"]
      },
      "created_at": "2024-05-14T11:30:00Z",
      "updated_at": "2024-05-14T11:30:00Z",
      "status": "active"
    }
  ]
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| total | integer | Total number of resources matching the filters |
| skip | integer | Number of records skipped |
| limit | integer | Maximum number of records returned |
| items | array | Array of resource objects |

**Error Response** (400 Bad Request):
```json
{
  "detail": "Invalid query parameters",
  "errors": {
    "limit": "limit cannot exceed 100"
  }
}
```

---

## 📖 Complete Request/Response Examples

### Example 1: Full Resource Lifecycle

#### Step 1: Create a Resource
```bash
# Create a new resource
curl -X POST http://localhost:8000/api/v1/resources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Database",
    "description": "Primary production database instance",
    "type": "enterprise",
    "metadata": {
      "region": "us-east-1",
      "environment": "production",
      "version": "14.5"
    }
  }'
```

**Response**:
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "name": "Production Database",
  "description": "Primary production database instance",
  "type": "enterprise",
  "metadata": {
    "region": "us-east-1",
    "environment": "production",
    "version": "14.5"
  },
  "created_at": "2024-05-14T12:00:00Z",
  "updated_at": "2024-05-14T12:00:00Z",
  "status": "active"
}
```

#### Step 2: Retrieve the Created Resource
```bash
curl -X GET http://localhost:8000/api/v1/resources/7c9e6679-7425-40de-944b-e07fc1f90ae7 \
  -H "Content-Type: application/json"
```

**Response**:
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "name": "Production Database",
  "description": "Primary production database instance",
  "type": "enterprise",
  "metadata": {
    "region": "us-east-1",
    "environment": "production",
    "version": "14.5"
  },
  "created_at": "2024-05-14T12:00:00Z",
  "updated_at": "2024-05-14T12:00:00Z",
  "status": "active"
}
```

#### Step 3: List All Resources
```bash
curl -X GET "http://localhost:8000/api/v1/resources?limit=5" \
  -H "Content-Type: application/json"
```

**Response**:
```json
{
  "total": 3,
  "skip": 0,
  "limit": 5,
  "items": [
    {
      "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "name": "Production Database",
      "description": "Primary production database instance",
      "type": "enterprise",
      "metadata": {
        "region": "us-east-1",
        "environment": "production",
        "version": "14.5"
      },
      "created_at": "2024-05-14T12:00:00Z",
      "updated_at": "2024-05-14T12:00:00Z",
      "status": "active"
    }
  ]
}
```

---

## 🧪 Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_api.py -v

# Run tests matching a pattern
pytest -k "test_create" -v

# Run tests with output
pytest -v -s
```

### Test Structure

```
tests/
├── __init__.py
├── test_api.py          # API endpoint tests
├── test_models.py       # Data model tests
└── test_integration.py  # Integration tests
```

### Example Test Output

```
tests/test_api.py::test_health_check PASSED                          [ 20%]
tests/test_api.py::test_create_resource PASSED                       [ 40%]
tests/test_api.py::test_get_resource PASSED                          [ 60%]
tests/test_api.py::test_list_resources PASSED                        [ 80%]
tests/test_api.py::test_resource_not_found PASSED                    [100%]

========================= 5 passed in 0.42s ==========================
```

---

## 📁 Project Structure

```
project/
├── app/
│   ├── __init__.py           # Application initialization
│   ├── main.py               # FastAPI application entry point
│   ├── models.py             # Pydantic data models
│   ├── schemas.py            # Request/response schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py  # API endpoint definitions
│   │   │   └── dependencies.py
│   │   └── routes.py         # Route configuration
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Application configuration
│   │   └── security.py       # Security utilities
│   └── services/
│       ├── __init__.py
│       └── resource_service.py  # Business logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_api.py           # API tests
│   ├── test_models.py        # Model tests
│   └── test_integration.py  # Integration tests
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── pyproject.toml            # Project metadata (optional)
```

### Key Files Description

| File/Directory | Description |
|----------------|-------------|
| `app/main.py` | FastAPI application instance and configuration |
| `app/models.py` | Pydantic models for data validation |
| `app/api/v1/endpoints.py` | API endpoint implementations |
| `tests/` | Test suite for the application |
| `requirements.txt` | Python package dependencies |
| `.env` | Environment-specific configuration |

---

## 🔍 HTTP Status Codes

The API uses standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| **200** OK | Request succeeded |
| **201** Created | Resource successfully created |
| **400** Bad Request | Invalid request parameters |
| **404** Not Found | Resource not found |
| **422** Unprocessable Entity | Validation error |
| **500** Internal Server Error | Server error |

---

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

#### Module Not Found Error
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Import Errors
```bash
# Ensure you're in the project root directory
cd /workspace/project

# Run with Python module syntax
python -m uvicorn app.main:app --reload
```

---

## 🔐 Security Considerations

For production deployments:

1. **Enable CORS**: Configure CORS middleware with specific origins
2. **Add Authentication**: Implement JWT or OAuth2
3. **Rate Limiting**: Add rate limiting middleware
4. **HTTPS**: Always use HTTPS in production
5. **Input Validation**: Leverage Pydantic models (already implemented)
6. **Environment Variables**: Store sensitive data in environment variables
7. **Logging**: Implement comprehensive logging

---

## 📊 Performance Tips

- Use **async/await** for I/O operations
- Enable **uvicorn workers** for production (`--workers 4`)
- Implement **caching** for frequently accessed data
- Use **connection pooling** for database connections
- Enable **Gzip compression** middleware
- Monitor with **Prometheus/Grafana**

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Support

For questions and support:
- **Issues**: GitHub Issues
- **Documentation**: [FastAPI Documentation](https://fastapi.tiangolo.com/)
- **Email**: support@example.com

---

## 🗺️ Roadmap

- [ ] Add authentication (JWT)
- [ ] Implement database integration (PostgreSQL)
- [ ] Add Docker support
- [ ] Implement CI/CD pipeline
- [ ] Add WebSocket support
- [ ] Implement caching (Redis)
- [ ] Add monitoring and metrics
- [ ] Write comprehensive documentation

---

**Version**: 1.0.0  
**Last Updated**: 2024-05-14  
**Status**: Active Development
