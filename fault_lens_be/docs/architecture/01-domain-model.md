# FaultLens Domain Model

## Vision

FaultLens is an AI-powered Incident Intelligence Platform that helps engineering teams understand, investigate, and resolve production issues faster.

The platform is built around one core principle:

> Everything belongs to a Project, and every Project belongs to an Organization.

---

# Core Hierarchy

User
└── Organization Membership
      └── Organization
            └── Project
                  ├── Log Sources
                  ├── Logs
                  ├── Alert Rules
                  ├── Incidents
                  ├── AI Analysis
                  ├── API Keys
                  └── Dashboard Metrics

---

# Core Concepts

## User

Represents a person with an account.

A user may belong to zero, one, or many organizations.

Users never own projects directly.

---

## Organization

Represents a company, team, client, startup, or personal workspace.

Organizations are the tenant boundary.

Everything inside FaultLens ultimately belongs to an organization.

---

## Project

Represents one monitored application or service.

Examples:

- Backend API
- Frontend
- Payment Service
- Mobile API
- Authentication Service

Projects isolate operational data.

---

# Design Principles

1. Users belong to Organizations.
2. Organizations own Projects.
3. Projects own operational resources.
4. Every operational resource belongs to exactly one Project.
5. Every Project belongs to exactly one Organization.
6. AI analyzes Project data.
7. Organization dashboards aggregate Project data.

---

# Future Modules

Organization

↓

Projects

↓

Log Sources

↓

Logs

↓

Incidents

↓

Alerts

↓

Dashboard

↓

AI Analysis

↓

Runbooks

↓

Audit Logs

↓

Billing