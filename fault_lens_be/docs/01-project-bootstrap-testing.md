# Project Bootstrap - Testing

## Overview

This document describes the testing strategy implemented during the Project Bootstrap phase of the FaultLens FastAPI backend.

The objective was to verify that the initial application setup works correctly before any business features are implemented.

---

# Goals

The following functionality was validated:

- FastAPI application starts successfully.
- Root endpoint is accessible.
- Database connection is healthy.
- SQLAlchemy can establish a connection with PostgreSQL.
- Automated testing environment is configured.

---

# Testing Stack

The following testing libraries were installed:

- pytest
- pytest-asyncio
- httpx
- pytest-cov
- asgi-lifespan

These provide:

- Test discovery
- Async test support
- HTTP client for FastAPI
- Coverage reporting
- Application lifespan support

---

# Project Structure

```
tests/
│
├── conftest.py
├── test_root.py
└── test_health.py
```

---

# Test Client

A shared asynchronous HTTP client is provided through a pytest fixture.

```python
@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
```

This allows every test to communicate directly with the FastAPI application without starting an external server.

---

# Root Endpoint Test

Purpose:

Verify that the API is running.

Assertions:

- HTTP Status = 200
- status == "ok"
- application == "FaultLens"

---

# Database Health Test

Purpose:

Verify that the application can connect to PostgreSQL.

The endpoint executes:

```sql
SELECT 1;
```

Assertions:

- HTTP Status = 200
- status == "ok"
- database == "connected"

This verifies:

- SQLAlchemy engine
- Async session
- Database connectivity

---

# Debugging Experience

During implementation, several issues were encountered.

## 1. pytest executable not found

Problem:

```
pytest: command not found
```

Cause:

The virtual environment had not been activated.

Solution:

```bash
source .venv/bin/activate
```

---

## 2. ModuleNotFoundError

Problem:

```
ModuleNotFoundError: No module named 'app'
```

Cause:

pytest was executed without the project root on Python's import path.

Temporary solution:

```bash
PYTHONPATH=. pytest
```

Future improvement:

Configure the project so pytest automatically includes the project root without requiring the PYTHONPATH environment variable.

---

## 3. Failed Assertions

The tests initially failed because the expected response did not match the actual API response.

Example:

Expected:

```json
{
  "database": "connected"
}
```

Actual:

```json
{
  "status": "ok",
  "database": "connected"
}
```

Lesson:

Tests should validate the API contract rather than make assumptions about the response.

---

# Lessons Learned

## Automated tests validate behavior, not implementation.

A passing manual test does not guarantee the application will continue working after future changes.

Automated tests provide confidence that existing functionality remains intact.

---

## Test only what matters.

Instead of comparing entire JSON objects, assert only the fields that define the API contract.

Example:

```python
assert data["status"] == "ok"
assert data["database"] == "connected"
```

This makes tests more resilient to unrelated changes.

---

## Shared fixtures reduce duplication.

Using a single `client` fixture allows all API tests to share the same setup while keeping the tests concise.

---

# Definition of Done

Project Bootstrap testing is complete when:

- [x] FastAPI application starts
- [x] Root endpoint tested
- [x] Database endpoint tested
- [x] Async pytest configured
- [x] HTTP test client configured
- [x] Database connectivity verified
- [x] Manual testing completed
- [x] Automated tests passing

---

# Next Milestone

Infrastructure

- Configure Alembic
- Generate the first migration
- Verify migration workflow
- Prepare the project for feature development

After infrastructure is complete, development will follow a vertical feature workflow:

```
Feature
    ↓
Backend
    ↓
Tests
    ↓
Frontend Integration
    ↓
Manual Verification
    ↓
Merge
```
