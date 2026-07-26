# Authentication Module

**Feature Status:** ✅ Complete

**Last Updated:** July 2026

---

# Overview

The Authentication module is responsible for verifying user identity and managing authenticated sessions within FaultLens.

Instead of using stateless JWT authentication alone, FaultLens combines JWT access tokens with persistent refresh-token sessions stored in the database. This allows sessions to be revoked, rotated, audited, and extended without forcing users to log in repeatedly.

The authentication system follows a layered architecture:

```
API
 ↓
Service
 ↓
Repository
 ↓
Database
```

The module was implemented using:

- FastAPI
- SQLAlchemy 2.0 Async ORM
- PostgreSQL
- AsyncPG
- JWT (python-jose)
- Argon2 password hashing
- Testcontainers
- Pytest

---

# Goals

The authentication module was designed to satisfy the following requirements:

- Secure user registration
- Secure password storage
- User login
- JWT-based authentication
- Refresh token rotation
- Persistent login sessions
- Session revocation (logout)
- Current authenticated user endpoint
- Fully integration tested

---

# Authentication Flow

## Registration

```
Client
   │
   ▼
POST /register
   │
   ▼
Validate request
   │
   ▼
Hash password (Argon2)
   │
   ▼
Store user
   │
   ▼
Return user
```

---

## Login

```
Client
   │
   ▼
POST /login
   │
   ▼
Verify email
   │
   ▼
Verify password
   │
   ▼
Generate Access Token
   │
   ▼
Generate Refresh Token
   │
   ▼
Store Session
   │
   ▼
Return tokens
```

---

## Authenticated Request

```
Client
      │
Authorization: Bearer AccessToken
      │
      ▼
JWT Validation
      │
      ▼
Load User
      │
      ▼
Endpoint
```

---

## Refresh Token

```
Client
      │
Refresh Token
      │
      ▼
Validate JWT
      │
      ▼
Find Session
      │
      ▼
Rotate Refresh Token
      │
      ▼
Issue New Access Token
      │
      ▼
Return Tokens
```

---

## Logout

```
Client
      │
Refresh Token
      │
      ▼
Locate Session
      │
      ▼
Delete Session
      │
      ▼
Logout Complete
```

---

# Architecture

The authentication module follows a layered architecture.

## API Layer

Responsibilities:

- Receive HTTP requests
- Validate request bodies
- Call service layer
- Return responses

Endpoints include:

- POST /register
- POST /login
- POST /refresh
- POST /logout
- GET /me

The API layer contains no business logic.

---

## Service Layer

Responsible for all authentication logic.

Examples:

- Register user
- Verify passwords
- Generate JWTs
- Rotate refresh tokens
- Logout
- Retrieve current user

The service layer orchestrates repositories but never performs SQL directly.

---

## Repository Layer

Repositories encapsulate all database access.

### UserRepository

Responsibilities

- Find by email
- Find by id
- Create user
- Update user

---

### SessionRepository

Responsibilities

- Create session
- Find by refresh token id
- Find by session id
- Find by user id
- Delete session
- Update session

---

# Database Design

## users

Stores registered users.

Important fields

- id
- email
- full_name
- password_hash
- created_at

Passwords are never stored in plaintext.

---

## user_sessions

Stores active login sessions.

Important fields

- id
- user_id
- refresh_token_id
- expires_at
- created_at

One user can have multiple active sessions.

Relationship

```
User
 └── UserSession
```

---

# Security Decisions

## Password Hashing

Passwords are hashed using Argon2 via pwdlib.

Reasons:

- Modern password hashing algorithm
- Resistant to GPU attacks
- Automatically salts passwords

Passwords are never reversible.

---

## JWT Access Tokens

Access tokens are short-lived.

They contain:

- subject (user id)
- expiration
- token type

Access tokens are never stored in the database.

---

## Refresh Tokens

Refresh tokens are long-lived.

Unlike access tokens:

- session exists in database
- can be revoked
- can be rotated
- can expire

---

## Token Rotation

Every refresh request issues:

- new access token
- new refresh token

Old refresh token becomes invalid.

This prevents replay attacks.

---

## Session Revocation

Logout deletes the stored session.

After logout:

- refresh token is unusable
- access token expires naturally

---

# API Endpoints

## POST /register

Creates a new account.

Request

```json
{
  "email": "...",
  "password": "...",
  "full_name": "..."
}
```

Response

```json
{
  "id": "...",
  "email": "...",
  "full_name": "..."
}
```

---

## POST /login

Authenticates a user.

Returns

- access token
- refresh token

---

## POST /refresh

Generates new authentication tokens.

Requires:

- refresh token

---

## POST /logout

Revokes current session.

---

## GET /me

Returns authenticated user information.

Requires:

```
Authorization: Bearer <token>
```

---

# Testing Strategy

The authentication module uses integration testing instead of mocked repositories.

Each test runs against a real PostgreSQL database inside a Docker container.

Technologies:

- Pytest
- pytest-asyncio
- HTTPX
- Testcontainers
- Async SQLAlchemy

---

## Why Testcontainers?

Originally the tests attempted to reuse a local PostgreSQL instance.

This resulted in multiple problems:

- event loop conflicts
- connection reuse
- inconsistent test isolation
- platform-specific failures

Switching to Testcontainers solved these issues.

Benefits:

- fresh database
- isolated environment
- deterministic tests
- no manual setup
- CI friendly

---

## Dependency Overrides

FastAPI dependencies are overridden during testing.

Production:

```
get_db()
        │
        ▼
Production Database
```

Tests:

```
get_db()
        │
        ▼
TestContainer Database
```

This ensures production infrastructure is never touched.

---

## Database Lifecycle

During testing:

```
Start PostgreSQL Container

↓

Create Tables

↓

Run Tests

↓

Drop Tables

↓

Dispose Engine

↓

Stop Container
```

---

# Major Problems Encountered

## 1. Async Event Loop Errors

Error

```
Future attached to a different loop
```

Cause

Database connections were created in one event loop and reused in another.

This happened because pytest-asyncio creates separate loops unless configured correctly.

Solution

Configured pytest to use a session-wide event loop.

```
asyncio_default_fixture_loop_scope = "session"
asyncio_default_test_loop_scope = "session"
```

---

## 2. AsyncPG "another operation is in progress"

Cause

Multiple operations attempted to share the same connection simultaneously.

Solution

Reworked test fixtures to:

- create independent sessions
- isolate connections
- use NullPool

---

## 3. Local Database Instability

Initially the tests targeted a locally running PostgreSQL instance.

Problems included:

- inconsistent state
- leftover data
- manual cleanup
- event loop conflicts

Decision

Move entirely to Testcontainers.

---

## 4. Relative Import Errors

Problem

```
attempted relative import with no known parent package
```

Solution

Import from

```
tests.container
```

instead of relative imports.

---

## 5. Test Database Isolation

Initially tests polluted each other's data.

Solution

Each test receives:

- fresh transaction
- isolated session

making tests deterministic.

---

# Final Test Results

Authentication module test suite:

```
23 passed in 7.82s
```

Coverage includes:

- Registration
- Login
- Logout
- Refresh Token
- Current User
- Password hashing
- JWT validation
- Database repositories
- Security helpers
- Health endpoints

---

# Lessons Learned

- Async SQLAlchemy requires careful event loop management.
- Integration tests provide significantly more confidence than mocked tests.
- Testcontainers simplify local development by eliminating external database dependencies.
- Dependency injection in FastAPI makes testing much easier.
- Authentication systems benefit from refresh-token persistence rather than purely stateless JWTs.

---

# Future Improvements

The following features are intentionally deferred:

- Email verification
- Forgot password
- Password reset
- Multi-factor authentication
- OAuth providers (Google, GitHub)
- Session management UI
- Device tracking
- Login history
- Rate limiting
- Account lockout
- Refresh token hashing
- Audit logs

---

# Completion Checklist

| Feature | Status |
|----------|--------|
| User Registration | ✅ |
| Login | ✅ |
| Logout | ✅ |
| Refresh Tokens | ✅ |
| Current User | ✅ |
| JWT Authentication | ✅ |
| Password Hashing | ✅ |
| Session Persistence | ✅ |
| Integration Tests | ✅ |
| Testcontainers | ✅ |
| Dependency Overrides | ✅ |

---

# Summary

The authentication module forms the security foundation of FaultLens.

It implements a production-oriented authentication system using JWT access tokens, persistent refresh-token sessions, Argon2 password hashing, and asynchronous PostgreSQL access. The module is fully integration tested using isolated PostgreSQL Testcontainers, providing a reliable and reproducible testing environment.

This module serves as the foundation upon which the remaining FaultLens features will be built.